""""""
'''
·········································································
File: bioconductor.py
Project: Olivia-Finder
Created Date: Friday February 24th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
from typing_extensions import override

from ...data_source.scraper import ScraperError
from ...data_source.scrapers.r import RScraper
from ...myrequests.request_handler import RequestHandler
from ...util.util import Util

# Selenium imports (for scraping JavaScript pages)
from selenium import webdriver                                    
from selenium.webdriver.common.by import By

class BiocScraper(RScraper):
    '''
    Class to scrape data from Bioconductor packages
    
    Parameters
    ----------
    name : Optional[str]
        Name of the data source
    description : Optional[str]
        Description of the data source
    request_handler : Optional[RequestHandler]
        Request handler for the scraper, if None, it will be initialized with a generic RequestHandler
    
    Attributes
    ----------
    NAME : str
        The name of the data source
    DESCRIPTION : str
        The description of the data source
    BIOCONDUCTOR_LIST_URL : str
        The URL of the page with the list of Bioconductor packages
    BIOCONDUCTOR_PACKAGE_DATA_URL : str
        The URL of the page with the data of each Bioconductor package
    '''

    # Class variables
    BIOCONDUCTOR_LIST_URL = 'https://www.bioconductor.org/packages/release/BiocViews.html#___Software'
    '''The URL of the page with the list of Bioconductor packages'''
    BIOCONDUCTOR_PACKAGE_DATA_URL = 'https://www.bioconductor.org/packages/release/bioc/html/'
    '''The URL of the page with the data of each Bioconductor package'''
    NAME: str = 'Bioconductor'
    '''The name of the data source'''
    DESCRIPTION: str = "Scraper class implementation for the Bioconductor package network"
    '''The description of the data source'''

    
    def __init__(
        self, 
        name: Optional[str] = NAME, 
        description: Optional[str] = DESCRIPTION, 
        request_handler: Optional[RequestHandler] = None, 
    ):
        '''
        Constructor
        '''
        super().__init__(name, description, request_handler)

    @override
    def obtain_package_names(self) -> List[str]:
        '''
        Get the list of packages from the Bioconductor website

        Returns
        -------
        List[str]
            List of package names
            
        Raises
        ------
        ScraperError
            If the list of packages cannot be obtained
            
        Example
        -------
        >>> scraper = BiocScraper()
        >>> package_names = scraper.obtain_package_names()
        '''

        # # Make HTTP request to the list of packages page
        # # Is necessary to use Selenium because the list of packages is loaded dynamically
        # # with JavaScript, we need to render the page to get the list of packages

        # # Load the Selenium driver
        # driver_path = UtilConfig.get_value_config_file("selenium", "driver_path")

        # # Check if the driver exists
        # if not os.path.exists(driver_path):
        #     UtilLogger.logg(f'The Selenium driver does not exist: {driver_path}')
        #     return None

        # Create the driver

        try:
            driver_options = webdriver.FirefoxOptions()
            driver_options.headless = True
            driver = webdriver.Firefox(
                options = driver_options, 
                # executable_path = driver_path
            )
        except ScraperError("Exception occurred while creating the Selenium driver.") as e:
            raise e

        # Scraping webpage with package list
        try:
            driver.get(self.BIOCONDUCTOR_LIST_URL)
            table = driver.find_element(By.ID, "biocViews_package_table")
            table_content = table.get_attribute("innerHTML")
        except ScraperError("Exception occurred while scraping the Bioconductor website.") as e:
            raise e

        # Close the driver
        driver.close()

        # Process the HTML to obtain packages
        try:
            soup = BeautifulSoup(table_content, 'html.parser')
            packages = []
            for row in soup.find_all("tr"):
                packages.extend(
                    cell.find("a").text
                    for cell in row.find_all("td")
                    if cell.find("a")
                )
        except ScraperError("Exception occurred while processing the HTML.") as e:
            raise e
        
        # Sort the list of packages
        packages.sort()
        
        return packages
    
    @override
    def _build_url(self, package_name: str) -> str:
        '''
        Build the URL of the package page in the Bioconductor website

        Parameters
        ----------
        package_name : str
            The name of the package
        
        Returns
        -------
        str
            The URL of the package page in the Bioconductor website
        '''
        return f'{self.BIOCONDUCTOR_PACKAGE_DATA_URL}{package_name}.html'

    @override
    def _parser(self, response: requests.Response) -> Dict[str, str]:
        '''
        Parse the response from the Bioconductor website
        It's obtained from the list of packages in the Bioconductor website

        Parameters
        ----------
        response : requests.Response
            The response from the Bioconductor website
        
        Returns
        -------
        Dict[str, str]
            The data of the package
        '''        
        # Get the data from the table
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('h1').text.strip()
        url = response.url

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
                        dep_list = self._parse_dependencies(depends)
                elif cells[0].text == 'Imports':
                    imports = Util.clean_string(cells[1].text.strip())
                    if imports != '':
                        imp_list = self._parse_dependencies(imports)
                        
        # Remove duplicates from the dependencies
        for dep in dep_list:
            if dep in imp_list:
                imp_list.remove(dep)

        # Return the data
        return {
            'name': name,
            'version': version,
            'dependencies': list(dep_list + imp_list),
            'url': url
        }

