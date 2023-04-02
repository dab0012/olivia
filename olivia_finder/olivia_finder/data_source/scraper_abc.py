'''
scraper_abc.py
==================

Description
-----------

Module that contains ...

File information:
    - File: scraper_abc.py
    - Project: data_source
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

from abc import ABC, abstractmethod
from typing import Dict, List

import requests
from .data_source import DataSource

class ScraperABC(DataSource, ABC):
    """
    Abstract class that implements the methods for scraping a package manager
    """
    
    @abstractmethod
    def _build_url(self, package_name: str) -> str:
        '''
        Build the url for scraping the package

        Parameters
        ----------
        package_name : str
            Name of the package to scrape
        
        Returns
        -------
        str
            Url for scraping the package
        '''
    
    @abstractmethod
    def _build_urls(self, package_names: List[str]) -> List[str]:
        '''
        Build the urls for scraping the packages

        Parameters
        ----------
        package_names : List[str]
            List of package names to scrape
        
        Returns
        -------
        List[str]
            List of urls for scraping the packages
        '''
    
    @abstractmethod 
    def _parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the response from the request, it should return a dictionary with the package data
        as string values.

        Parameters
        ----------
        response : requests.Response
            Response of the request to the package data URL
        
        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package as key-value pairs
        '''
