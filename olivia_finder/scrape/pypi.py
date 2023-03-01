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

import logging
from typing import Dict, Union
from bs4 import BeautifulSoup
import requests
import tqdm
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.scraper import Scraper
from olivia_finder.package import Package

class PypiScraper(Scraper):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    '''

    # Class variables
    PYPI_PACKAGE_LIST_URL = "https://pypi.org/simple/"
    PYPI_PACKAGE_DATA_URL = "https://pypi.org/pypi/"    # PYPI_PACKAGE_DATA_URL = "https://pypi.org/pypi/{package_name}/json"

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class
        
        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests

        '''
        super().__init__(rh, 'PyPI')
        self.not_found = []

    def parse_json(self, response: requests.Response) -> Dict[str, str]:
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

    def scrape_package(self, pkg_name) -> Union[Dict[str, str], None]:

        # Get the package page
        url = f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'
        url_, response = self.request_handler.do_request(url)

        # Check if the package exists
        if response.status_code == 404:
            return None

        # Parse the JSON
        return self.parse_json(response)

    def scrape_package_list(self, pkg_list: list, progress_bar: tqdm.tqdm = None) -> list:
        '''
        Scrape a list of packages with the RequestHandler multiprocessing capabilities

        Parameters
        ----------
        pkg_list : list
            List of packages to scrape

        Returns
        -------
        list
            List of scraped packages

        '''
        # Get the list of requests to do
        urls = []
        for pkg_name in pkg_list:
            url = f'{self.PYPI_PACKAGE_DATA_URL}{pkg_name}/json'
            urls.append(url)

        # Do the requests with the RequestHandler parallelly
        responses = self.request_handler.do_parallel_requests(urls, progress_bar=progress_bar)

        # Parse the responses
        packages = []
        for key_url in responses.keys():

            response = responses[key_url]

            # Check if the package exists
            if response.status_code == 404:

                # log the error url
                logging.error(f'Package {key_url} not found in {self.name}') 
                self.not_found.append(pkg_name)
                continue

            # Parse the JSON
            package_data = self.parse_json(response)
            packages.append(package_data)

        return packages
        
    
    def get_list_of_packages(self) -> list:
        '''
        Get the list of packages from the PyPI website

        Returns
        -------
        list
            List of packages

        '''
        # Get the HTML
        url_, response = self.request_handler.do_request(self.PYPI_PACKAGE_LIST_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the list of packages
        packages = []
        for a in soup.find_all('a'):
            packages.append(a.text)

        return packages

