'''
File:              cran.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:59:08 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import requests
from bs4 import BeautifulSoup
from typing import Dict, Union, List
from .r import RScraper     
from .scraper import Scraper
from ..requests.request_handler import RequestHandler
from ..util.logger import UtilLogger
from ..util.util import Util

class CranScraper(RScraper, Scraper):
    '''
    Class that scrapes the CRAN website to obtain information about R packages
    '''

    # Class variables
    CRAN_PACKAGE_LIST_URL = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
    CRAN_PACKAGE_DATA_URL = "https://cran.r-project.org/package="

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class
        
        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests

        '''
        super().__init__(rh, 'CRAN')

    """
    Implementation of Scraper.obtain_package_names()
    """
    def obtain_package_names(self) -> List[str]:
        '''
        Get the list of packages in the CRAN repository

        Returns
        -------
        List[str]
            List of packages

        '''

        try:
            response = self.request_handler.do_request(self.CRAN_PACKAGE_LIST_URL)[1]
        except Exception as e:
            UtilLogger.log(f'Exception getting list of packages in CranScraper.obtain_package_names: {e}')
            return []

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get table with packages
        table = soup.find("table")
        rows = table.find_all("tr")
        # Clean the first row of the table (it contains the headers)
        rows.pop(0)

        packages = []

        # We iterate over each row of the table
        for row in rows:

            # We extract the cells of the current row
            cells = row.find_all("td")

            package_name = ""
            # If there are cells in the row
            if cells:
                try: 
                    # We extract the name of the package
                    # The name is in the first cell of the row
                    package_name = cells[0].find("a").text   

                    # We add the package name to the list of packages
                    packages.append(package_name)
                    UtilLogger.log(f'Package {package_name} added to the list of packages')
                   
                # If an error occurs, we show the error message
                except Exception as e:
                    UtilLogger.log(f'Exception getting package name in CranScraper.get_list_of_packages: {e}')
                    continue

        return packages

    """
    Implementation of Scraper.build_urls()
    """
    def build_urls(self, pckg_names: List[str]) -> List[str]:
        '''
        Build the URLs of the packages in the CRAN repository

        Parameters
        ----------
        pckg_names : List[str]
            List of package names

        Returns
        -------
        List[str]
            List of URLs

        '''
        urls = []
        for pckg_name in pckg_names:
            urls.append(self.CRAN_PACKAGE_DATA_URL + pckg_name)
        return urls

    """
    Implementation of Scraper.parser()
    """
    def parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the HTML of a package page in the CRAN website

        Parameters
        ----------
        response : requests.Response
            Response of the HTTP request to the package page

        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package

        '''
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get package name
        name = None
        try:
            d = soup.find('h2').text
            name = Util.clean_string(d).split(':')[0]
        except Exception:
            UtilLogger.log('Package does not have a name')

        # Get package version
        version = None
        try:
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = Util.clean_string(d)
        except Exception:
            UtilLogger.log('Package does not have a version')

        # Get depends
        dep_list = []
        try:
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = Util.clean_string(d)
            dep_list = self.parse_dependencies(depends)
        except Exception:
            UtilLogger.log('Package does not have dependencies')

        # Get imports
        imp_list = []
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = Util.clean_string(d)
            imp_list = self.parse_dependencies(imports)
        except Exception:
            UtilLogger.log('Package does not have imports')

        # Build dictionary with package data
        # we consider that dependencies and imports are the same level of importance
        # so we add them to the same list
        dependencies = list(set(dep_list + imp_list))

        return {
            'name': name,
            'version': version,
            'dependencies': dependencies,
            'url': f'{self.CRAN_PACKAGE_DATA_URL}{name}'
        }

    """
    Implementation of Scraper.scrape_package_data()
    """
    def scrape_package_data(self, pkg_name) -> Union[Dict[str, str], None]:
        '''
        Get data from a CRAN packet.
        It's obtained from the package page in the CRAN website.
        This function has to be called from the get_pkg_data function.
        Obtain the data through HTML scraping on the page, in addition, if any of the optional data is not found, the rest of the data is continued

        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package

        Raises
        ------
        Exception
            If the package is not found or any of the optional data is not found
            If any of the optional data is not found, the scraper will continue handling the rest of the data

        '''

        # Make HTTP request to package page, the package must exist, otherwise an exception is raised
        url = f'{self.CRAN_PACKAGE_DATA_URL}{pkg_name}'
        response = self.request_handler.do_request(url)[1]

        # Check if the package exists
        if response.status_code == 404:
            UtilLogger.log(f'Package {pkg_name} not found')
            return None
            
        # Parse HTML (get data for version, depends and imports)
        UtilLogger.log(f'Parsing HTML of package {pkg_name}')
        data = self.parser(response)

        # Return as dictionary
        UtilLogger.log(f'Package {pkg_name} data ok')
        return {
            'name': pkg_name,
            'version': data['version'],
            'url': url,
            'dependencies': data['dependencies'],
        }
    