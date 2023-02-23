# Author: Daniel Alonso Báscones
# Date: 2022-2-21
# Project: TFG OLIVIA

from bs4 import BeautifulSoup
from typing import Dict

from ...Util import *
from ...ProxyRequest import RequestHandler
from .R_Scraper import R_Scraper

class Cran_Scraper(R_Scraper):
    '''
    Class that scrapes the CRAN website to obtain information about R packages
    '''

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

        super().__init__(request_handler)

    def scrape_package(self, pkg_name) -> Dict[str, str]:
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
        except Exception as e:
            print_colored(f'Exception getting package {pkg_name} in CranScraper.__parse_pkg_data: {e}', 'red')
            return None

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get Name and Description
        # ------------------------
        name = soup.title.text.split(':')[0]
        description = clean_string(soup.find('p').text)

        # Get optional table data
        # -----------------------      

        # Get package version
        version = None
        try:
            d = soup.find('td', text='Version:').find_next_sibling('td').text
            version = clean_string(d)
        except:
            pass

        # Get publication date
        publication_date = None    
        try:
            d = soup.find('td', text='Published:').find_next_sibling('td').text
            publication_date = clean_string(d)
        except:
            pass

        # Get author
        authors = None
        try:
            d = soup.find('td', text='Author:').find_next_sibling('td').text
            authors = clean_string(d)
        except:
            pass

        # Get mantainer
        mantainer = None
        try:
            d = soup.find('td', text='Maintainer:').find_next_sibling('td').text.replace(' at ', '@')
            mantainer = clean_string(d)
        except:
            pass

        # Get license
        license = None
        try:
            d = soup.find('td', text='License:').find_next_sibling('td').text
            license = clean_string(d)
        except:
            pass

        # Get compilation requirement
        requires_compilation = None
        try:
            d = soup.find('td', text='NeedsCompilation:').find_next_sibling('td').text
            d = clean_string(d)
            requires_compilation = (d == 'yes')    # Convert to boolean
        except:
            pass

        # Get dependencies
        depends = None
        try:
            d = soup.find('td', text='Depends:').find_next_sibling('td').text
            depends = clean_string(d)
        except:
            pass

        # Get imports
        imports = None
        try:
            d = soup.find('td', text='Imports:').find_next_sibling('td').text
            imports = clean_string(d)
        except:
            pass

        # Build dictionary with package data
        return {
            'name': name,
            'description': description,
            'version': version,
            'publication_date': publication_date,
            'authors': authors,
            'mantainer': mantainer,
            'license': license,
            'requires_compilation': requires_compilation,
            'depends': depends,
            'imports': imports,
            'url': url,
            'source': 'CRAN'
        }

   