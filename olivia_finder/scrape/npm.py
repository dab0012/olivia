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
from typing import Dict, List, Union
from bs4 import BeautifulSoup
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

    def __init__(self, rh: RequestHandler) -> None:
        '''
        Constructor of the class

        Parameters
        ----------
        rh : RequestHandler
            RequestHandler object to make HTTP requests
        '''

        super().__init__(rh, 'NPM')

    def obtain_package_names(self, page_size=2000, num_threads=32) -> List[dict]:
        '''
        Obtain the names of the packages in the repository

        Returns
        -------
        List[dict]
            List of dictionaries with the name of the package and the url
        '''

        # Get the total number of packages
        response = requests.get(self.NPM_PACKAGE_REGISTRY_URL)
        total_packages = response.json()['doc_count']

        # Get the list of packages
        # ------------------------

        # Get the initial package list of the block
        start_keys = []
        for i in range(0, total_packages, page_size):
            start_keys.append(f'"{i}"')

        # show progress of download chunks
        progress_bar = tqdm(total=len(start_keys))
        progress_bar.set_description('Descargando paquetes')

        func = partial(
            self.__download_page,           # function to execute
            progress_bar=progress_bar,      # progress bar
        )

        pages = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            pages = list(executor.map(func, start_keys))

        # Get the complete list of package names        
        package_names = []
        for page in pages:
            for row in page:
                package_names.append(row['id'])

        return package_names

    # Function to download a page of documents
    def __download_page(self, start_key, progress_bar:tqdm, size=2000):
        params = {'limit': size, 'start_key': start_key}
        try:
            response = requests.get(self.NPM_PACKAGE_LIST_URL, params=params)
        except Exception as e:
            print(e)
            # If there is an error retry the request 5 more times
            for i in range(5):
                try:
                    response = requests.get(self.NPM_PACKAGE_LIST_URL, params=params)
                    break
                except Exception as e:
                    print(e)
                    continue
                
                print('No se pudo descargar la página con start_key:', start_key)
        
        progress_bar.update(1)
        return response.json()['rows']
    
    def build_urls(self, pckg_names: list) -> List[str]:
        pass

    def parser(self, response: requests.Response) -> dict:
        pass

    def scrape_package_data(self, package_name: str) -> Package:
        pass