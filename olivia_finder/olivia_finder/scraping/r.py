'''
File:              r.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 7:01:45 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from typing_extensions import override
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.scraping.scraper import Scraper
from olivia_finder.util.logger import UtilLogger

class RScraper(Scraper, ABC):
    '''
    Abstract class that implements the common methods for scraping R repositories
    
    Parameters
    ----------
    name : str
        The name of the data source
    description : str
        The description of the data source
    request_handler : RequestHandler
        The request handler to perform the requests to the package manager website 
    '''
    
    def __init__(
        self, 
        name: Optional[str] = None, 
        description: Optional[str] = None, 
        request_handler: Optional[RequestHandler] = None
    ):
        '''
        Constructor of the class
        '''
        super().__init__(name, description, request_handler)

    def __parse_dependencies(self, dependencies_str: str) -> List[Dict[str, str]]:
        '''
        Parse the dependencies string and return a list of tuples with the name and version of each dependency
        This method is used common of all the scrapers that implement this class so it is private and it is called from the
        child implementation of the method _Scraper__parser

        Parameters
        ----------
        dependencies_str : str
            The dependencies string

        Returns
        -------
        List[Tuple[str, str]]
            A list of tuples with the name and version of each dependency        
        '''

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else '' for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', name.strip()) for name in dependencies_str.split(",")]

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or not names:
            return []

        return [
            {'name': names[i], 'version': versions[i]} for i in range(len(names))
        ]

    @abstractmethod
    def obtain_package_names(self) -> List[Dict[str, str]]:
        pass