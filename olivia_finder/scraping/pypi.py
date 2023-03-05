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
from typing import Dict, Union
from bs4 import BeautifulSoup
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.scraping.scraper import Scraper
from olivia_finder.package import Package
from olivia_finder.util import UtilLogger

class PypiScraper(Scraper):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    '''

    # Class variables
    PYPI_PACKAGE_LIST_URL = "https://pypi.org/simple/"
    PYPI_PACKAGE_DATA_URL = "https://pypi.org/pypi/"    
    
    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class
        
        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests

        '''
        super().__init__(rh, 'PyPI')

    """
    Implementation of Scraper.obtain_package_names()
    """
    def obtain_package_names(self) -> list:
        '''
        Get the list of packages from the PyPI website

        Returns
        -------
        list
            List of packages

        '''
        # Get the HTML of the page
        response = self.request_handler.do_request(self.PYPI_PACKAGE_LIST_URL)[1]
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the list of packages
        packages = []
        for a in soup.find_all('a'):
            packages.append(a.text)

        return packages
    
    """ 
    Implementation of Scraper.bulid_urls()
    """ 
    def build_urls(self, pkg_list: list) -> list:
        '''
        Build the list of URLs to scrape

        Parameters
        ----------
        pkg_list : list
            List of packages to scrape

        Returns
        -------
        list
            List of URLs to scrape

        '''
        urls = []
        for pkg_name in pkg_list:
            url = f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'
            urls.append(url)

        return urls

    """
    Implementation of Scraper.parser()
    """
    def parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the JSON data of a package

        Parameters
        ----------
        data : dict
            JSON data of the package

        Returns
        -------
        dict
            Dictionary with the name, version, url and dependencies of the package

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

    """
    Implementation of Scraper.scrape_package_data()
    """
    def scrape_package_data(self, pkg_name) -> Union[Dict[str, str], None]:

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

