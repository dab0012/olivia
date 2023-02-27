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

class Scraper(ABC):

    """
    Abstract class that implements the methods for scraping repositories
    """

    def __init__(self, rh, repo_name):
        self.request_handler = rh
        self.repo_name = repo_name

    @abstractmethod
    def scrape_package(self, pkg_name):
        pass

    def build_list(self, pkg_list):
        packages = []
        for pkg in tqdm.tqdm(pkg_list):
            try:
                package = self.build(pkg)
                packages.append(package)
            except Exception as e:
                logging.error(f'Error scraping package {pkg}: {e}')
        return packages

    # def build_list(self, pkg_list, num_processes=8):
    #     with Pool(num_processes) as pool:
    #         results = []
    #         for pkg in tqdm.tqdm(pkg_list):
    #             result = pool.apply_async(self.build, args=(pkg,))
    #             results.append(result)
    #         packages = [result.get() for result in results]
    #     return packages

    def build(self, pkg_name):
        
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

