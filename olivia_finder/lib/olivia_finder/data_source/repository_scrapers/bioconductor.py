'''
bioconductor.py
==================

Description
-----------

Module that contains ...

File information:
    - File: bioconductor.py
    - Project: scrapers
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

import requests
from bs4 import BeautifulSoup
from typing_extensions import override
from . import r
from ..scraper_ds import ScraperDataSource, ScraperError
from ...myrequests.request_handler import RequestHandler
from ...utilities.utilities import clean_string
from ...utilities.logger import MyLogger

# Selenium imports (for scraping JavaScript pages)
from selenium import webdriver                                    
from selenium.webdriver.common.by import By

class BioconductorScraper(ScraperDataSource):
    '''
    Class to scrape data from Bioconductor packages
    
    Parameters
    ----------
    name : str = None
        Name of the data source
    description : str = None
        Description of the data source
    auxiliary_datasources : Optional[list[DataSource]]
        List of auxiliary data sources
    request_handler : RequestHandler = None
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
    
    def __init__(
        self, 
        name: str = None, 
        description: str = None, 
        request_handler: RequestHandler = None,
    ):
        '''
        Constructor
        '''

        # Initialize the class variables
        self.BIOCONDUCTOR_LIST_URL = 'https://www.bioconductor.org/packages/release/BiocViews.html#___Software'
        self.BIOCONDUCTOR_PACKAGE_DATA_URL = 'https://www.bioconductor.org/packages/release/bioc/html/'
        if name is None:
            self.NAME: str = 'Bioconductor'
        if description is None:
            self.DESCRIPTION: str = "Scraper class implementation for the Bioconductor package network"

        # Call the constructor of the parent class
        super().__init__(self.NAME, self.DESCRIPTION, request_handler)



    @override
    def obtain_package_names(self) -> list[str]:
        '''
        Get the list of packages from the Bioconductor website
        TODO: FIX THIS METHOD, IT REQUIRES FIREFOX INSTALLED IN THE SYSTEM and it can be fixed 

        Returns
        -------
        list[str]
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
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


        # Create the driver
        try:
            MyLogger().get_logger().debug("Creating the Selenium driver...")

            driver_options = webdriver.FirefoxOptions()
            driver_options.headless = True
            driver = webdriver.Firefox(
                options = driver_options
            )
        except Exception as e:
            raise ScraperError("Exception occurred while creating the Selenium driver") from e
    
        # Scraping webpage with package list
        try:
            MyLogger().get_logger().debug("Scraping the Bioconductor website...")
            driver.get(self.BIOCONDUCTOR_LIST_URL)
            table = driver.find_element(By.ID, "biocViews_package_table")
            table_content = table.get_attribute("innerHTML")
        except Exception as e:
            raise ScraperError("Exception occurred while scraping the Bioconductor website") from e

        # Close the driver
        driver.close()

        # Process the HTML to obtain packages
        try:
            MyLogger().get_logger().debug("Processing the HTML...")
            soup = BeautifulSoup(table_content, 'html.parser')
            packages = []
            for row in soup.find_all("tr"):
                packages.extend(
                    cell.find("a").text
                    for cell in row.find_all("td")
                    if cell.find("a")
                )
        except Exception as e:
            raise ScraperError("Exception occurred while processing the HTML.") from e
        
        # Sort the list of packages
        packages.sort()
        MyLogger().get_logger().info(f"Obtained {len(packages)} packages from {self.BIOCONDUCTOR_LIST_URL}")
        
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
    def _parser(self, response: requests.Response) -> dict[str, str]:
        '''
        Parse the response from the Bioconductor website
        It's obtained from the list of packages in the Bioconductor website

        Parameters
        ----------
        response : requests.Response
            The response from the Bioconductor website
        
        Returns
        -------
        dict[str, str]
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
                    version = clean_string(cells[1].text.strip())
                elif cells[0].text == 'Depends':
                    depends = clean_string(cells[1].text.strip())
                    if depends != '':
                        dep_list = r.parse_dependencies(depends)
                elif cells[0].text == 'Imports':
                    imports = clean_string(cells[1].text.strip())
                    if imports != '':
                        imp_list = r.parse_dependencies(imports)
                        
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
