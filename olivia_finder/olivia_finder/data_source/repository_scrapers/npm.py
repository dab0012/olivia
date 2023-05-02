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
import requests
from typing_extensions import override
from typing import Optional
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
    NAME : str
        Name of the data source
    DESCRIPTION : str
        Description of the data source
        
    Parameters
    ----------
    name : Optional[str]
        Name of the scraper
    description : Optional[str]
        Description of the scraper
    request_handler : Optional[RequestHandler]
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
        name: Optional[str] = NAME, 
        description: Optional[str] = DESCRIPTION, 
        request_handler: Optional[RequestHandler] = None
    ):
        '''
        Constructor of the class
        '''

        self.chunks_folder = None
        '''
        Folder where the chunks will be saved, 
        This is because the NPM registry is too big to be downloaded in one go
        '''

        super().__init__(name, description, request_handler)

    @override
    def obtain_package_names(
        self, 
        page_size: Optional[int]=100, 
        show_progress_bar: Optional[bool]=True,
        save_chunks: Optional[bool]=False,
    ) -> list[dict]:

        '''
        Function to obtain the names of the packages in the NPM repository

        Parameters
        ----------
        page_size : Optional[int]
            Size of the page to download
        save_chunks : Optional[bool]
            Flag to save the chunks in the chunks folder
        show_progress_bar : Optional[bool]
            Flag to show the progress bar
        
        Returns
        -------
        list[dict]
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

        MyLogger().get_logger().debug(f'Total number of packages: {total_packages}')
        MyLogger().get_logger().debug(f'Number of pages: {num_pages}')

        # Initialize the progress bar if is set
        progress_bar = tqdm(total=num_pages) if show_progress_bar else None

        # Initialize the chunks folder if is set
        if save_chunks:
            MyLogger().get_logger().debug(f'Saving chunks at: {self.chunks_folder}')
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
                    MyLogger().get_logger().debug(f'Connection error in page {i} of {num_pages}')
                    MyLogger().get_logger().debug(f'Last key: {last_key}')
                    MyLogger().get_logger().debug('Retrying...')

                # check if the page is empty
                if len(page) == 0:
                    MyLogger().get_logger().debug(f'Empty page {i} of {num_pages}')
                    MyLogger().get_logger().debug(f'Last key: {last_key}')
                    page = None

            pages.append(page)
            MyLogger().get_logger().debug(f'Downloaded page {i} of {num_pages}')

            # get the last key of the page for the next iter
            last_key = page[-1]['id']

            # Save chunk if is set
            if save_chunks:
                MyLogger().get_logger().debug(f'Saving chunk {i} of {num_pages}')
                with open(f'{self.chunks_folder}/chunk_{i}.json', 'w') as f:
                    f.write(str(page))            

            # Update progress bar if is set
            if show_progress_bar:
                progress_bar.update(1)

        package_names = [row['id'] for page in pages for row in page]
        MyLogger().get_logger().info(f'Obtained {len(package_names)} packages from {self.NPM_PACKAGE_LIST_URL}')
        return 

    def _init_chunks_folder(self):
        '''
        Function to initialize the chunks folder, where the chunks will be saved
        Loads the path from the configuration file
        '''
        self.chunks_folder = f'{Configuration().get_key("folders", "working_dir")}/npm_package_names_chunks'
        os.makedirs(self.chunks_folder, exist_ok=True)

    def _download_page(
        self, 
        start_key: Optional[str]=None, 
        size: Optional[int]=1000, 
        retries: Optional[int]=5
    )-> list[dict]:
        '''
        Function to download a page of documents from the NPM repository and return a list of dictionaries with the name and version of the packages
        
        Parameters
        ----------
        start_key : Optional[str]
            Key to start the download
        size : Optional[int]
            Size of the page to download
        retries : Optional[int]
            Number of retries to download the page
        
        Returns
        -------
        list[dict]
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
            MyLogger().get_logger().debug(f'None response at __download_page: url={self.NPM_PACKAGE_LIST_URL}')
            return []
                        
        # If the response returns an error, return an empty list
        try:
            data = job.response.json()
        except Exception as e:
            MyLogger().get_logger().debug(f'EXCEPTION at __download_page: url={self.NPM_PACKAGE_LIST_URL}')
            MyLogger().get_logger().debug(f'Error parsing JSON: {e}')
            MyLogger().get_logger().debug(f'Response: {job.response.text}')
            MyLogger().get_logger().debug(f'Params: {params}')
            MyLogger().get_logger().debug(f'Retrying, times left: {retries}')
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

            # Add the dependency to the list
            dep_list.append({
                'name': dep_name,
                'version': dep_version
            })

        return {
            'name': package_name,
            'version': package_version,
            'dependencies': dep_list,
            'url': f'{self.NPM_REPO_URL}/{package_name}'
        }

    
    