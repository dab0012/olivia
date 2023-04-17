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
from typing import Dict, List, Optional, Tuple
import requests
import tqdm
from .data_source import DataSource
from ..myrequests.request_handler import RequestHandler
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
        Dictionary with the packages data

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
        auxiliary_datasources: Optional[List[DataSource]] = None, 
        request_handler: Optional[RequestHandler] = None, 
    ):
        """
        Constructor of the class
        """

        # Call the constructor of the parent class (DataSource)
        super().__init__(name, description, auxiliary_datasources)

        # if request_handler is None build a generic RequestHandler
        if request_handler is None:
            self.request_handler: RequestHandler = RequestHandler.get_instance()
        else:
            self.request_handler: RequestHandler = request_handler

        # Initialize the not_found list for storing the packages that are not found
        self.not_found = []

    def _build_urls(self, package_names: List[str]) -> List[str]:
        '''
        Build the urls for scraping the packages of the package_names list
        
        Attributes
        ----------
        package_names : list[str]
            List of package names to scrape
        
        Returns
        -------
        list[str]
            List of urls to scrape
        '''
        
        return [self._build_url(package_name) for package_name in package_names]
    
    def obtain_packages_data(
        self, 
        package_names: Optional[List[str]] = None,
        progress_bar: Optional[tqdm.tqdm] = None,
        from_data_source: Optional[bool] = False
    ) -> Tuple[List[Dict], List[str]]:
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
            if not from_data_source:
                raise ScraperError('package_names is None or empty and full_scrape is disabled')
            
            MyLogger.log(f'Obtaining package names from Scraper: {self.name}, {self.description}')
            package_names = self.obtain_package_names()
            
        else:
            MyLogger.log('Using package names from param list')

        # Build the urls
        MyLogger.log('Building urls')
        urls = self._build_urls(package_names)
        
        # Map the urls to the package names
        url_package_names = {urls[i]: package_names[i] for i in range(len(urls))}

        # Do the requests with the RequestHandler parallelism
        responses = self.request_handler.do_parallel_requests(urls, progress_bar=progress_bar)

        # Parse the responses
        packages = []
        not_found = []
        for key_url in responses.keys():
            response = responses[key_url]

            # Check if the package exists
            if response.status_code == 404:
                not_found_name = url_package_names[key_url]
                not_found.append(not_found_name)
                MyLogger.log(f'Package {not_found_name} not found, status code: {response.status_code}, url: {key_url}, skipping...')
                continue

            # Parse the source data and add it to the list
            packages.append(self._parser(response))

        return packages, not_found

    def obtain_package_data(self, package_name: str) -> Dict:
        """
        Obtain the data of a package from the web page of the package manager

        Parameters
        ----------
        package_name : str
            Name of the package to be scraped

        Returns
        -------
        Dict
            Dictionary with the data of the package

        """


        # Make the request, the response is the second element of the tuple returned by do_request
        MyLogger.log(f'Scraping package {package_name}')
        response = self.request_handler.do_request(
            self._build_url(package_name)
        )[1]

        # Parse the response
        parsed_response = None if response.status_code == 404 else self._parser(response)

        if parsed_response is None:
            # --
            # The package is not found

            # Try luck with the aux scraper if it is defined
            # --

            parsed_response = super()._auxyliary_search(package_name)

        if parsed_response is None:
            # --
            # The package is not found in the aux scraper either

            # Log the package as not found
            # --

            MyLogger.log(f'Package {package_name} not found')
            MyLogger.log(f'Adding {package_name} to the not found list')
            self.not_found.append(package_name)
            return None


        # If the package is found, log it and return the package data
        MyLogger.log(f'Package {package_name} scraped successfully')
        return parsed_response 


    # Abstract methods
    # ----------------

    # This methods should be implemented in the child class

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
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
    def _parser(self, response: requests.Response) -> Dict:
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
        MyLogger.log(str(self))

    def __str__(self):
        """
        String representation of the exception
        
        Returns
        -------
        str
            String representation of the exception
        """
        return f'ScraperError: {self.message}'
    