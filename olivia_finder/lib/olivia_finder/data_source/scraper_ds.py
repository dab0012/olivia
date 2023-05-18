'''
scraper_ds.py
=============

Description
-----------

Module that contains ...

File information:
    - File: scraper.py
    - Project: data_source
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Union
import requests
import tqdm
from .data_source import DataSource
from ..myrequests.request_handler import RequestHandler
from ..myrequests.job import RequestJob
from ..utilities.exception import OliviaFinderException
from ..utilities.logger import MyLogger

class ScraperDataSource(DataSource, ABC):

    """
    Base class for custom scraping implementations of software repositories as CRAN, PyPI, etc.
    This class is an abstract class, so it cannot be instantiated.
    The subclasses must implement the abstract methods.
    This class is a subclass of the DataSource class.
    This class implements the methods _build_urls, obtain_package_data and obtain_packages_data
    
    Attributes
    ----------
    name : str
        Name of the data source
    description : str
        Description of the data source
    request_handler : RequestHandler
        Request handler for making the requests
    not_found : list[str]
        List of packages not found
    """
    
    def __init__(
        self, 
        name: str = None, 
        description: str = None,
        request_handler: RequestHandler = None,
    ):
        """
        Constructor of the class

        Parameters
        ----------
        name : str, optional
            Name of the data source, by default None
        description : str, optional
            Description of the data source, by default None
        request_handler : RequestHandler, optional
            Request handler for making the requests, by default None
        """

        super().__init__(name, description)

        # Initialize the request handler, use the default one if None is passed
        self.request_handler = request_handler if request_handler is not None else RequestHandler()

        # Initialize the not_found list for storing the packages that are not found
        self.not_found = []   

    def _build_jobs(self, package_names:list[str]) -> list[RequestJob]:
        '''
        Build the jobs for scraping the packages of the package_names list

        Parameters
        ----------
        package_names : list[str]
            List of package names to scrape

        Returns
        -------
        list[RequestJob]
            List of jobs to scrape
        '''

        return [RequestJob(package_name, self._build_url(package_name)) for package_name in package_names]

    def obtain_packages_data(
        self, 
        package_names: list[str] = None,
        progress_bar: tqdm.tqdm = None,
    ) -> Tuple[dict[dict], list[str]]:
        '''
        Scrape a list of packages from a package manager, if the package is not found, it is added to the not_found list
        Overrides the method of the DataSource class

        Parameters
        ----------
        package_names : list[str], optional
            List of package names to scrape, by default None
        progress_bar : tqdm.tqdm, optional
            Progress bar for visualizing the progress, by default None
        full_scrape : bool, optional
            If True, it tries to scrape all the packages obtainig the package names from the data source, by default False
            Only works if package_names is None

        Raises
        ------
        ScraperError
            If the list of package names is None or empty and full_scrape is disabled
    
        Returns
        -------
        Tuple[list[dict], list[str]]
            Tuple with the list of packages data and the list of packages not found
            
        Examples
        --------
        >>> scraper = Scraper()
        >>> scraper.obtain_packages_data(['numpy', 'pandas'])
        '''

        # If package_names is None, obtain the package names from the data source
        if package_names is None or len(package_names) == 0:
            MyLogger.get_logger('scraper').debug('Package names list is None or empty')
            MyLogger.get_logger('scraper').debug(f'Obtaining package names from Scraper: {self.name}, {self.description}')
            package_names = self.obtain_package_names()

        else:
            MyLogger.get_logger('scraper').debug('Using package names from param list')

        MyLogger.get_logger('scraper').debug(f'Total packages to scrape: {len(package_names)}')
        MyLogger.get_logger('scraper').debug('Building jobs')
        jobs = self._build_jobs(package_names)

        # Do the requests with the RequestHandler whitout parallelization
        MyLogger.get_logger('scraper').debug('Making requests')
        finnalized_jobs = self.request_handler.do_requests(
            request_jobs=jobs,
            progress_bar=progress_bar
        )

        # Initialize the list of packages
        packages = []
        packages_keys = {}

        # Initialize the list of packages not found
        not_found = []

        for finnalized_job in finnalized_jobs:
            
            # If the response is None, the package is not found
            if finnalized_job.response is None:
                not_found.append(finnalized_job.key)
                continue

            # Parse the source data and add it to the list
            if finnalized_job.key not in packages_keys:
                packages_keys[finnalized_job.key] = True
                packages.append(self._parser(finnalized_job.response))

        # Clear the variables to save memory
        del jobs
        del finnalized_jobs
        del packages_keys
        del package_names
        
        # Return the packages and the packages not found
        return packages, not_found
    
    def obtain_package_data(self, package_name: str) -> Union[dict, None]:
        """
        Obtain the data of a package from the web page of the package manager

        Parameters
        ----------
        package_name : str
            Name of the package to be scraped

        Returns
        -------
        dict
            dictionary with the data of the package
        None
            If the package is not found
        """

        # Make the request, the response is the second element of the tuple returned by do_request
        MyLogger.get_logger('scraper').debug(f'Scraping package {package_name}')
        request_job = self.request_handler.do_request(
            RequestJob(package_name, self._build_url(package_name))
        )

        # Parse the response
        if request_job.response is None:
            
            MyLogger.get_logger('scraper').debug(
                f'Package {package_name} not found\n' +
                f'Adding {package_name} to the not found list'
            )
            self.not_found.append(package_name)
            return None
        else:
            package_data = self._parser(request_job.response)

        # If the package is found, log it and return the package data
        MyLogger.get_logger('scraper').debug(f'Package {package_name} scraped successfully')
        return package_data 

    # Abstract methods
    # ----------------
    # This methods should be implemented in the child class

    @abstractmethod
    def obtain_package_names(self) -> list[str]:
        """
        Obtain the package names from the web page of the package manager
        it must handle exceptions and return an empty list if the package names cannot be obtained
        To be implemented by the child class
        
        Raises
        ------
        NotImplementedError
            Bcause the method is not implemented in the base class
        """
        raise NotImplementedError

    @abstractmethod
    def _build_url(self, package_name: str) -> str:
        '''
        Build the url for scraping a package
        This method must be implemented by the child class
        
        Parameters
        ----------
        package_name : str
            Name of the package to scrape

        Returns
        -------
        str
            Url to request the package data
        '''
        
        raise NotImplementedError

    @abstractmethod
    def _parser(self, response: requests.Response) -> dict:
        '''
        Parse the response of the package page
        This method must be implemented by the child class
        
        Parameters
        ----------
        response : requests.Response
            Response of the package page

        Returns
        -------
        dict
            Package data as a dictionary
        '''
        raise NotImplementedError
    
class ScraperError(OliviaFinderException, BaseException):
    '''
    Exception raised when an error occurs while scraping
    '''
    



    