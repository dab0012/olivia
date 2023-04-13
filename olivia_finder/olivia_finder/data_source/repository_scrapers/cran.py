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
from . import r
from ..data_source import DataSource
from ..scraper_ds import ScraperDataSource
from ...myrequests.request_handler import RequestHandler
from ...utilities.logger import MyLogger
from ...utilities.util import Util

class CranScraper(ScraperDataSource):
    '''
    Class that scrapes the CRAN website to obtain information about R packages.
    Implements the abstract methods of the ScraperDataSource class.

    As the CRAN repository can contain packages who depend on Bioconductor packages, this class also can
    obtain the list of Bioconductor packages from the Bioconductor website and merge it with the CRAN packages.
    This functionality is implemented in the method obtain_package_data() and it is optional.

    Parameters
    ----------
    name : Optional[str]
        Name of the data source
    description : Optional[str]
        Description of the data source
    auxiliary_datasources : Optional[List[DataSource]]
        List of auxiliary data sources that can be used to obtain information about packages        
    request_handler : Optional[RequestHandler]
        Request handler for the scraper, if None, it will be initialized with a generic RequestHandler

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

    def __init__(
        self, 
        name: Optional[str] = None, 
        description: Optional[str] = None, 
        auxiliary_datasources: Optional[List[DataSource]] = None,
        request_handler: Optional[RequestHandler] = None
    ):
        '''
        Constructor of the class
        '''

        # We initialize the class variables
        self.CRAN_PACKAGE_LIST_URL: str  = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
        self.CRAN_PACKAGE_DATA_URL: str  = "https://cran.r-project.org/package="
        self.NAME: str = "CRAN Scraper" if name is None else name
        if description is None:
            self.DESCRIPTION: str = "Scraper class implementation for the CRAN package manager."
        else:
            self.DESCRIPTION: str = description

        # We call the constructor of the parent class
        super().__init__(self.NAME, self.DESCRIPTION, auxiliary_datasources, request_handler)

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
            dep_list = r.parse_dependencies(depends)
        except Exception:
            MyLogger.log(f'Dependencies not found for package {name}')

        # Get imports
        imp_list = []
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = Util.clean_string(d)
            imp_list = r.parse_dependencies(imports)
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

    