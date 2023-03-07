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
from olivia_finder.util import Util, UtilConfig, UtilLogger

class UserAgentHandler():
    '''Handles useragents'''

    # Attributes
    # ----------------
    USERAGENTSTRING_URL                 =   'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    useragents_list: List[str]
    LOGER: logging.Logger
    DATA_FILE: str

    def __init__(self) -> None:
        '''
        Constructor

        Parameters
        ----------
        useragents_file_path : str, optional
            Path to the file containing the useragents, by default None
        '''

        loaded_with_file = loaded_with_api = False
        self.DATA_FILE = UtilConfig.get_value_config_file("folders", "data_dir") + "useragents.txt"

        # Load useragents from file
        loaded_with_file = self._load_from_file(self.DATA_FILE)
        if loaded_with_file:
            UtilLogger.logg(f"Useragents loaded from file: {self.DATA_FILE}")
            return

        # Load useragents from web
        loaded_with_api = self._load_from_api()
        if loaded_with_api:
            UtilLogger.logg(f"Useragents loaded from API: {self.USERAGENTSTRING_URL}")
            return

        # If the list is empty, return default useragent
        self.useragents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36']
        UtilLogger.logg("Useragents list is empty. Using default useragent")

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
            UtilLogger.logg(f"Useragents file not found: {file_path}")
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
            UtilLogger.logg(f"Error getting user agents from API: {self.USERAGENTSTRING_URL}")
            UtilLogger.logg(f"Error: {e}")
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
            UtilLogger.logg(f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}")
            UtilLogger.logg(f"Error: {e}")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list

        Returns
        -------
        str
            A random useragent
        '''
        UtilLogger.logg("Getting next useragent")
        # Get a random useragent
        index = random.randint(0, len(self.useragents_list) - 1)
        return self.useragents_list[index]
