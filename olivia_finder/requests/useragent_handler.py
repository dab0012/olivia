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
from olivia_finder.util import Util, UtilLogger

class UserAgentHandler():
    '''Handles useragents'''

    # Attributes
    # ----------------
    USERAGENTSTRING_URL                 =   'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    useragents_list: List[str]          =   []
    LOGER: logging.Logger               =   None

    def __init__(self, useragents_file_path: str = None, logger: logging.Logger = None) -> None:
        '''
        Constructor

        Parameters
        ----------
        useragents_file_path : str, optional
            Path to the file containing the useragents, by default None
        '''
        self.LOGER = logger

        loaded_with_file = loaded_with_api = False

        # Load useragents from file
        loaded_with_file = self._load_from_file(useragents_file_path)
        if loaded_with_file:
            UtilLogger.logg(self.LOGER, f"Useragents loaded from file: {useragents_file_path}", "DEBUG")
            return

        # Load useragents from web
        loaded_with_api = self._load_from_API()
        if loaded_with_api:
            UtilLogger.logg(self.LOGER, f"Useragents loaded from API: {self.USERAGENTSTRING_URL}", "DEBUG")
            return

        # If the list is empty, return default useragent
        self.useragents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36']
        UtilLogger.logg(self.LOGER, f"Useragents list empty. Using default useragent", "DEBUG")

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
            UtilLogger.logg(self.LOGER, f"Useragents file not found: {file_path}", "DEBUG")
            return False
    
    def _load_from_API(self) -> bool:
        
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
            UtilLogger.logg(self.LOGER, f"Error getting user agents from API: {self.USERAGENTSTRING_URL}", "DEBUG")
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
            UtilLogger.logg(self.LOGER, f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}", "DEBUG")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list

        Returns
        -------
        str
            A random useragent
        '''
        UtilLogger.logg(self.LOGER, f"Getting random useragent", "DEBUG")
        # Get a random useragent
        index = random.randint(0, len(self.useragents_list) - 1)
        return self.useragents_list[index]
