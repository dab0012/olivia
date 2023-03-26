from abc import ABC, abstractmethod
from typing import Dict, List
from .data_source import DataSource

class ScraperABC(DataSource, ABC):
    """
    Abstract class that implements the methods for scraping a package manager
    """
    
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

