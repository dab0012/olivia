'''
File:              npm.py
Project:           Olivia-Finder
Created Date:      Thursday March 2nd 2023
Author:            Daniel Alonso Báscones
Last Modified:     Thursday March 2nd 2023 3:07:37 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests
from typing import List
from tqdm import tqdm
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.scraping.scraper import Scraper
from olivia_finder.package import Package
from olivia_finder.util import UtilLogger

class NpmScraper(Scraper):
    '''
    Class that scrapes the NPM website to obtain information about JavaScript packages
    '''

    # Constants
    NPM_PACKAGEs_URL = 'https://libraries.io/search?order=desc&platforms=npm&sort=rank'

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class

        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests
        '''

        super().__init__(rh, 'NPM')

        # List of keys to get the list of packages when downloading the pages
        # This is an auxiliary list to avoid downloading the same page twice while the implementation is not finished
        # It will be removed in the future
        self.GET_NAMES_KEYS = []

    def obtain_package_names(self, page_size=100, save_chunks = False, save_folder = None) -> List[dict]:

        # Get the total number of packages
        # response = requests.get(self.NPM_PACKAGE_REGISTRY_URL)
        response = self.request_handler.do_request(self.NPM_PACKAGE_REGISTRY_URL)[1]
        total_packages = response.json()['doc_count']

        # Calculate the number of pages (chunks)
        num_pages = (total_packages // page_size) + 1
        progress_bar = tqdm(total=num_pages)
        last_key = None

        pages = []
        for i in range(num_pages):
            page = self.__download_page(last_key, progress_bar, page_size)
            pages.append(page)
            UtilLogger.logg(f'Downloaded page {i} of {num_pages}', 'INFO')

            # get the last key of the page for the next iter
            last_key = page[-1]['id']
        
            if save_chunks:
                UtilLogger.logg(f'Saving chunk {i} of {num_pages}', 'INFO')
                with open(f'{save_folder}/chunk_{i}.json', 'w') as f:
                    f.write(str(page))            

            progress_bar.update(1)

        # process the pages
        package_names = [row['id'] for page in pages for row in page]

        return package_names

    # Function to download a page of documents
    def __download_page(self, start_key, progress_bar: tqdm, size: int = 1000, retries: int = 5)-> List[dict]:

        # Fix for the first page
        if start_key is None:
            params = {'limit': size}
        else:
            encode_start_key = "\"" + start_key + "\""
            params = {'startkey': encode_start_key, 'limit': size}

        # Retry the request if it fails
        response = self.request_handler.do_request(
            self.NPM_PACKAGE_LIST_URL, 
            params=params, retry_count=retries
        )[1]
   
        # If the response is None, return an empty list
        if response is None:
            print('Error getting response')
            return []
                        
        # If the response returns an error, return an empty list
        try:
            data = response.json()
        except Exception as e:
            UtilLogger.logg(f'EXCEPTION at __download_page: url={self.NPM_PACKAGE_LIST_URL}', 'ERROR')
            UtilLogger.logg(f'Error parsing JSON: {e}', 'ERROR')
            UtilLogger.logg(f'Response: {response.text}', 'ERROR')
            UtilLogger.logg(f'Params: {params}', 'ERROR')
            UtilLogger.logg(f'Retrying, times left: {retries}', 'ERROR')
            return self.__download_page(start_key, progress_bar, size, retries-1)
            
        if data.keys() == {'error', 'reason'}:
            return self.__download_page(start_key, progress_bar, size, retries-1)
        
        else:
            progress_bar.update(1)

            # Fix of selecting by last key
            return data['rows'][1:]
    
    def build_urls(self, pckg_names: List[str]) -> List[str]:
        '''
        Build the urls of the packages

        Parameters
        ----------
        pckg_names : list
            List of package names

        Returns
        -------
        List[str]
            List of urls
        '''

        # If the package name contains a slash, it is a scoped package
        # and we must replace the slash with a %2F to hit the correct url
        slash_token = '%2F'
        urls = []
        for pckg_name in pckg_names:
            if slash_token in pckg_name:
                pckg_name = pckg_name.replace('/', slash_token)
                
            urls.append(f'{self.NPM_PACKAGE_REGISTRY_URL}/{pckg_name}')

        return urls

    def parser(self, response: requests.Response) -> dict:
        '''
        Parse the response of the request

        Parameters
        ----------
        response : requests.Response
            Response of the request

        Returns
        -------
        dict
            Dictionary with the parsed data
        '''

        response_json = response.json()

        # Check if the package exists
        if 'error' in response_json:
            return {}

        # Get the package name and version
        package_name = response_json['_id']
        package_version = response_json['dist-tags']['latest']

        # get the dependencies
        try:
            dependencies = response_json['versions'][package_version]['dependencies']
        except KeyError:
            dependencies = {}

        dep_list = []
        for key in dependencies:
             
            # Get the name and version of the dependency
            dep_name = key
            dep_version = dependencies[key].replace('^', '')

            # Create the dependency object
            d = Package("NPM", dep_name, dep_version)
            dep_list.append(d)

        return {
            'name': package_name,
            'version': package_version,
            'dependencies': dep_list,
            'url': f'{self.NPM_REPO_URL}/{package_name}'
        }

    def scrape_package_data(self, package_name: str) -> Package:
        '''
        Scrape the data of a package

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        Package
            Package object with the scraped data
        '''

        # Make the request to the package registry
        url = f'{self.NPM_PACKAGE_REGISTRY_URL}/{package_name}'
        response = self.request_handler.do_request(url)[1]
        
        # Check if the package exists
        if response.status_code == 404:
            return None
        
        # Parse the response
        logging.info(f'Parsing JSON data of {package_name}')
        data = self.parser(response)

        # Check if the package exists
        if data == {}:
            return None

        # return the package as dict
        return data
