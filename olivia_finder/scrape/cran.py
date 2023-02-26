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

from olivia_finder.util import Util
from bs4 import BeautifulSoup
from typing import Dict, Union, List
import logging
from olivia_finder.scrape.r import RScraper                                         
from olivia_finder.scrape.requests.request_handler import RequestHandler


class CranScraper(RScraper):
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

    def scrape_package(self, pkg_name) -> Union[Dict[str, str], None]:
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
        try:
            response = self.request_handler.do_request(url)

            # Check if the package exists
            if response.status_code == 404:
                logging.error(f'Package {pkg_name} not found in CranScraper.__parse_pkg_data')
                return None
            
        except Exception as e:
            logging.error(f'Exception getting package {pkg_name} in CranScraper.__parse_pkg_data: {e}')
            return None

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get package version
        version = None
        try:
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = Util.clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have a version')

        # Get depends
        depends = None
        dep_list = []
        try:
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = Util.clean_string(d)
            dep_list = self.parse_dependencies(depends)
        except Exception:
            logging.info(f'Package {pkg_name} does not have dependencies')

        # Get imports
        imports = None
        imp_list = []
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = Util.clean_string(d)
            imp_list = self.parse_dependencies(imports)
        except Exception:
            logging.info(f'Package {pkg_name} does not have imports')

        # Build dictionary with package data
        return {
            'name': pkg_name,
            'version': version,
            'url': url,
            'dependencies': dep_list + imp_list,
        }

    def get_list_of_packages(self) -> List[str]:
        '''
        Get the list of packages in the CRAN repository

        Returns
        -------
        List[str]
            List of packages

        '''

        try:
            response = self.request_handler.do_request(self.CRAN_PACKAGE_LIST_URL)
        except Exception as e:
            logging.error(f'Exception getting list of packages in CranScraper.get_list_of_packages: {e}')
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
                    logging.info(f'Package {package_name} added to the list of packages')
                   
                # If an error occurs, we show the error message
                except Exception as e:
                    logging.warning(f'Exception getting package name in CranScraper.get_list_of_packages: {e}')
                    continue

        return packages
