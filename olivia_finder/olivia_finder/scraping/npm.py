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

import os, requests
from typing import List
from tqdm import tqdm
from .scraper import Scraper
from ..util.config_ini import Configuration
from ..util.logger import UtilLogger
from ..requests.request_handler import RequestHandler
from ..package import Package

class NpmScraper(Scraper):
    '''
    Class that scrapes the NPM website to obtain information about JavaScript packages
    '''

    # Constants
    NPM_PACKAGE_REGISTRY_URL    = 'https://skimdb.npmjs.com/registry'
    NPM_PACKAGE_LIST_URL        = 'https://skimdb.npmjs.com/registry/_all_docs'
    NPM_REPO_URL                = 'https://www.npmjs.com/package'

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class

        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests
        '''
        super().__init__(rh, 'NPM')
        self.output_folder = Configuration().get_key("folders", "persistence_dir")
        self.chunks_folder = self.output_folder + '/chunks'

        # Create the chunks folder if it does not exist
        os.makedirs(self.chunks_folder, exist_ok=True)

    def obtain_package_names(self, page_size=100, save_chunks = False) -> List[dict]:

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
            page = self.__download_page(last_key, page_size)

            # check if the page is empty
            if len(page) == 0:
                UtilLogger.log(f'Empty page {i} of {num_pages}')
                UtilLogger.log(f'Last key: {last_key}')
                continue

            pages.append(page)
            UtilLogger.log(f'Downloaded page {i} of {num_pages}')

            # get the last key of the page for the next iter
            last_key = page[-1]['id']
        
            # Save chunk if is set
            if save_chunks:
                UtilLogger.log(f'Saving chunk {i} of {num_pages}')
                with open(f'{self.chunks_folder}/chunk_{i}.json', 'w') as f:
                    f.write(str(page))            

            progress_bar.update(1)

        # process the pages
        package_names = [row['id'] for page in pages for row in page]

        return package_names

    # Function to download a page of documents
    def __download_page(self, start_key = None, size: int = 1000, retries: int = 5)-> List[dict]:

        # Fix for the first page
        if start_key is None:
            params = {'limit': size}
        else:
            encode_start_key = "\"" + start_key + "\""
            params = {'startkey': encode_start_key, 'limit': size}

        response = self.request_handler.do_request(self.NPM_PACKAGE_LIST_URL, params=params)[1]
   
        # If the response is None, return an empty list
        if response is None:
            UtilLogger.log(f'None response at __download_page: url={self.NPM_PACKAGE_LIST_URL}')
            return []
                        
        # If the response returns an error, return an empty list
        try:
            data = response.json()
        except Exception as e:
            UtilLogger.log(f'EXCEPTION at __download_page: url={self.NPM_PACKAGE_LIST_URL}')
            UtilLogger.log(f'Error parsing JSON: {e}')
            UtilLogger.log(f'Response: {response.text}')
            UtilLogger.log(f'Params: {params}')
            UtilLogger.log(f'Retrying, times left: {retries}')
            return self.__download_page(start_key, size, retries-1)
            
        if data.keys() == {'error', 'reason'}:
            return self.__download_page(start_key, size, retries-1)
        else:
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
        data = self.parser(response)

        # Check if the package exists
        if data == {}:
            return None

        # return the package as dict
        return data
