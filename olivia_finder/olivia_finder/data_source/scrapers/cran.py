'''
cran.py
==================

Description
-----------

Module that contains ...

File information:
    - File: cran.py
    - Project: scrapers
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

import requests
from typing_extensions import override
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

from ..data_source_abc import DataSourceABC
from ..scraper import ScraperError
from ...data_source.scrapers.r import RScraper
from ...myrequests.request_handler import RequestHandler
from ...util.logger import MyLogger
from ...util.util import Util

class CranScraper(RScraper):
    '''
    Class that scrapes the CRAN website to obtain information about R packages.
    Implements the abstract class Scraper and accordingly DataSource class

    As the CRAN repository can contain packages who depend on Bioconductor packages, this class also can
    obtain the list of Bioconductor packages from the Bioconductor website and merge it with the CRAN packages.
    This functionality is implemented in the method obtain_package_data() and it is optional.

    Attributes
    ----------
    CRAN_PACKAGE_LIST_URL : str
        URL of the CRAN website where the list of packages is located
    CRAN_PACKAGE_DATA_URL : str
        URL of the CRAN website where the data of a package is located
    NAME : str
        Name of the scraper
    DESCRIPTION : str
        Description of the scraper

    '''

    # Class variables
    CRAN_PACKAGE_LIST_URL: str  = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
    CRAN_PACKAGE_DATA_URL: str  = "https://cran.r-project.org/package="
    NAME: str                   = "CRAN Scraper"
    DESCRIPTION: str            = "Scraper class implementation for the CRAN package manager."
    
    def __init__(
        self, 
        name: Optional[str] = NAME, 
        description: Optional[str] = DESCRIPTION, 
        request_handler: Optional[RequestHandler] = None,
        bioconductor_ds: Optional[DataSourceABC] = None
    ):
        '''
        Constructor of the class
        '''
        super().__init__(name, description, request_handler)

        # check if the bioconductor_ds is a valid data source instance
        if bioconductor_ds is not None and bioconductor_ds is not isinstance(
            bioconductor_ds, DataSourceABC
        ):
            raise ScraperError(
                'The bioconductor_ds parameter must be a valid data source instance'
            )

        self.bioconductor_ds = bioconductor_ds

    @override
    def obtain_package_names(self) -> List[str]:
        '''
        Get the list of packages in the CRAN website, by scraping the HTML of the page

        Returns
        -------
        List[str]
            List of packages
            
        Examples
        --------
        >>> from olivia_finder.scraping.cran import CranScraper
        >>> cs = CranScraper()
        >>> package_names = cs.obtain_package_names()
        '''

        response = self.request_handler.do_request(self.CRAN_PACKAGE_LIST_URL)[1]

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get table with packages
        table = soup.find("table")
        rows = table.find_all("tr")
        # Clean the first row of the table (it contains the headers)
        rows.pop(0)

        packages = []

        # We iterate over each row of the table to get the names of the packages
        for row in rows:
            if not (cells := row.find_all("td")):
                continue
            try: 
                # We extract the name of the package
                # The name is in the first cell of the row
                package_name = cells[0].find("a").text   
            # If an error occurs, we show the error message
            except AttributeError as e:
                MyLogger.log(f'Error while obtaining the name of a package: {e}')
                continue

            # We add the package name to the list of packages
            packages.append(package_name)
            MyLogger.log(f'Package {package_name} added to the list of packages')

        return packages

    @override
    def _build_url(self, package_name: str) -> str:
        '''
        Build the URL of a package page in the CRAN website

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        str
            URL of the package page

        '''
        return f'{self.CRAN_PACKAGE_DATA_URL}{package_name}'

    @override
    def _parser(self, response: requests.Response) -> Dict[str, str]:
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
            return None

        # Get package version
        version = None
        try:
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = Util.clean_string(d)
        except Exception:
            MyLogger.log(f'Version not found for package {name}')

        # Get depends
        dep_list = []
        try:
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = Util.clean_string(d)
            dep_list = self._parse_dependencies(depends)
        except Exception:
            MyLogger.log(f'Dependencies not found for package {name}')

        # Get imports
        imp_list = []
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = Util.clean_string(d)
            imp_list = self._parse_dependencies(imports)
        except Exception:
            MyLogger.log(f'Imports not found for package {name}')
            
        # Build dictionary with package data
        # we consider that dependencies and imports are the same level of importance
        # so we add them to the same list
        dependencies = list(dep_list + imp_list)

        return {
            'name': name,
            'version': version,
            'dependencies': dependencies,
            'url': f'{self.CRAN_PACKAGE_DATA_URL}{name}'
        }

    @override
    def obtain_package_data(self, package_name: str) -> Dict[str, str]:
        '''
        Get the data of a package in the CRAN website, the use_bioconductor parameter can be used 
        to check if the package is a Bioconductor package if it is not found in the CRAN website,
        if the package is a Bioconductor package, it will be obtained from the Bioconductor 
        datasource class attribute.
        If the use_bioconductor flag is enabled and a Bioconductor datasource is not provided,
        an exception will be raised.

        Parameters
        ----------
        package_name : str
            Name of the package
        use_bioconductor : bool
            If True, it will check if the package is a Bioconductor package

        Raises
        ------
        ScraperError
            If the package does not exist in in the provided datasources
        
        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package

        '''
        # We build the URL of the package page
        url = self._build_url(package_name)

        # We make the HTTP request to the package page
        response = self.request_handler.do_request(url)[1]

        # Check if the package exists
        if response.status_code == 404:
            MyLogger.log(f'Package {package_name} not found in the CRAN website')

            if not self.bioconductor_ds:
                raise ScraperError("Bioconductor datasource not found, please provide a valid datasource usin the class constructor ")

            MyLogger.log(f'Checking if {package_name} is a Bioconductor package')
            return self.bioconductor_ds.obtain_package_data(package_name)

        # We parse the HTML of the package page and return the data
        return self._parser(response)


        # # if there is no bioconductor datasource, we use the default method
        # if not self.bioconductor_ds:
        #     super().obtain_package_data(package_name)
        # else:
        #     try:
        #         super().obtain_package_data(package_name)
        #     except ScraperError(f"Package {package_name} not found in the CRAN website"):
        #         MyLogger.log(f'Checking if {package_name} is a Bioconductor package')
        #         return self.bioconductor_ds.obtain_package_data(package_name)

