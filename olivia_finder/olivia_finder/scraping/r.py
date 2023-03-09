'''
File:              r.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 7:01:45 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import re
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from ..package import Package
from ..requests.request_handler import RequestHandler
from .scraper import Scraper
from ..util.logger import UtilLogger

class RScraper(Scraper, ABC):
    '''
    Abstract class that implements the common methods for scraping R repositories
    '''

    def __init__(self, name: str = None, description:str = None, request_handler: RequestHandler = None, use_logger: bool = False):
        '''
        Constructor

        ---
        Parameters
        -   name: str                           -> Name of the data source
        -   description: str                    -> Description of the data source
        -   request_handler: RequestHandler     -> Object to perform the requests
        '''

        # Call the super constructor
        super().__init__(name, description, request_handler, use_logger)

    def parse_dependencies(self, dependencies_str) -> List[Dict[str, str]]:
        '''
        Parse the dependencies string and return a list of tuples with the name and version of each dependency

        ---
        Parameters
        -   dependencies_str: str -> String

        ---
        Returns
        -   List[Dict[str, str]] -> List of dictionaries with the name and version of each dependency
        '''

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else '' for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', nombre.strip()) for nombre in dependencies_str.split(",")]

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or len(names) == 0:
            UtilLogger.log(f'Error parsing dependencies in RScraper.__parse_dependencies: {names} {versions}')
            return []

        # Return list of dependency dictionaries
        dependencies = []
        for i in range(len(names)):
            dependencies.append({
                'name': names[i],
                'version': versions[i]
            })

        return dependencies

    @abstractmethod
    def obtain_package_names(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def build_urls(self, pckg_names: List[str]) -> List[str]:
        pass

    @abstractmethod
    def parser(self, response) -> Dict[str, str]:
        pass

    @abstractmethod
    def scrape_package_data(self, pkg_name) -> Dict[str, str]:
        pass
