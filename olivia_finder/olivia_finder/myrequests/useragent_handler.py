"""

.. danger:: 

    Remove the @singleton decorator before documenting the class
    Doc fails with the @singleton decorator

"""

import os
from threading import Lock
import random
from typing import List
import requests
from bs4 import BeautifulSoup
from ..utilities.logger import MyLogger
from ..utilities.singleton_decorator import singleton
from ..utilities.config import Configuration


@singleton
class UserAgentHandler():
    '''
    UserAgentHandler class

    This class is a singleton class that handles the user agents used by the requests
    to the different data sources. It can load the user agents from a file or from the
    useragentstring.com API. 
    
    If the user agents are loaded from a file, the file must be located in the data
    folder of the package and must be named useragents.txt. The file must contain one
    user agent per line.

    If the user agents are loaded from the useragentstring.com API, the user agents
    are loaded from the URL specified in the class variable USERAGENTSTRING_URL. The
    user agents are loaded from the page https://www.useragentstring.com/pages/useragentstring.php?name=All
    and the user agents are extracted from the table in the page. 

    
    Attributes
    ----------
    USERAGENTSTRING_URL : str
        The URL of the page with the list of user agents
    DATA_FILE : str
        The path to the file with the user agents
    useragents_list : List[str]
        The list of user agents loaded from the file or from the useragentstring.com API,
        default is an empty list that will be filled with the default user agents if the
        user agents cannot be loaded from the external sources
    '''

   
    
    USERAGENTSTRING_URL = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'
    DATA_FILE: str
    useragents_list: List[str]

    def __init__(self, use_file: bool = True) -> None:
        '''
        Constructor

        Parameters
        ----------
        use_file : bool = True
            If True, the user agents are loaded from the file specified in the class variable DATA_FILE.
            If False, the user agents are loaded from the useragentstring.com API.

        '''

        # Get logger name from config file
        self.logger = MyLogger.get_logger(
            Configuration().get_key("logger_myrequests", "name")
        )

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
                self.logger.info(f"Useragents loaded from file: {self.DATA_FILE}")
                return

        # Load user agents from the useragentstring.com API
        if self._load_from_useragentstring():
            self.logger.info(f"Useragents loaded from USERAGENTSTRING_URL: {self.USERAGENTSTRING_URL}")
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
        self.logger.info("Useragents list is empty. Using default useragents")

    def _load_from_file(self, file_path:str) -> bool:
        '''
        Load user agents from a file, one user agent per line, and save them in the user agent list

        Parameters
        ----------
        file_path : str
            Path to the file containing the user agents

        Returns
        -------
        bool
            True if the user agents were loaded correctly, False otherwise

        Examples
        --------
        >>> useragent_handler = UserAgentHandler()
        >>> useragent_handler._load_from_file('data/useragents.txt')
            True
        '''

        if file_path is None:
            return False

        try:
            with open(file_path, 'r') as f:
                self.useragents_list = f.read().split('\n')
                return True
            
        except FileNotFoundError:
            self.logger.warning(f"Useragents file not found: {file_path}")
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

        self.logger.debug(f"Getting user agents from API: {self.USERAGENTSTRING_URL}")

        # Get user agents from the API
        try:
            user_agents_request = requests.get(self.USERAGENTSTRING_URL, timeout=60).text
        except Exception as e:
            self.logger.debug(f"Error getting user agents from API: {self.USERAGENTSTRING_URL}")
            self.logger.debug(f"Error: {e}")
            return False
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(user_agents_request, 'html.parser')
            div = soup.find(id="liste")     # Find the div element with id = liste
            lis = div.find_all("li")        # type: ignore # Search for all li elements within the div element

            # Stores user agents in a list
            for li in lis:
                # Add the user agent to the list (cleaning the blanks from the string)     
                ua = li.text.strip()
                self.useragents_list.append(ua)
            return True
        
        except Exception as e:
            self.logger.warning(f"Error parsing user agents from API: {self.USERAGENTSTRING_URL}")
            self.logger.warning(f"Error: {e}")
            return False

    def get_next_useragent(self) -> str:
        '''
        Returns a random useragent from the list, if the list is empty, returns a default useragent

        Returns
        -------

        str
            A random useragent
        '''

        # If the list is empty, return a default useragent (THIS SHOULD NOT HAPPEN)
        if len(self.useragents_list) == 0:
            self.logger.warning("Useragents list is empty")
            return "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

        index = random.randint(0, len(self.useragents_list) - 1)
        self.logger.debug(f"Next useragent: {self.useragents_list[index]}")
        return self.useragents_list[index]
