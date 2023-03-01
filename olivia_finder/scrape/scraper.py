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

import logging
from abc import ABC, abstractmethod
from multiprocessing import Pool
from olivia_finder.package import Package
import tqdm

from olivia_finder.scrape.requests.request_handler import RequestHandler

class Scraper(ABC):

    """
    Abstract class that implements the methods for scraping repositories
    """

    def __init__(self, rh, repo_name):
        self.request_handler: RequestHandler = rh
        self.repo_name = repo_name

    @abstractmethod
    def scrape_package(self, pkg_name):
        pass

    @abstractmethod
    def scrape_package_list(self, pkg_list, progress_bar):
        pass

    def build_obj_list(self, pkg_list):
        '''
        Build a list of Package objects from a list of package names
        
        Parameters
        ----------
        pkg_list : list
            List of package names
                
        Returns
        -------
        list
            List of Package objects
        '''
        
        pb = tqdm.tqdm(total=len(pkg_list), desc='Scraping packages')
        package_list = self.scrape_package_list(pkg_list, progress_bar=pb)
        pb.close()

        return package_list


    def build_obj(self, pkg_name):
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
        pkg_data = self.scrape_package(pkg_name)

        if not pkg_data:
            logging.error(f'Error scraping package {pkg_name}')
            return None

        return Package(
                repo=self.repo_name,
                name=pkg_name,
                version=pkg_data.get('version'),
                url=pkg_data.get('url'),
                dependencies=pkg_data.get('dependencies'))

