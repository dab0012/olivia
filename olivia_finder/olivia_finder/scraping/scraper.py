""""""
'''
·········································································
File: scraper.py
Project: Olivia-Finder
Created Date: Friday February 24th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''

import requests, tqdm
from typing_extensions import override
from typing import Dict, List, Optional, Tuple
from abc import abstractmethod
from olivia_finder.data_source import DataSource
from olivia_finder.myrequests.request_handler import RequestHandler
from olivia_finder.util.logger import UtilLogger


class Scraper(DataSource):
    """
    Abstract class that implements the methods for scraping a package manager
    
    Attributes
    ----------
    request_handler : RequestHandler
        Request handler for the scraper
        
    Parameters
    ----------
    name : Optional[str]
        Name of the data source
    description : Optional[str]
        Description of the data source
    request_handler : Optional[RequestHandler]
        Request handler for the scraper, if None, it will be initialized with a generic RequestHandler
    """
    
    # Attributes
    # ----------
    request_handler: RequestHandler

    def __init__(
        self, 
        name: Optional[str] = None, 
        description: Optional[str] = None, 
        request_handler: Optional[RequestHandler] = None, 
    ):
        """
        Constructor of the class
        """

        # Call the super constructor
        super().__init__(name, description)

        # if request_handler is None build a generic RequestHandler
        if request_handler is None:
            self.request_handler = RequestHandler()
        else:
            self.request_handler: request_handler

        # Initialize the not_found list for storing the packages that are not found
        self.not_found = []

    #region Private methods

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
    
    @abstractmethod
    def _build_url(self, package_name: str) -> str:
        '''
        Build the url for scraping the package
        To be implemented by the child class
        '''
        pass
        
    @abstractmethod 
    def _parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the response from the request, it should return a dictionary with the package data
        as string values.
        This method is called by the scrape_package_data of the child class.
        It has to handle th data source specific format (e.g. html, json, etc.)
        The format of the dictionary should be:
        {
            'name': str,
            'description': str,
            'version': str,
            'url': str,
            'dependencies': list[str]
        }
        or None if the package is not found or an error occurs
        To be implemented by the child class
        '''
        pass
    
    #endregion

    #region Public methods
    
    @override
    def obtain_package_data(self, package_name: str, override_previous: Optional[bool] = False ) -> Dict:
        """
        Scrape a package from a package manager, if the package is not found, it is added to the not_found list
        Implements the abstract method of the DataSource class
        
        Parameters
        ----------
        pkg_name : str
            Name of the package to scrape

        Returns
        -------
        Dict
            Package data as a dictionary, if the package is not found, it returns None
            
        Examples
        --------
        >>> scraper = Scraper()
        >>> scraper.obtain_package_data('numpy')
        """
        
        # Get the package page
        UtilLogger.log(f'Scraping package {package_name}')
        response = self.request_handler.do_request(
            self._build_url(package_name)
        )[1]

        # Return None if the package is not found, otherwise return the package data
        parsed_response = None if response.status_code == 404 else self._parser(response)

        if parsed_response is None:
            raise ScraperError(f'Package {package_name} not found')
        
        UtilLogger.log(f'Package {package_name} scraped successfully')
            
        return parsed_response 

    @override
    def obtain_packages_data(
        self, 
        package_names:  Optional[List[str]] = None,
        progress_bar:   Optional[tqdm.tqdm] = None,
        full_scrape:    Optional[bool] = False
    ) -> Tuple[List[Dict], List[str]]:
        '''
        Scrape a list of packages from a package manager, if the package is not found, it is added to the not_found list
        Implements the abstract method of the DataSource class

        Parameters
        ----------
        package_names : list[str], optional
            List of package names to scrape, by default None
        progress_bar : tqdm.tqdm, optional
            Progress bar for visualizing the progress, by default None
        full_scrape : bool, optional
            If True, it tries to scrape all the packages obtainig the package names from the data source, by default False
            Only works if package_names is None
    
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
            if not full_scrape:
                raise ScraperError('package_names is None or empty and full_scrape is disabled')
            UtilLogger.log(f'Obtaining package names from Scraper: {self.name}, {self.description}')
            package_names = self.obtain_package_names()
        else:
            UtilLogger.log('Using package names from param list')

        # Build the urls
        UtilLogger.log('Building urls')
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
                UtilLogger.log(f'Package {not_found_name} not found, status code: {response.status_code}, url: {key_url}, skipping...')
                continue

            # Parse the source data and add it to the list
            packages.append(self._parser(response))

        return packages, not_found

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        '''
        Obtain the package names from the web page of the package manager
        it must handle exceptions and return an empty list if the package names cannot be obtained
        To be implemented by the child class
        '''
        pass
    
    #endregion

class ScraperError(Exception):
    """
    Exception for the Scraper class
    
    Attributes
    ----------
    message : str
        Message of the exception
    """
    
    def __init__(self, message: str = ''):
        '''Constructor'''
        
        
        self.message = message
        UtilLogger.log(str(self))

    def __str__(self):
        """
        String representation of the exception
        
        Returns
        -------
        str
            String representation of the exception
        """
        return (f'ScraperError: {self.message}')
    