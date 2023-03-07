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
from olivia_finder.data_source import DataSource
from olivia_finder.package import Package
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.util import UtilLogger

class Scraper(DataSource):
    """
    Abstract class that implements the methods for scraping repositories
    """

    def __init__(self, request_handler, repo_name):

        self.request_handler: RequestHandler = request_handler
        self.repo_name = repo_name
        self.not_found = []

    # Overrided methods
    # -----------------

    @override # from DataSource
    def obtain_package(self, pkg_name) -> Package:
    
        # Get package data from HTML scraping
        UtilLogger.log(f'Scraping package {pkg_name}')
        pkg_data = self.scrape_package_data(pkg_name)

        if not pkg_data:
            UtilLogger.log(f'Error scraping package {pkg_name}')
            return None

        return Package(
                name=pkg_name,
                version=pkg_data.get('version'),
                url=pkg_data.get('url'),
                dependencies=pkg_data.get('dependencies'))

    @override # from DataSource
    def obtain_dependency_network(self, pckg_names: list, pb: tqdm.tqdm) -> List[Package]:
        '''
        Build a list of Package objects from a list of package names

        Parameters
        ----------
        pckg_names : list
            List of package names
        pb : tqdm.tqdm
            Progress bar

        Returns
        -------
        list
            List of Package objects
        '''

        # Build the urls
        urls = self.build_urls(pckg_names)

        # Do the requests with the RequestHandler parallelly
        responses = self.request_handler.do_parallel_requests(urls, progress_bar=pb)

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

            # Build the Package object
            p = Package(
                name=package_data.get('name'),
                version=package_data.get('version'),
                url=package_data.get('url'),
                dependencies=package_data.get('dependencies'))

            packages.append(p)

        return packages

    # Methods to be implemented by the subclasses
    # -------------------------------------------

    @abstractmethod # from DataSource
    def obtain_package_names(self) -> List[dict]:
        pass

    @abstractmethod # from DataSource
    def build_urls(self, pckg_names: list) -> List[str]:
        pass

    @abstractmethod 
    def parser(self, response: requests.Response) -> Dict[str, str]:
        pass

    @abstractmethod
    def scrape_package_data(self, pkg_name) -> Union[Dict[str, str], None]:
        pass