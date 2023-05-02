'''
pypi.py
==================

Description
-----------

Module that contains ...

File information:
    - File: pypi.py
    - Project: scrapers
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

import re
import requests
from typing_extensions import override
from bs4 import BeautifulSoup
from ..scraper_ds import ScraperDataSource, ScraperError
from ...myrequests.request_handler import RequestHandler
from ...myrequests.job import RequestJob
from ...utilities.logger import MyLogger



class PypiScraper(ScraperDataSource):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    Implements the abstract class Scraper and accordingly DataSource class
    
    Attributes
    ----------
    NAME : str
        Name of the scraper
    DESCRIPTION : str
        Description of the scraper
    PYPI_PACKAGE_LIST_URL : str
        URL of the PyPI website where the list of packages is located
    PYPI_PACKAGE_DATA_URL : str
        URL of the PyPI website where the data of a package is located
    '''

    # Class variables  
    PYPI_PACKAGE_LIST_URL: str  = "https://pypi.org/simple/"
    PYPI_PACKAGE_DATA_URL: str  = "https://pypi.org/pypi/"
    NAME: str                   = "PyPI Scraper"
    DESCRIPTION: str            = "Scraper class implementation for the PyPI package network."  

    def __init__(self, name: str = NAME, description: str = DESCRIPTION, request_handler: RequestHandler = None):
        '''
        Constructor
        '''

        super().__init__(name, description, request_handler)

    @override
    def obtain_package_names(self) -> list[str]:
        '''
        Obtain the list of packages names from the PyPI website
        Implements the abstract method of DataSource class

        Returns
        -------
        list[str]
            List of packages names
            
        Handles
        -------
        Exception
            If there is an error obtaining the list of packages, it returns an empty list
            
        Example
        -------
        >>> pypi_scraper = PypiScraper()
        >>> pypi_scraper.obtain_package_names()
        ['package1', 'package2', ...]
        '''

        # Build the request job
        job = RequestJob("PYPI package names", self.PYPI_PACKAGE_LIST_URL)

        # Get the HTML of the page
        job = self.request_handler.do_request(job)

        if job.response is None:
            raise ScraperError(f'Error obtaining the list of packages from {self.PYPI_PACKAGE_LIST_URL}')
        
        soup = BeautifulSoup(job.response.text, 'html.parser')
        
        try:
            # Get the list of packages
            pakage_list = [a.text for a in soup.find_all('a')]
        except Exception as e:
            raise ScraperError(f'Error obtaining the list of packages from {self.PYPI_PACKAGE_LIST_URL}') from e
        

        MyLogger().get_logger().info(f'Obtained {len(pakage_list)} packages from {self.PYPI_PACKAGE_LIST_URL}')
        return pakage_list
    
    @override
    def _build_url(self, package_name: str) -> str:
        '''
        Build the URL to scrape a package
        Implements the abstract method of Scraper class
        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        str
            URL to scrape
        '''
        return f'{self.PYPI_PACKAGE_DATA_URL}{package_name}/json'

    @override
    def _parser(self, response: requests.Response) -> dict:
        '''
        Parse the JSON data of a package and return the package data as a dictionary
        
        Parameters
        ----------
        response : requests.Response
            Response of the request to the package data URL
        
        Returns
        -------
        dict
            dictionary with the package data in the following format:
            {
                'name': name: str,
                'version': version: str,
                'url': url: str,
                'dependencies': dependencies: list[str]
            }
        '''
        # Parse the JSON
        data = response.json()

        # Get the dependencies if they exist, build the list of dependencies as Package objects

        dependencies = []
        if data['info']['requires_dist'] is not None:
            dependencies_raw = data['info']['requires_dist']
            
            # Build a dictionary with the dependencies to avoid duplicates with different versions
            dependencies_dict = {}
            
            for dependency in dependencies_raw:
                
                # # Split the dependency in name and version
                # dependency_data = dependency.split(' ')

                # # check if the dependency has a version
                # if len(dependency_data) == 1:
                #     dependencies_dict[dependency_data[0]] = ""
                # else:
                #     # Add the dependency to the dictionary
                #     # dependency_name: dependency_version
                #     dependencies_dict[dependency_data[0]] = dependency_data[1]

                # Get the name of the dependency
                dependency_name = self._clean_name(dependency)
                dependencies_dict[dependency_name] = None
                
            # Build the list of dependencies as dictionaries
            dependencies = [{'name': name, 'version': version} for name, version in dependencies_dict.items()]
            
            
        # Build the dictionary and return it
        return {
            'name': data['info']['name'],
            'version': data['info']['version'],
            'url': data['info']['project_url'],
            'dependencies': dependencies,
        }    

    def _clean_name(self, name: str) -> str:
        '''
        Clean the package name from versions and other characters

        Parameters
        ----------
        name : str
            Name of the package
        
        Returns
        -------
        str
            Cleaned name of the package
            
        '''
        
        regex = re.compile(r'[^\w\d]+')

        # Reemplazar cualquier coincidencia de la expresión regular en la cadena de dependencia con un espacio en blanco
        name = regex.sub(' ', name)

        # Obtenga el primer elemento de la lista resultante después de dividir la cadena por espacios en blanco
        name = name.split()[0]

        return name