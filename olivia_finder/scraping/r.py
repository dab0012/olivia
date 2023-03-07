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
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.scraping.scraper import Scraper

class RScraper(Scraper, ABC):
    '''
    Abstract class that implements the common methods for scraping R repositories
    '''

    def __init__(self, rh: RequestHandler, repo: str) -> None:
        super().__init__(rh, repo)

    def parse_dependencies(self, dependencies_str) -> List[Tuple[str, str]]:

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else '' for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', nombre.strip()) for nombre in dependencies_str.split(",")]

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or len(names) == 0:
            UtilLogger.log(f'Error parsing dependencies in RScraper.__parse_dependencies: {names} {versions}')
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
