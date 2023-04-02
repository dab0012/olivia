import os
from typing import List
import random
import requests
from bs4 import BeautifulSoup
from ..util.logger import MyLogger
from ..util.util import Util

class UserAgentHandler():
    '''
    Handles useragents for the requests

    Attributes
    ----------
    USERAGENTSTRING_URL : str
        URL to get user agents from the useragentstring.com API
    DATA_FILE : str
        file containing the user agents in txt format
    useragents_list : List[str]
        List of user agents

    '''

    # Attributes
    # ----------------
    USERAGENTSTRING_URL = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    '''URL to get user agents from the useragentstring.com API'''
    DATA_FILE: str
    '''Path to the file containing the user agents'''

    useragents_list: List[str]

    def __init__(self) -> None:
        '''
        Constructor
        '''

        # Initialize the list before loading the user agents
        self.useragents_list = []

        # get the data file path
        current_file_path =  os.path.abspath(__file__)
        self.DATA_FILE = os.path.join(os.path.dirname(current_file_path), 'data', 'useragents.txt')

        if self._load_from_file(self.DATA_FILE):
            MyLogger.log(f"Useragents loaded from file: {self.DATA_FILE}")
            return

        if self._load_from_useragentstring():
            MyLogger.log(f"Useragents loaded from API: {self.USERAGENTSTRING_URL}")
            return

        # If the list is empty, return default useragent
        self.useragents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36']
        MyLogger.log("Useragents list is empty. Using default useragent")

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
            MyLogger.log(f"Useragents file not found: {file_path}")
            return False
    
    def _load_from_useragentstring(self) -> bool:
        
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
            user_agents_request = requests.get(self.USERAGENTSTRING_URL, timeout=60).text
        except Exception as e:
            MyLogger.log(f"Error getting user agents from API: {self.USERAGENTSTRING_URL}")
            MyLogger.log(f"Error: {e}")
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
            MyLogger.log(f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}")
            MyLogger.log(f"Error: {e}")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list

        Returns
        -------
        str
            A random useragent
        '''
        MyLogger.log("Getting next useragent")
        # Get a random useragent
        index = random.randint(0, len(self.useragents_list) - 1)
        return self.useragents_list[index]
