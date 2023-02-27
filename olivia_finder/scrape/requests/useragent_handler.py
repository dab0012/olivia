from typing import List
import logging
import random
from bs4 import BeautifulSoup
import requests


class UserAgentHandler():
    '''Handles useragents'''

    USERAGENTSTRING_URL = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'

    # Useragents list
    useragents = []

    def __init__(self):

        # Load useragents from file
        loaded_with_file = False
        try:
            with open('olivia_finder/data/useragents.txt', 'r') as f:
                self.useragents = f.read().split('\n')
                loaded_with_file = True
        except FileNotFoundError:
            logging.info('Useragents file not found. Loading from web.')

        # Load useragents from web
        if not loaded_with_file:
            self.useragents = self.load_from_API()

        # If the list is empty, return default useragent
        if len(self.useragents) == 0:
            self.useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36']

    def get_useragents(self) -> List[str]:
        return self.useragents
    
    def load_from_file(self, file_path:str) -> List[str]:
        with open(file_path, 'r') as f:
            return f.read().split('\n')
    
    def load_from_API(self) -> List[str]:
        
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

        ua_list = []

        # Get user agents
        # Be careful with the request!!!
        try:
            user_agents_request = requests.get(self.USERAGENTSTRING_URL).text
        except Exception as e:
            logging.warning("Error getting user agents (RequestHandler.__obtain_user_agents): ", e)
            return []
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(user_agents_request, 'html.parser')
            div = soup.find(id="liste")     # Find the div element with id = liste
            lis = div.find_all("li")        # Search for all li elements within the div element

            # Stores user agents in a list
            for li in lis:
                # Add the user agent to the list            
                ua = li.text
                ua_list.append(ua)

            return ua_list

        
        except Exception as e:
            logging.warning("Error parsing user agents (RequestHandler.load_from_API): ", e)
            return []


    def get_next_useragent(self) -> str:

        # Get a random useragent
        index = random.randint(0, len(self.useragents) - 1)
        useragent = self.useragents[index]

        return useragent



    
