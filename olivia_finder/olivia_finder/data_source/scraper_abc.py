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

from abc import ABC, abstractmethod
from typing import Dict, List
from typing_extensions import override
from olivia_finder.data_source.data_source_abc import DataSourceABC

class ScraperABC(DataSourceABC, ABC):
    """
    Abstract class that implements the methods for scraping a package manager
    """
        
    def obtain_package_data(self) -> Dict[str, str]:
        '''
        Scrape a package from a package manager, if the package is not found, it is added to the not_found list
        Implements the abstract method of the DataSource class
        
        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package as key-value pairs
        '''
        pass 

    def obtain_packages_data(self) -> List[Dict[str, str]]:
        '''
        Scrape a list of packages from a package manager, if the package is not found, it is added to the not_found list
        Implements the abstract method of the DataSource class
        
        Returns
        -------
        List[Dict[str, str]]
            List of dictionaries with the data of the packages as key-value pairs
        '''
        pass

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        '''
        Obtain the package names from the web page of the package manager
        it must handle exceptions and return an empty list if the package names cannot be obtained
        To be implemented by the child class
        
        Returns
        -------
        List[str]
            List of package names
        '''
        pass

    @abstractmethod
    def _build_url(self) -> str:
        '''
        Build the url for scraping the package
        
        Returns
        -------
        str
            Url for scraping the package
        '''
        pass
    
    @abstractmethod
    def _build_urls(self) -> List[str]:
        '''
        Build the urls for scraping the packages
        
        Returns
        -------
        List[str]
            List of urls for scraping the packages
        '''
        pass
    
    @abstractmethod 
    def _parser(self) -> Dict[str, str]:
        '''
        Parse the response from the request, it should return a dictionary with the package data
        as string values.
        
        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package as key-value pairs
        '''
        pass