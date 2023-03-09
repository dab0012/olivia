'''
File:              scraper.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:39:40 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import requests, tqdm
from typing_extensions import override
from typing import Dict, List, Union
from abc import abstractmethod
from ..data_source import DataSource
from ..requests.request_handler import RequestHandler
from ..util import UtilLogger

class Scraper(DataSource):
    """
    Abstract class that implements the methods for scraping repositories
    """

    # Attributes
    # ----------
    request_handler: RequestHandler
    not_found: List[str]

    def __init__(self, name: str = None, description:str = None, request_handler: RequestHandler = None, use_logger: bool = False):
        """
        Constructor

        ---
        Parameters
        -   name: str                           -> Name of the data source
        -   description: str                    -> Description of the data source
        -   request_handler: RequestHandler     -> Object to perform the requests
        """

        # if request_handler is None build a generic RequestHandler
        if request_handler is None:
            self.request_handler = RequestHandler()
        else:
            self.request_handler: request_handler

        # Initialize the not_found list for storing the packages that are not found
        self.not_found = []

        # Call the super constructor
        super().__init__(name, description, use_logger)

    # Overrided methods
    # -----------------
    @override
    def obtain_package_data(self, pkg_name: str) -> Dict:
        """
        Scrape a package from a package manager
        -   Implements :func:`DataSource.obtain_package_data`

        ---
        Parameters
        -   pkg_name: str -> Name of the package

        ---
        Returns
        -   Dict -> Package data
        """
        UtilLogger.log(f'Scraping package {pkg_name}')
        pkg_data = self.scrape_package_data(pkg_name)
        return pkg_data

    @override 
    def obtain_packages_data(self, pckg_names: list[str] = None, progress_bar: tqdm.tqdm = None) -> List[Dict]:
        '''
        Scrape a list of packages from a package manager
        -   Implements :func:`DataSource.obtain_packages_data`

        ---
        Parameters
        -   pckg_names: list[str]  -> List of package names
        -   progress_bar: tqdm.tqdm -> Progress bar

        ---
        Returns
        -   List[Dict] -> List of package data
        '''

        # If pckg_names is None, obtain the package names from the data source
        if pckg_names is None:
            UtilLogger.log(f'Obtaining package names from Scraper: {self.name}, {self.description}')
            pckg_names = self.obtain_package_names()
        else:
            UtilLogger.log(f'Using package names from param list')

        # Build the urls
        UtilLogger.log(f'Building urls')
        urls = self.build_urls(pckg_names)

        # Do the requests with the RequestHandler parallelly
        responses = self.request_handler.do_parallel_requests(urls, progress_bar=progress_bar)

        # Parse the responses
        packages = []
        for key_url in responses.keys():
            response = responses[key_url]

            # Check if the package exists
            if response.status_code == 404:
                UtilLogger.log(f'Package {key_url} not found')
                continue

            # Parse the soruce data
            package_data = self.parser(response)
            packages.append(package_data)

        return packages

    # Methods to be implemented by the subclasses
    # -------------------------------------------

    @abstractmethod
    def build_urls(self, pckg_names: List[str]) -> List[str]:
        pass

    @abstractmethod 
    def parser(self, response: requests.Response) -> Dict[str, str]:
        pass

    @abstractmethod
    def scrape_package_data(self, pkg_name: str) -> Union[Dict[str, str], None]:
        pass

class ScraperError(Exception):
    """
    Exception for the Scraper class
    """
    
    def __init__(self, message: str):
        '''
        Constructor
        
        ---
        Parameters
        -   message: str -> Error message
        '''
        self.message = message
        UtilLogger.log(f'ScraperError: {message}')

    def __str__(self):
        return self.message