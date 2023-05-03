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
from typing import Optional, Tuple, Union
import requests
import tqdm
from .data_source import DataSource
from ..myrequests.request_handler import RequestHandler
from ..myrequests.job import RequestJob
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
        List of packages that are not found
    auxiliary_datasources : list[DataSource]
        List of auxiliary data sources
    packages_data : dict
        dictionary with the packages data

    Parameters
    ----------
    name : str, optional
        Name of the data source, by default None
    description : str, optional
        Description of the data source, by default None
    auxiliary_datasources : list[DataSource], optional
        List of auxiliary data sources, by default None
    request_handler : RequestHandler, optional
        Request handler for making the requests, by default None

    """
    
    def __init__(
        self, 
        name: Optional[str] = None, 
        description: Optional[str] = None,
        request_handler: Optional[RequestHandler] = None,
    ):
        """
        Constructor of the class
        """

        # Call the constructor of the parent class (DataSource)
        super().__init__(name, description)

        # if request_handler is None build a generic RequestHandler
        if request_handler is None:
            self.request_handler: RequestHandler = RequestHandler()
        else:
            self.request_handler: RequestHandler = request_handler

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
        package_names: Optional[list[str]] = None,
        progress_bar: Optional[tqdm.tqdm] = None,
    ) -> Tuple[list[dict], list[str]]:
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
            MyLogger().get_logger().debug('Package names list is None or empty')
            MyLogger().get_logger().debug(f'Obtaining package names from Scraper: {self.name}, {self.description}')
            package_names = self.obtain_package_names()

        else:
            MyLogger().get_logger().debug('Using package names from param list')

        MyLogger().get_logger().debug(f'Total packages to scrape: {len(package_names)}')

        MyLogger().get_logger().debug('Building jobs')
        jobs = self._build_jobs(package_names)

        # Do the requests with the RequestHandler whitout parallelization
        MyLogger().get_logger().debug('Making requests')
        finnalized_jobs = self.request_handler.do_requests(
            jobs,
            progress_bar=progress_bar
        )

        # Initialize the list of packages
        packages = []

        # Initialize the list of packages not found
        not_found = []

        for finnalized_job in finnalized_jobs:
            
            # If the response is None, the package is not found
            if finnalized_job.response is None:
                not_found.append(finnalized_job.key)
                continue

            # Parse the source data and add it to the list
            packages.append(self._parser(finnalized_job.response))

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
        MyLogger().get_logger().debug(f'Scraping package {package_name}')
        request_job = self.request_handler.do_request(
            RequestJob(package_name, self._build_url(package_name))
        )

        # Parse the response
        if request_job.response is None:
            
            MyLogger().get_logger().debug(f'Package {package_name} not found')
            MyLogger().get_logger().debug(f'Adding {package_name} to the not found list')
            self.not_found.append(package_name)
            return None
        else:
            package_data = self._parser(request_job.response)

        # If the package is found, log it and return the package data
        MyLogger().get_logger().debug(f'Package {package_name} scraped successfully')
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
    
class ScraperError(Exception):
    """
    Exception for the Scraper class
    
    Attributes
    ----------
    message : str
        Message of the exception
        
    Parameters
    ----------
    message : str, optional
        Message of the exception, by default ''
    """
    
    def __init__(self, message: str = ''):
        '''Constructor'''
        super().__init__()
        self.message = message
        MyLogger().get_logger().debug(str(self))

    def __str__(self):
        """
        String representation of the exception
        
        Returns
        -------
        str
            String representation of the exception
        """
        return f'ScraperError: {self.message}'
    