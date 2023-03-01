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
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from olivia_finder.package import Package
from olivia_finder.scrape.scraper import Scraper
from olivia_finder.scrape.requests.request_handler import RequestHandler

class RScraper(Scraper, ABC):
    '''
    Abstract class that implements the methods for scraping R repositories
    '''

    def __init__(self, rh: RequestHandler, repo) -> None:

        self.request_handler = rh
        self.repo_name = repo

    def parse_dependencies(self, dependencies_str) -> List[Tuple[str, str]]:

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else '' for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', nombre.strip()) for nombre in dependencies_str.split(",")]

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or len(names) == 0:
            logging.error(f'Error parsing dependencies in RScraper.__parse_dependencies: {names} {versions}')
            return []

        dependencies = []
        # Return list of dependency objects
        for i in range(len(names)):
            d = Package(
                repo=self.repo_name,
                name=names[i],
                version=versions[i]
            )
            dependencies.append(d)

        return dependencies

    @abstractmethod
    def scrape_package(self, pkg_name) -> Dict[str, str]:
        pass

    @abstractmethod
    def scrape_package_list(self, pkg_list, progress_bar) -> List[Package]:
        pass
