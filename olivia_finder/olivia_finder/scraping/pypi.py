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
from typing import Dict, List, Union
from bs4 import BeautifulSoup
from .scraper import Scraper
from ..requests.request_handler import RequestHandler
from ..package import Package
from ..util.logger import UtilLogger

class PypiScraper(Scraper):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    Implements the abstract class Scraper and accordingly DataSource class
    '''

    # Class variables
    NAME: str                   = "PyPI Scraper"
    DESCRIPTION: str            = "Scraper class implementation for the PyPI package network."    
    PYPI_PACKAGE_LIST_URL: str  = "https://pypi.org/simple/"
    PYPI_PACKAGE_DATA_URL: str  = "https://pypi.org/pypi/"

    def __init__(self, request_handler: RequestHandler = None):
        '''
        Constructor

        ---
        Parameters
        -   request_handler: RequestHandler -> Object to perform the requests
        '''

        super().__init__(self.NAME, self.DESCRIPTION, request_handler)

    @override
    def obtain_package_names(self) -> List[str]:
        '''        
        Get the list of packages names from the PyPI website
        -   Implements :func:`DataSource.obtain_package_names`

        ---
        Returns
        -   List[str] -> List of packages names
        '''
        # Get the HTML of the page
        response = self.request_handler.do_request(self.PYPI_PACKAGE_LIST_URL)[1]
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the list of packages
        packages = []
        for a in soup.find_all('a'):
            packages.append(a.text)

        return packages
    
    @override
    def build_urls(self, pkg_list: List[str]) -> List[str]:
        '''
        Build the list of URLs to scrape
        -   Implements :func:`Scraper.build_urls`

        ---
        Parameters
        -   pkg_list: List[str] -> List of packages names

        ---
        Returns
        -   List[str] -> List of URLs to scrape
        '''
        urls = []
        for pkg_name in pkg_list:
            url = f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'
            urls.append(url)

        return urls

    @override
    def parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the JSON data of a package
        -   Implements :func:`Scraper.parser`

        ---
        Parameters
        -   response: requests.Response -> Response of the request

        ---
        Returns
        -   Dict[str, str] -> Dictionary with the package data

        '''
        # Parse the JSON
        data = response.json()

        # Get the dependencies if they exist
        dependencies = []
        if data['info']['requires_dist'] is not None:
            for dependency in data['info']['requires_dist']:
                dep_name = dependency.split(' ')[0]
                d = Package("PyPI", dep_name)
                dependencies.append(d) 

        name = data['info']['name']
        version = data['info']['version']
        url = data['info']['project_url']

        # Get the package data
        package_data = {
            'name': name,
            'version': version,
            'url': url,
            'dependencies': dependencies
        }

        return package_data    

    @override
    def scrape_package_data(self, pkg_name: str) -> Union[Dict[str, str], None]:
        '''
        Scrape the data of a package
        -   Implements :func:`Scraper.scrape_package_data`

        ---
        Parameters
        -   pkg_name: str -> Name of the package to scrape

        ---
        Returns
        -   Union[Dict[str, str], None] -> Dictionary with the package data or None if the package doesn't exist
        '''

        # Get the package page
        url = f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'
        response = self.request_handler.do_request(url)[1]

        # Check if the package exists
        if response.status_code == 404:
            self.not_found.append(pkg_name)
            UtilLogger.log(f'Package {pkg_name} not found in {self.name}')
            return None

        # Parse the JSON
        return self.parser(response)

