'''
npm.py
==================

Description
-----------

Module that contains ...

File information:
    - File: npm.py
    - Project: scrapers
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''


import os
from typing import List
import requests
from typing_extensions import override
from tqdm import tqdm

from ..scraper_ds import ScraperDataSource
from ...utilities.config import Configuration
from ...utilities.logger import MyLogger
from ...myrequests.request_handler import RequestHandler
from ...myrequests.job import RequestJob


class NpmScraper(ScraperDataSource):
    '''
    Class that scrapes the NPM website to obtain information about JavaScript packages
    
    Attributes
    ----------
    NPM_PACKAGE_REGISTRY_URL : str
        URL of the page that contains the list of packages
    NPM_PACKAGE_LIST_URL : str
        URL of the page that contains the data of a package
    NPM_REPO_URL : str
        URL of the page that contains the data of a package
        
    Parameters
    ----------
    request_handler : RequestHandler = None
        Request handler for the scraper, if None, it will be initialized with a generic RequestHandler
    '''

    # Constants
    NPM_PACKAGE_REGISTRY_URL: str   = 'https://skimdb.npmjs.com/registry'
    NPM_PACKAGE_LIST_URL: str       = 'https://skimdb.npmjs.com/registry/_all_docs'
    NPM_REPO_URL: str               = 'https://www.npmjs.com/package'
    NAME: str                       = "NPM Scraper"
    DESCRIPTION: str                = "Scraper class implementation for the NPM package manager."

    def __init__(
        self, 
        request_handler: RequestHandler = None,
    ):
        '''
        Constructor of the class
        '''

        self.chunks_folder = None
        '''
        Folder where the chunks will be saved, 
        This is because the NPM registry is too big to be downloaded in one go
        '''

        super().__init__(request_handler)

    @override
    def obtain_package_names(
        self, 
        page_size: int = 100, 
        show_progress_bar: bool = True,
        save_chunks: bool = False,
    ) -> List[dict]:

        '''
        Function to obtain the names of the packages in the NPM repository

        Parameters
        ----------
        page_size : int = 100
            Number of packages to be requested in each page
        show_progress_bar : bool = True
            Flag to show the progress bar
        save_chunks : bool = False
            Flag to save the chunks of the registry in the chunks folder
        
        Returns
        -------
        List[dict]
            List of dictionaries with the name and version of the packages
        
        Examples
        --------
        >>> scraper = NpmScraper()
        >>> scraper.obtain_package_names()
        '''
        # Get the total number of packages
        response = requests.get(self.NPM_PACKAGE_REGISTRY_URL, timeout=30)
        total_packages = response.json()['doc_count']

        # Calculate the number of pages (chunks)
        num_pages = (total_packages // page_size) + 1

        self.logger.debug(f'Total number of packages: {total_packages}')
        self.logger.debug(f'Number of pages: {num_pages}')

        # Initialize the progress bar if is set
        progress_bar = tqdm(total=num_pages) if show_progress_bar else None

        # Initialize the chunks folder if is set
        if save_chunks:
            self.logger.debug(f'Saving chunks at: {self.chunks_folder}')
            self._init_chunks_folder()

        # Obtain the names of the packages requesting the pages
        pages = []
        last_key = None
        for i in range(num_pages):

            # Download the page
            # Handle disconnects
            page = None
            while page is None:
                try:
                    page = self._download_page(last_key, page_size)
                except requests.exceptions.ConnectionError:
                    self.logger.debug(f'Connection error in page {i} of {num_pages}')
                    self.logger.debug(f'Last key: {last_key}')
                    self.logger.debug('Retrying...')

                # check if the page is empty
                if len(page) == 0:
                    self.logger.debug(f'Empty page {i} of {num_pages}')
                    self.logger.debug(f'Last key: {last_key}')
                    page = None

            pages.append(page)
            self.logger.debug(f'Downloaded page {i} of {num_pages}')

            # get the last key of the page for the next iter
            last_key = page[-1]['id']

            # Save chunk if is set
            if save_chunks:
                self.logger.debug(f'Saving chunk {i} of {num_pages}')
                with open(f'{self.chunks_folder}/chunk_{i}.json', 'w') as f:
                    f.write(str(page))            

            # Update progress bar if is set
            if show_progress_bar:
                progress_bar.update(1)

        package_names = [row['id'] for page in pages for row in page]
        self.logger.info(f'Obtained {len(package_names)} packages from {self.NPM_PACKAGE_LIST_URL}')
        return package_names

    def _init_chunks_folder(self):
        '''
        Function to initialize the chunks folder, where the chunks will be saved
        Loads the path from the configuration file
        '''
        self.chunks_folder = f'{Configuration().get_key("folders", "working_dir")}/npm_package_names_chunks'
        os.makedirs(self.chunks_folder, exist_ok=True)

    def _download_page(
        self, 
        start_key: str = None, 
        size: int = 1000, 
        retries: int = 5
    )-> List[dict]:
        '''
        Function to download a page of documents from the NPM repository and return a list of dictionaries with the name and version of the packages
        
        Parameters
        ----------
        start_key : str = None
            Key to start the download
        size : int = None
            Size of the page to download
        retries : int = None
            Number of retries to download the page
        
        Returns
        -------
        List[dict]
            List of dictionaries with the name and version of the packages
        '''

        # Fix for the first page
        if start_key is None:
            params = {'limit': size}
        else:
            encode_start_key = "\"" + start_key + "\""
            params = {'startkey': encode_start_key, 'limit': size}

        # Download the page
        job = self.request_handler.do_request(
            RequestJob(
                key='npm_download_page',
                url=self.NPM_PACKAGE_LIST_URL,
                params=params,
            )
        )
        
        # If the response is None, return an empty list
        if job.response is None:
            self.logger.debug(f'None response at __download_page: url={self.NPM_PACKAGE_LIST_URL}')
            return []
                        
        # If the response returns an error, return an empty list
        try:
            data = job.response.json()

        except Exception as e:

            msg = f'EXCEPTION at __download_page: url={self.NPM_PACKAGE_LIST_URL}\n'
            msg += f'Response: {job.response.text}\n'
            msg += f'Params: {params}\n'
            msg += f'Retrying, times left: {retries}\n'
            self.logger.debug(msg)
            
            return self._download_page(start_key, size, retries-1)
            
        if data.keys() == {'error', 'reason'}:
            return self._download_page(start_key, size, retries-1)
        else:
            # Fix of selecting by last key
            return data['rows'][1:]
    
    @override
    def _build_url(self, package_name: str):
        '''
        Function to build the URL of the package

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        str
            URL of the package
        '''
        return f'{self.NPM_PACKAGE_REGISTRY_URL}/{package_name}'

    @override
    def _parser(self, response: requests.Response) -> dict:
        '''
        Parse the response of the request

        Parameters
        ----------
        response : requests.Response
            Response of the request

        Returns
        -------
        dict
            dictionary with the parsed data

        Examples
        --------
        >>> response = requests.get('https://registry.npmjs.org/express')
        >>> parser(response)
        {
            'name': 'express',
            'version': '4.17.1',
            'dependencies': [
                {'name': 'accepts', 'version': '1.3.7'},
                {'name': 'array-flatten', 'version': '1.1.1'},
                {'name': 'body-parser', 'version': '1.19.0'},
                {'name': 'content-disposition', 'version': '0.5.3'},
                {'name': 'content-type', 'version': '1.0.4'}
            ],
            'url': 'https://www.npmjs.com/package/express'
        }
        '''

        response_json = response.json()

        # Check if the package exists
        if 'error' in response_json:
            return {}

        # Get the package name and version
        package_name = response_json['_id']
        try:
            package_version = response_json['dist-tags']['latest']
        except KeyError:
            package_version = None

        # get the dependencies
        try:
            dependencies = response_json['versions'][package_version]['dependencies']
        except KeyError:
            dependencies = {}

        dep_list = [
            {'name': key, 'version': value} for key, value in dependencies.items()
        ]

        return {
            'name': package_name,
            'version': package_version,
            'dependencies': dep_list,
            'url': f'{self.NPM_REPO_URL}/{package_name}'
        }

    
    