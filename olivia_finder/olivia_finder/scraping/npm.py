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
from typing_extensions import override
from typing import List, Optional
from tqdm import tqdm
from olivia_finder.scraping.scraper import Scraper
from olivia_finder.util.config_ini import Configuration
from olivia_finder.util.logger import UtilLogger
from olivia_finder.requests.request_handler import RequestHandler

class NpmScraper(Scraper):
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
        super().__init__(name, description, request_handler)

    @override
    def obtain_package_names(
        self, 
        page_size: Optional[int]=100, 
        save_chunks: Optional[bool]=False,
        show_progress_bar: Optional[bool]=True
    ) -> List[dict]:

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
        List[dict]
            List of dictionaries with the name and version of the packages
        
        Examples
        --------
        >>> scraper = NpmScraper()
        >>> scraper.obtain_package_names()
        '''
        # Get the total number of packages
        # response = requests.get(self.NPM_PACKAGE_REGISTRY_URL)
        response = self.request_handler.do_request(self.NPM_PACKAGE_REGISTRY_URL)[1]
        total_packages = response.json()['doc_count']

        # Calculate the number of pages (chunks)
        num_pages = (total_packages // page_size) + 1

        # Initialize the progress bar if is set
        progress_bar = tqdm(total=num_pages) if show_progress_bar else None
        
        # Initialize the chunks folder if is set
        self.__init_chunks_folder() if save_chunks else None

        # Obtain the names of the packages requesting the pages
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

            # Update progress bar if is set
            progress_bar.update(1) if show_progress_bar else None

        return [row['id'] for page in pages for row in page]

    #region Private methods

    def __init_chunks_folder(self):
        '''
        Function to initialize the chunks folder, where the chunks will be saved
        Loads the path from the configuration file
        '''
        self.chunks_folder = f'{Configuration.get_key("folders", "working_dir")}/npm'
        os.makedirs(self.chunks_folder, exist_ok=True)

    def __download_page(
        self, 
        start_key: Optional[str]=None, 
        size: Optional[int]=1000, 
        retries: Optional[int]=5
    )-> List[dict]:
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
        List[dict]
            List of dictionaries with the name and version of the packages
        '''

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
    
    @override
    def _Scraper__build_url(self, package_name: str):
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
    def _Scraper__parser(self, response: requests.Response) -> dict:
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

    #endregion