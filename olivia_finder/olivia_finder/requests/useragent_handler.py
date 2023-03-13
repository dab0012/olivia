'''
File:              useragent_handler.py
Project:           Olivia-Finder
Created Date:      Monday February 27th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Monday February 27th 2023 7:38:04 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from typing import List
import logging, random, requests
from bs4 import BeautifulSoup
from ..util.logger import UtilLogger
from ..util.config_ini import Configuration
from ..util.util import Util

class UserAgentHandler():
    '''Handles useragents'''

    # Attributes
    # ----------------
    USERAGENTSTRING_URL = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    DATA_FILE: str

    useragents_list: List[str]
    my_logger: logging.Logger

    def __init__(self) -> None:
        '''
        Constructor

        Parameters
        ----------
        useragents_file_path : str, optional
            Path to the file containing the useragents, by default None
        '''

        self.DATA_FILE = Configuration().get_key("folders", "data_dir") + "useragents.txt"

        if self._load_from_file(self.DATA_FILE):
            UtilLogger.log(f"Useragents loaded from file: {self.DATA_FILE}")
            return

        if self._load_from_api():
            UtilLogger.log(f"Useragents loaded from API: {self.USERAGENTSTRING_URL}")
            return

        # If the list is empty, return default useragent
        self.useragents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36']
        UtilLogger.log("Useragents list is empty. Using default useragent")

    def _load_from_file(self, file_path:str) -> bool:
        '''
        Load user agents from a file
        Parameters
        ----------
        file_path : str
            Path to the file containing the user agents
        Returns
        -------
        bool
            True if the user agents were loaded correctly, False otherwise
        '''

        if file_path is None:
            return False

        try:
            with open(file_path, 'r') as f:
                self.useragents_list = f.read().split('\n')
                return True
            
        except FileNotFoundError:
            UtilLogger.log(f"Useragents file not found: {file_path}")
            return False
    
    def _load_from_api(self) -> bool:
        
        '''
        Get user agents from the useragentstring.com API and save them in the user agent list
        Parameters
        ----------
        max_count : int, optional
            Maximum number of user agents to be obtained, by default 30
        Returns
        -------
        bool
            True if the user agents were obtained correctly, False otherwise
        '''

        # Get user agents from the API
        try:
            user_agents_request = requests.get(self.USERAGENTSTRING_URL).text
        except Exception as e:
            UtilLogger.log(f"Error getting user agents from API: {self.USERAGENTSTRING_URL}")
            UtilLogger.log(f"Error: {e}")
            return False
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(user_agents_request, 'html.parser')
            div = soup.find(id="liste")     # Find the div element with id = liste
            lis = div.find_all("li")        # Search for all li elements within the div element

            # Stores user agents in a list
            for li in lis:
                # Add the user agent to the list            
                ua = Util.clean_string(li.text)
                self.useragents_list.append(ua)
            return True
        
        except Exception as e:
            UtilLogger.log(f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}")
            UtilLogger.log(f"Error: {e}")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list

        Returns
        -------
        str
            A random useragent
        '''
        UtilLogger.log("Getting next useragent")
        # Get a random useragent
        index = random.randint(0, len(self.useragents_list) - 1)
        return self.useragents_list[index]
