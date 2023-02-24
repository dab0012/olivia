# Author: Daniel Alonso Báscones
# Date: 2022-2-21
# Project: TFG OLIVIA

from bs4 import BeautifulSoup
from typing import Dict, Union

from ...LoadConfig import logging
from ...Util import clean_string
from ...ProxyRequest import RequestHandler
from .RScraper import RScraper

class CranScraper(RScraper):
    '''
    Class that scrapes the CRAN website to obtain information about R packages
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

        super().__init__(rh)

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
        url = f'https://cran.r-project.org/package={pkg_name}'
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

        # Get Name and Description
        # ------------------------
        name = soup.title.text.split(':')[0]
        description = clean_string(soup.find('p').text)

        # Get optional table data
        # -----------------------      

        #region optional data

        # Get package version
        version = None
        try:
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have a version')

        # Get publication date
        publication_date = None    
        try:
            d = soup.find('td', text='Published:').find_next_sibling('td').text
            publication_date = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have a publication date')

        # Get author
        authors = None
        try:
            d = soup.find('td', text='Author:').find_next_sibling('td').text
            authors = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have an author')

        # Get mantainer
        mantainer = None
        try:
            d = soup.find('td', text='Maintainer:').find_next_sibling('td').text.replace(' at ', '@')
            mantainer = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have a mantainer')

        # Get license
        license_ = None
        try:
            d = soup.find('td', text='License:').find_next_sibling('td').text
            license_ = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have a license')

        # Get compilation requirement
        requires_compilation = None
        try:
            d = soup.find('td', text='NeedsCompilation:').find_next_sibling('td').text
            d = clean_string(d)
            requires_compilation = (d == 'yes')    # Convert to boolean
        except Exception:
            logging.info(f'Package {pkg_name} does not have a compilation requirement')

        #endregion optional data

        # Get dependencies
        # ----------------

        # Get depends
        depends = None
        try:
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have dependencies')

        # Get imports
        imports = None
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = clean_string(d)
        except Exception:
            logging.info(f'Package {pkg_name} does not have imports')

        # Build dictionary with package data
        return {
            'name': name,
            'description': description,
            'version': version,
            'publication_date': publication_date,
            'authors': authors,
            'mantainer': mantainer,
            'license': license_,
            'requires_compilation': requires_compilation,
            'depends': depends,
            'imports': imports,
            'url': url,
            'source': 'CRAN'
        }

   