from typing import List
import logging
import random
import requests


class UserAgentHandler():
    '''Handles useragents'''

    # Useragents list
    useragents = []

    def __init__(self):

        # Load useragents from file
        loaded_with_file = False
        try:
            with open('useragents.txt', 'r') as f:
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
        
        # Get useragents from the user-agents.net API
        url = 'https://user-agents.net/download'
        params = {'browser': 'google', 'download': 'json'}

        response = requests.post(url, params=params)

        if response.status_code == 200:
            print(response.content)
        else:
            print('Error en la petición:', response.status_code)

    def get_next_useragent(self) -> str:

        # Get a random useragent
        index = random.randint(0, len(self.useragents) - 1)
        useragent = self.useragents[index]

        return useragent



    
