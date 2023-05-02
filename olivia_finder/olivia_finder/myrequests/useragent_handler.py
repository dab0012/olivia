import os
from threading import Lock
import random
import requests
from bs4 import BeautifulSoup
from  ..utilities.logger import MyLogger
from singleton_decorator import singleton

@singleton
class UserAgentHandler():
    '''UserAgentHandler class'''
    # Attributes
    # ----------
    
    USERAGENTSTRING_URL = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    DATA_FILE: str
    useragents_list: list[str]

    def __init__(self, use_file: bool = True) -> None:

        # Lock to prevent concurrent access to the proxy list
        self.lock = Lock()

        # Initialize the list before loading the user agents
        self.useragents_list = []

        # Load user agents from file
        if use_file:
            # get the data file path
            current_file_path =  os.path.abspath(__file__)
            self.DATA_FILE = os.path.join(os.path.dirname(current_file_path), 'data', 'useragents.txt')

            if self._load_from_file(self.DATA_FILE):
                MyLogger().get_logger().info(f"Useragents loaded from file: {self.DATA_FILE}")
                return

        # Load user agents from the useragentstring.com API
        if self._load_from_useragentstring():
            MyLogger().get_logger().info(f"Useragents loaded from USERAGENTSTRING_URL: {self.USERAGENTSTRING_URL}")
            return

        # If at this time there are no uses available, the default useragents are loaded using the list
        # hardcodeted below
        self.useragents_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
            'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
        ]
        MyLogger().get_logger().info("Useragents list is empty. Using default useragents")

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
            MyLogger().get_logger().warning(f"Useragents file not found: {file_path}")
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

        MyLogger().get_logger().debug(f"Getting user agents from API: {self.USERAGENTSTRING_URL}")

        # Get user agents from the API
        try:
            user_agents_request = requests.get(self.USERAGENTSTRING_URL, timeout=60).text
        except Exception as e:
            MyLogger().get_logger().debug(f"Error getting user agents from API: {self.USERAGENTSTRING_URL}")
            MyLogger().get_logger().debug(f"Error: {e}")
            return False
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(user_agents_request, 'html.parser')
            div = soup.find(id="liste")     # Find the div element with id = liste
            lis = div.find_all("li")        # Search for all li elements within the div element

            # Stores user agents in a list
            for li in lis:
                # Add the user agent to the list (cleaning the blanks from the string)     
                ua = li.text.strip()
                self.useragents_list.append(ua)
            return True
        
        except Exception as e:
            MyLogger().get_logger().warning(f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}")
            MyLogger().get_logger().warning(f"Error: {e}")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list

        Returns
        -------
        str
            A random useragent
        '''
        # Get a random useragent
        index = random.randint(0, len(self.useragents_list) - 1)

        MyLogger().get_logger().debug(f"Next useragent: {self.useragents_list[index]}")
        return self.useragents_list[index]
