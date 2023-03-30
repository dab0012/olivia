'''
r.py
====

Description
-----------

Module that contains the abstract class that implements the common methods of the scraper implementations 
for Bioconductor and CRAN

File information:
    - File: r.py
    - Project: scrapers
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

import re
from typing import Dict, List, Optional
from typing_extensions import override
from ..scraper import Scraper
from ...myrequests.request_handler import RequestHandler

class RScraper(Scraper):
    '''
    Class that implements the common methods of the scraper implementations for Bioconductor and CRAN
    
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

    def _parse_dependencies(self, dependencies_str: str) -> List[Dict[str, str]]:
        '''
        Parses the dependencies string and returns a list of dictionaries with the name and version of each dependency

        Parameters
        ----------
        dependencies_str : str
            The dependencies string

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries with the name and version of each dependency    
        '''

        # Remove unnecessary line breaks, tabs, and spaces
        pattern = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versions = [re.findall(pattern, dep)[0] if re.findall(pattern, dep) else None for dep in dependencies_str.split(",")]
        names = [re.sub(r'\s*\(.*\)', '', name.strip()) for name in dependencies_str.split(",")]

        # Check if the lists have the same length and are not empty
        if len(names) != len(versions) or not names:
            return []

        return [
            {'name': names[i], 'version': versions[i]} for i in range(len(names))
        ]
