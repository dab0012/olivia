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
import logging, requests
from typing import List
from tqdm import tqdm
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.scraper import Scraper
from olivia_finder.package import Package

class NpmScraper(Scraper):
    '''
    Class that scrapes the NPM website to obtain information about JavaScript packages
    '''

    NPM_PACKAGE_REGISTRY_URL = 'https://skimdb.npmjs.com/registry'
    NPM_PACKAGE_LIST_URL = 'https://skimdb.npmjs.com/registry/_all_docs'
    NPM_REPO_URL = 'https://www.npmjs.com/package'

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class

        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests
        '''

        super().__init__(rh, 'NPM')

    # def obtain_package_names(self, page_size=2000, num_threads=32) -> List[dict]:
    #     '''
    #     Obtain the names of the packages in the repository

    #     Returns
    #     -------
    #     List[dict]
    #         List of dictionaries with the name of the package and the url
    #     '''

    #     # Get the total number of packages
    #     response = requests.get(self.NPM_PACKAGE_REGISTRY_URL)
    #     total_packages = response.json()['doc_count']

    #     # Get the list of packages
    #     # ------------------------

    #     # Build the list of start keys
    #     start_keys = []
    #     iters = (total_packages // page_size) + 1
    #     for i in range(iters):
    #         start_keys.append(str(i))
    #         i += page_size
            
    #     # show progress of download chunks
    #     progress_bar = tqdm(total=len(start_keys))
    #     progress_bar.set_description('Descargando paquetes')

    #     func = partial(
    #         self.__download_page,           # function to execute
    #         progress_bar=progress_bar,      # progress bar
    #     )

    #     pages = []
    #     with ThreadPoolExecutor(max_workers=num_threads) as executor:
    #         pages = list(executor.map(func, start_keys))
    #         logging.info('Descargadas todos los chunks de paquetes de NPM')

    #     # Get the complete list of package names        
    #     package_names = []
    #     for page in pages:

    #         # If the page is empty
    #         if not page:
    #             logging.debug('Chunk de paquetes de NPM vacío')
    #             continue

    #         for row in page:
    #             package_names.append(row['id'])

    #     return package_names

    def obtain_package_names(self, page_size=100) -> List[dict]:

        # Get the total number of packages
        response = requests.get(self.NPM_PACKAGE_REGISTRY_URL)
        total_packages = response.json()['doc_count']

        # Get the list of packages in chunks of 100 without using threads
        # -----------------------------------------

        num_pages = (total_packages // page_size) + 1
        progress_bar = tqdm(total=num_pages)
        last_key = None

        pages = []
        for i in range(num_pages):
            page = self.__download_page(last_key, progress_bar, page_size)
            pages.append(page)
            last_key = page[-1]['id']
            progress_bar.update(1)
        
        # process the pages
        package_names = []
        for page in pages:
            for row in page:
                package_names.append(row['id'])

        return package_names

    # Function to download a page of documents
    def __download_page(self, start_key, progress_bar:tqdm, size, retries=5):
        '''
        Download a page of documents

        Parameters
        ----------
        start_key : str
            Start key of the page
        progress_bar : tqdm
            Progress bar to show the progress of the download
        size : int
            Size of the page
        retries : int, optional

        Returns
        -------
        List[dict]
            List of documents
        '''

        # Try to do the request
        response = None
        
        # Fix for the first page
        if start_key is None:
            params = {'limit': size}
        else:
            start_key = "\"" + start_key + "\""
            params = {'startkey': start_key, 'limit': size}

        try:
            response = requests.get(self.NPM_PACKAGE_LIST_URL, params=params)
        except Exception as e:
            print(e)
            for i in range(5):
                try:
                    response = requests.get(self.NPM_PACKAGE_LIST_URL, params=params)
                    break
                except Exception as e:
                    print(e)
                    continue

        # If the response is None, return an empty list
        if response is None:
            print('Error getting response')
            return []
                        
        # If the response returns an error, return an empty list
        data = response.json()
        if data.keys() == {'error', 'reason'}:
            print(data['reason'])
            return []
        
        progress_bar.update(1)
        return data['rows']

    
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
