'''
File:              bioconductor.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 7:01:57 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import logging
from typing import Dict, Union, List
from bs4 import BeautifulSoup
from olivia_finder.package import Package
from olivia_finder.util import Util
from olivia_finder.scrape.r import RScraper                                         
from olivia_finder.scrape.requests.request_handler import RequestHandler

# Selenium imports (for scraping JavaScript pages)
from selenium import webdriver                                    
from selenium.webdriver.common.by import By

class BiocScraper(RScraper):
    '''
    Class to scrape data from Bioconductor packages
    '''

    # Class variables
    BIOCONDUCTOR_LIST_URL = 'https://www.bioconductor.org/packages/release/BiocViews.html#___Software'
    BIOCONDUCTOR_PACKAGE_DATA_URL = 'https://www.bioconductor.org/packages/release/bioc/html/'

    def __init__(self, request_handler: RequestHandler) -> None:
        super().__init__(request_handler, 'Bioconductor')

    def parse_html(self, response: str) -> Dict[str, str]:
        # Get the data from the table
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='details')
        rows = table.find_all('tr')

        # For each row, we get the cells if they are of interest
        dep_list = []
        imp_list = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                if cells[0].text == 'Version':
                    version = Util.clean_string(cells[1].text.strip())
                elif cells[0].text == 'Depends':
                    depends = Util.clean_string(cells[1].text.strip())
                    if depends != '':
                        dep_list = self.parse_dependencies(depends)
                elif cells[0].text == 'Imports':
                    imports = Util.clean_string(cells[1].text.strip())
                    if imports != '':
                        imp_list = self.parse_dependencies(imports)

        # Return the data
        return {
            'version': version,
            'dependencies': [set(dep_list + imp_list)]
        }

    def scrape_package(self, pkg_name) -> Union[Dict[str, str], None]:
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
        url = f'{self.BIOCONDUCTOR_PACKAGE_DATA_URL}{pkg_name}.html'
        response = self.request_handler.do_request(url)[1]

        # Parse the response
        response_data = self.parse_html(response)
                    
        # Return data
        return {
            'name': pkg_name,
            'version': response_data['version'],
            'url': url,
            'dependencies': response_data['dependencies']
        }
    
    def scrape_package_list(self, pkg_list, progress_bar) -> List[Package]:
        '''
        Get data from a list of Bioconductor packets.
        It's obtained from the package page in the Bioconductor website.
        This function has to be called from the get_pkg_data function.
        Obtain the data through HTML scraping on the page, in addition, if any of the optional data is not found, the rest of the data is continued

        Parameters
        ----------
        pkg_list : List[str]
            List of packages
        progress_bar : tqdm
            Progress bar

        Returns
        -------
        List[Package]
            List of packages

        Raises
        ------
        Exception
            If the package is not found or any of the optional data is not found
            If any of the optional data is not found, the scraper will continue handling the rest of the data

        '''
        # # Get the list of requests to do
        # urls = []
        # for pkg_name in pkg_list:
        #     url = f'{self.BIOCONDUCTOR_PACKAGE_DATA_URL}{pkg_name}.html'
        #     urls.append((url, pkg_name))

        # # Do the requests with the request handler parallelized
        # responses = self.request_handler.do_parallel_requests(urls, urls, progress_bar=progress_bar)

        # # Parse the responses
        # pkg_list = []
        # for response in responses:
        pass

    def get_list_of_packages(self) -> List[str]:
        '''
        Get the list of packages from the Bioconductor website

        Returns
        -------
        List[str]
            List of packages

        Raises
        ------
        Exception
            If the list of packages is not found
        '''

        # Make HTTP request to the list of packages page
        # Is necessary to use Selenium because the list of packages is loaded dynamically
        # with JavaScript, we need to render the page to get the list of packages
        
        # Create the Selenium driver
        try:
            driver_options = webdriver.FirefoxOptions()
            driver_options.headless = True
            driver = webdriver.Firefox(options=driver_options)
        except Exception as e:
            logging.error(f'Error creating the Selenium driver: {e}')
            return None

        # Scraping webpage with package list
        try:
            driver.get(self.BIOCONDUCTOR_LIST_URL)
            table = driver.find_element(By.ID, "biocViews_package_table")
            table_content = table.get_attribute("innerHTML")
        except Exception as e:
            logging.error(f'Error scraping the webpage with the list of packages: {e}')
            return None

        # Close the driver
        driver.close()

        # Process the HTML to obtain packages
        try:
            soup = BeautifulSoup(table_content, 'html.parser')
            bioc_packages = []
            for row in soup.find_all("tr"):
                for cell in row.find_all("td"):
                    if cell.find("a"):
                        bioc_packages.append(cell.find("a").text)
        except Exception as e:
            logging.error(f'Error processing the HTML to obtain packages: {e}')
            return None

        return bioc_packages