'''
File:              pypi.py
Project:           Olivia-Finder
Created Date:      Sunday February 26th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Sunday February 26th 2023 5:20:41 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import requests
from typing_extensions import override
from typing import Dict, List
from bs4 import BeautifulSoup
from olivia_finder.scraping.scraper import Scraper, ScraperError
from olivia_finder.requests.request_handler import RequestHandler

class PypiScraper(Scraper):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    Implements the abstract class Scraper and accordingly DataSource class
    
    Attributes
    ----------
    NAME : str
        Name of the scraper
    DESCRIPTION : str
        Description of the scraper
    PYPI_PACKAGE_LIST_URL : str
        URL of the PyPI website where the list of packages is located
    PYPI_PACKAGE_DATA_URL : str
        URL of the PyPI website where the data of a package is located
    '''

    # Class variables  
    PYPI_PACKAGE_LIST_URL: str  = "https://pypi.org/simple/"
    PYPI_PACKAGE_DATA_URL: str  = "https://pypi.org/pypi/"
    NAME: str                   = "PyPI Scraper"
    DESCRIPTION: str            = "Scraper class implementation for the PyPI package network."  

    def __init__(self, request_handler: RequestHandler = None):
        '''
        Constructor
        '''

        super().__init__(self.NAME, self.DESCRIPTION, request_handler)

    @override
    def obtain_package_names(self) -> List[str]:
        '''
        Obtain the list of packages names from the PyPI website
        Implements the abstract method of DataSource class

        Returns
        -------
        List[str]
            List of packages names
            
        Handles
        -------
        Exception
            If there is an error obtaining the list of packages, it returns an empty list
            
        Example
        -------
        >>> pypi_scraper = PypiScraper()
        >>> pypi_scraper.obtain_package_names()
        ['package1', 'package2', ...]        
        '''
        # Get the HTML of the page
        response = self.request_handler.do_request(self.PYPI_PACKAGE_LIST_URL)[1]
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            # Get the list of packages
            pakage_list = [a.text for a in soup.find_all('a')]
        except Exception as e:
            raise ScraperError(f'Error obtaining the list of packages from {self.PYPI_PACKAGE_LIST_URL}') from e
        
        return pakage_list
    
    @override
    def _build_url(self, pkg_name: str) -> str:
        '''
        Build the URL to scrape a package
        Implements the abstract method of Scraper class
        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        str
            URL to scrape
        '''
        return f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'

    @override
    def _parser(self, response: requests.Response) -> Dict:
        '''
        Parse the JSON data of a package and return the package data as a dictionary
        
        Parameters
        ----------
        response : requests.Response
            Response of the request to the package data URL
        
        Returns
        -------
        Dict
            Dictionary with the package data in the following format:
            {
                'name': name: str,
                'version': version: str,
                'url': url: str,
                'dependencies': dependencies: List[str]
            }
        '''
        # Parse the JSON
        data = response.json()

        # Get the dependencies if they exist, build the list of dependencies as Package objects
        # TODO: The parser should return a list of strings with the dependencies names, not Package objects

        dependencies = []
        if data['info']['requires_dist'] is not None:
            dependencies_raw = data['info']['requires_dist']
            
            # Build a dictionary with the dependencies to avoid duplicates with different versions
            dependencies_dict = {}
            
            for dependency in dependencies_raw:
                
                # Split the dependency in name and version
                dependency_data = dependency.split(' ')
                dependencies_dict[dependency_data[0]] = dependency_data[1]
                
            # Build the list of dependencies as dictionaries
            dependencies = [{'name': name, 'version': version} for name, version in dependencies_dict.items()]
            
            
        # Build the dictionary and return it
        return {
            'name': data['info']['name'],
            'version': data['info']['version'],
            'url': data['info']['project_url'],
            'dependencies': dependencies,
        }    
