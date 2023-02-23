# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA


import re
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from modules.Util import *
from modules.Package import Package
from modules.Dependency import Dependency
from modules.scraping.ProxyRequest import RequestHandler

class Scraper(ABC):

    def __init__(self, request_handler: RequestHandler) -> None:
        '''
        Class constructor
        
        Parameters
        ----------
        request_handler : RequestHandler
            Request handler object
            
        Returns
        -------
            None
        '''

        self.request_handler = request_handler

    def __parse_dependencies(self, dependencies_str, type) -> List[Tuple[str, str]]:
        '''
        Parse dependencies data and handle exceptions

        Parameters
        ----------
        dependencies_str : str
            String with dependencies data
        type : str
            Type of dependency

        Returns
        List[Tuple[str, str]]
            List of dependencies
        '''

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else '' for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', nombre.strip()) for nombre in dependencies_str.split(",")]

        dependencies = []
        # Return list of dependency objects
        for i in range(len(names)):
            d = Dependency(names[i], type, versions[i])
            dependencies.append(d)

        return dependencies

    @abstractmethod
    def scrape_package(self, pkg_name) -> Dict[str, str]:
        pass

    def build_list(self, pkg_list: List[str]) -> List[Package]:
        '''
        Scrape a list of packages

        Parameters
        ----------
        pkg_list : List[str]
            List of packages to scrape

        Returns
        -------
        List[Package]
            List of scraped packages
        '''

        # Scrape packages
        packages = []
        total = len(pkg_list)
        count = 0

        # Error packages while scraping
        error_packages = []

        # Incluir una barra de progreso con tqdm
        for pkg_name in pkg_list:
            count += 1
            try:
                packages.append(self.build(pkg_name))
                print_colored(f'Scraped package {pkg_name}: {count}/{total}', GREEN)

            except Exception as e:
                print_colored(f'Exception scraping package {pkg_name} in BioconductorScraper.scrape_list: {e}', 'red')
                error_packages.append(pkg_name)
                print_colored(f'Error packages: {error_packages}', 'red')
                pass

        # Try to scrape error packages
        while len(error_packages) > 0:
            count = 0
            for pkg_name in error_packages:
                try:
                    packages.append(self.build(pkg_name))
                    error_packages.remove(pkg_name)
                    print_colored(f'Scraped package {pkg_name}: {count}/{len(error_packages)}', GREEN)
                except Exception as e:
                    print_colored(f'Exception scraping package {pkg_name} in BioconductorScraper.scrape_list: {e}', 'red')
                    print_colored(f'Error packages: {error_packages}', 'red')
                    pass

        # Return list of packages
        return packages

    def build(self, pkg_name) -> Package:
        '''
        Build a Package object with the data of the scraped package

        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        Package
            Package object with the data of the scraped package
        ''' 

        # Get package data from HTML scraping
        pkg_data = self.scrape_package(pkg_name)

        # Parse dependencies data and handle exceptions
        dep_list = []
        for dep_type in ['depends', 'imports']:
            try:
                dep_str = pkg_data.get(dep_type)
                if dep_str:
                    dep_list += self.__parse_dependencies(pkg_data.get(dep_type), dep_type)
            except Exception as e:
                dep_list = []

        # Set package attributes
        package = Package()
        package.name = pkg_name
        package.description = pkg_data['description']
        package.version = pkg_data['version']
        package.publication_date = pkg_data['publication_date']
        package.author_data = pkg_data['authors']
        package.mantainer = pkg_data['mantainer']
        package.license = pkg_data['license']
        package.requires_compilation = pkg_data['requires_compilation']
        package.dependencies = dep_list
        package.url = pkg_data['url']
        package.in_cran = pkg_data['source'] == 'CRAN'
        package.in_bioc = pkg_data['source'] == 'Bioconductor'

        # Return package
        return package