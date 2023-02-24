# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: Olivia Finder
# Description: Class that implmenets the RScraper abstract class for scraping the R repositories

import re
from typing             import Dict, List, Tuple
from abc                import ABC, abstractmethod

# Own modules
from ...LoadConfig      import logging
from ...Util            import print_colored, GREEN, RED, YELLOW
from ...ProxyRequest    import RequestHandler
from ..RPackage         import RPackage
from ..RDependency      import RDependency


class RScraper(ABC):
    '''
    Abstract class that implements the methods for scraping R repositories
    '''

    def __init__(self, rh: RequestHandler) -> None:
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

        self.request_handler = rh

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

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or len(names) == 0:
            logging.error(f'Error parsing dependencies in RScraper.__parse_dependencies: {names} {versions}')
            return []

        dependencies = []
        # Return list of dependency objects
        for i in range(len(names)):
            d = RDependency(names[i], type, versions[i])
            dependencies.append(d)

        return dependencies

    @abstractmethod
    def scrape_package(self, pkg_name) -> Dict[str, str]:
        pass

    def build_list(self, pkg_list: List[str]) -> List[RPackage]:
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
                error_packages.append(pkg_name)
                logging.error(f'Exception scraping package {pkg_name} in RScraper.scrape_list: {e}')
                logging.error(f'Error packages: {error_packages}')

        # Try to scrape error packages
        while len(error_packages) > 0:
            count = 0
            for pkg_name in error_packages:
                try:
                    packages.append(self.build(pkg_name))
                    error_packages.remove(pkg_name)
                    print_colored(f'Scraped package {pkg_name}: {count}/{len(error_packages)}', GREEN)
                except Exception as e:
                    logging.error(f'Exception scraping package {pkg_name} in RScraper.scrape_list: {e}')
                    logging.error(f'Error packages: {error_packages}')

        # Return list of packages
        return packages

    def build(self, pkg_name) -> RPackage:
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
                logging.error(f'Exception parsing dependencies of package {pkg_name}: {e}')
                dep_list = []

        # Set package attributes
        package = RPackage()
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