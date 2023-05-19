import re
import requests
from typing_extensions import override
from bs4 import BeautifulSoup
from ..scraper_ds import ScraperDataSource
from ...myrequests.request_handler import RequestHandler
from ...myrequests.job import RequestJob
from ...utilities.logger import MyLogger
from ...utilities.exception import OliviaFinderException

class GithubScraper(ScraperDataSource):
    ''' 
    Class that scrapes the PyPI website to obtain information about Python packages
    Implements the abstract class Scraper and accordingly DataSource class
    
    Attributes
    ----------
    NAME : str
        Name of the scraper
    DESCRIPTION : str
        Description of the scraper

    '''

    # Class variables  
    NAME: str                   = "Github Scraper"
    DESCRIPTION: str            = "Scraper class implementation for the Github repository network."

    def __init__(self, name: str = NAME, description: str = DESCRIPTION, request_handler: RequestHandler = None):
        '''
        Constructor
        '''

        super().__init__(name, description, request_handler)

    @override
    def obtain_package_names(self, repository: str) -> list[str]:
        '''
        Obtain the list of packages names from the github repository 

        Parameters
        ----------
        repository : str
            Repository to scrape

        Returns
        -------
        list[str]
            List of packages names

        '''

        request_timeout = 10


        # Build the request job and do the request
        url = self._build_url(repository)
        job = self.request_handler.do_request(
            RequestJob("Repository packages", url)
        )

        if job.response is None:
            raise OliviaFinderException(f'Error obtaining the list of packages from {url}')
        
        
        # Get the list of packages
        soup = BeautifulSoup(job.response.text, 'html.parser')


        next_page = True
        dependencies = []

        # Loop through all pages
        while next_page:

            # do request and parse
            response = requests.get(url=url, timeout=request_timeout)
            soup = BeautifulSoup(response.content, "html.parser")

            # loop through all dependencies
            for d in soup.findAll("li", {"class":"Box-row"}):

                # Get data and store in the list
                dep_name = d.find("a").text
                dep_version = d.find("span").text
                dep_url = f'https://github.com{d.find("a")["href"]}'

                # Clean up data
                dep_name = dep_name.replace(" ", "").replace("\n", "")
                dep_version = dep_version.replace(" ", "").replace("\n", "")

                dependencies.append({
                    "name": dep_name,
                    "version": dep_version,
                    "url": dep_url
                })

            # Check if next page exists and update url
            next_page = soup.find("a", {"class":"next_page"}) != None
            if next_page:
                url = f"https://github.com{soup.find('a', {'class':'next_page'})['href']}"
        
        return dependencies
    

    def _parser(self, response) -> dict:
        pass

    @override
    def _build_url(self, repository: str) -> str:
        '''
        Build the URL to scrape a package
        Implements the abstract method of Scraper class
        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        str
            URL to scrape
        '''

        return f"https://github.com/{repository}/network/dependencies"


        '''
        Clean the package name from versions and other characters

        Parameters
        ----------
        name : str
            Name of the package
        
        Returns
        -------
        str
            Cleaned name of the package
            
        '''
        
        regex = re.compile(r'[^\w\d]+')

        # Reemplazar cualquier coincidencia de la expresión regular en la cadena de dependencia con un espacio en blanco
        name = regex.sub(' ', name)

        # Obtenga el primer elemento de la lista resultante después de dividir la cadena por espacios en blanco
        name = name.split()[0]

        return name