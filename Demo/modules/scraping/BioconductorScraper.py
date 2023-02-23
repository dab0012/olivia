# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

from bs4 import BeautifulSoup
from typing import Dict

from modules.Util import *
from modules.scraping.ProxyRequest import RequestHandler
from modules.scraping.Scraper import Scraper

class BioconductorScraper(Scraper):

    def __init__(self, request_handler: RequestHandler) -> None:
        super().__init__(request_handler)

    def scrape_package(self, pkg_name) -> Dict[str, str]:
        '''
        Get data from a Bioconductor packet.
        It's obtained from the package page in the Bioconductor website.
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
        url = f'https://www.bioconductor.org/packages/release/bioc/html/{pkg_name}.html'
        try:
            response = self.request_handler.do_request(url)
        except Exception as e:
            print_colored(f'Exception getting package {pkg_name} in BioconductorScraper.__parse_pkg_data: {e}', 'red')
            return None

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get Name and Description
        # ------------------------

        # Get optional table data
        # -----------------------      
        data_p = soup.find('div', class_='do_not_rebase').findAll('p')
        description = clean_string(data_p[1].text)              # Get the package description
        authors = clean_string(data_p[2].text )                 # Get the authors of the package
        authors.replace('Author: ', '')                         # We removed the word 'Authors: ' from the authors
        maintainer = clean_string(data_p[3].text)               # Get the maintainer of the package
        maintainer = maintainer.replace('Maintainer: ', '')     # We remove the word 'Maintainer: ' from the maintainer
        maintainer = maintainer.replace(' at ', '@')            # We change the ' at ' by the '@' of the maintainer

        # Get the data from the table
        table = soup.find('table', class_='details')
        rows = table.find_all('tr')

        # For each row, we get the cells if they are of interest
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                if cells[0].text == 'Version':
                    version = clean_string(cells[1].text.strip())
                elif cells[0].text == 'License':
                    license = clean_string(cells[1].text.strip())
                elif cells[0].text == 'Depends':
                    depends = clean_string(cells[1].text.strip())
                elif cells[0].text == 'Imports':
                    imports = clean_string(cells[1].text.strip())
                    

        # Return data
        return {
            'name': pkg_name,
            'description': description,
            'version': version,
            'publication_date': None,
            'authors': authors,
            'mantainer': maintainer,
            'license': license,
            'requires_compilation': None,
            'depends': depends,
            'imports': imports,
            'url': url,
            'source': 'Bioconductor'
        }
    
