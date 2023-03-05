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

import logging, requests, tqdm
from typing import List
from abc import ABC, abstractmethod
from olivia_finder.package import Package
from olivia_finder.requests.request_handler import RequestHandler

class Scraper(ABC):

    """
    Abstract class that implements the methods for scraping repositories
    """

    def __init__(self, rh, repo_name):
        self.request_handler: RequestHandler = rh
        self.repo_name = repo_name
        self.not_found = []
        self.LOGGER = rh.LOGGER

    @abstractmethod
    def obtain_package_names(self) -> List[dict]:
        pass

    @abstractmethod
    def build_urls(self, pckg_names: list) -> List[str]:
        pass

    @abstractmethod
    def parser(self, response: requests.Response) -> dict:
        pass

    @abstractmethod
    def scrape_package_data(self, pkg_name) -> dict:
        pass

    def build_obj(self, pkg_name) -> Package:
        '''
        Build a Package object from a package name

        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        Package
            Package object
        '''
        
        # Get package data from HTML scraping
        pkg_data = self.scrape_package_data(pkg_name)

        if not pkg_data:
            logging.error(f'Error scraping package {pkg_name}')
            return None

        return Package(
                repo=self.repo_name,
                name=pkg_name,
                version=pkg_data.get('version'),
                url=pkg_data.get('url'),
                dependencies=pkg_data.get('dependencies'))

    def build_obj_list(self, pckg_names: list, pb: tqdm.tqdm) -> list:
        '''
        Build a list of Package objects from a list of urls

        Parameters
        ----------
        urls : list
            List of urls to scrape
        parse_source : function
            Function to parse the source of the url

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
                logging.error(f'Package {key_url} not found')
                continue

            # Parse the soruce data
            package_data = self.parser(response)

            # Build the Package object
            p = Package(
                repo=self.repo_name,
                name=package_data.get('name'),
                version=package_data.get('version'),
                url=package_data.get('url'),
                dependencies=package_data.get('dependencies'))

            packages.append(p)

        return packages
