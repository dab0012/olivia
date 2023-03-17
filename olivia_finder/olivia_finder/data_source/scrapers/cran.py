
""""""
'''
·········································································
File: cran.py
Project: Olivia-Finder
Created Date: Friday February 24th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''


import contextlib, requests
from typing_extensions import override
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from olivia_finder.scraping.r import RScraper
from olivia_finder.scraping.scraper import Scraper, ScraperError
from olivia_finder.myrequests.request_handler import RequestHandler
from olivia_finder.util.logger import UtilLogger
from olivia_finder.util.util import Util

class CranScraper(RScraper, Scraper):
    '''
    Class that scrapes the CRAN website to obtain information about R packages
    
    Attributes
    ----------
    CRAN_PACKAGE_LIST_URL : str
        URL of the page that contains the list of packages
    CRAN_PACKAGE_DATA_URL : str
        URL of the page that contains the data of a package
    
    Parameters
    ----------
    name : Optional[str]
        Name of the data source
    description : Optional[str]
        Description of the data source
    request_handler : Optional[RequestHandler]
        Request handler for the scraper, if None, it will be initialized with a generic RequestHandler    
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
    ):
        '''
        Constructor of the class
        '''
        super().__init__(name, description, request_handler)

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

                # We add the package name to the list of packages
                packages.append(package_name)
                UtilLogger.log(f'Package {package_name} added to the list of packages')

            # If an error occurs, we show the error message
            except ScraperError("Error while obtaining the name of a package"):
                continue

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
        with contextlib.suppress(ScraperError(f"Error while obtaining the version of the package {name}")):
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = Util.clean_string(d)

        # Get depends
        dep_list = []
        with contextlib.suppress(ScraperError(f"Error while obtaining the dependencies of the package {name}")):
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = Util.clean_string(d)
            dep_list = self._parse_dependencies(depends)

        # Get imports
        imp_list = []
        with contextlib.suppress(ScraperError(f"Error while obtaining the imports of the package {name}")):
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = Util.clean_string(d)
            imp_list = self._parse_dependencies(imports)
            
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
