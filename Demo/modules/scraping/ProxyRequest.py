# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

import requests
import random
from bs4 import BeautifulSoup
from typing import Dict
from modules.Util import *

class RequestHandler(requests.Request):
    ''' 
    Class to handle HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested
    Basically, it manages the proxies and user agents so that scraping is not detected
    '''

    def __init__(self, max_request=5, *args, **kwargs):
        '''
        Class constructor

        Parameters
        ----------
        max_request : int, optional
            Maximum number of requests to be made with the same proxy, by default 5
        *args : tuple
            Arguments to be passed to the parent class
        **kwargs : dict
            Keyword arguments to be passed to the parent class

        Returns
        -------
            None
        '''

        # Call the constructor of the parent class
        super().__init__(*args, **kwargs)

        self.proxies = {}                   # Initialize the proxy list
        self.user_agents = []               # Initialize the user agent list
        self.max_request = max_request      # Maximum number of requests to be made with the same proxy

    def __obtain_proxies(self) -> None:
        '''
        Get proxies from proxyscrape.com API using the free plan and save them in the proxy list
        '''

        # get proxy
        proxies = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all').text
        proxies = proxies.splitlines()

        # Save (proxy, number_uses) in proxy list
        self.proxies = [(f'http://{proxy}', 0) for proxy in proxies]

    def __get_next_proxy(self) -> Dict[str, str]:
        '''
        Get next proxy from the proxy list

        Returns
        -------
        Dict[str, str]
            Dictionary with the proxy, in the format {'http': 'http://ip:port'} used in the requests library

        '''

        # If the proxy list is empty, get new proxies
        if not self.proxies:
            self.__obtain_proxies()

        # Select the next proxy
        selected_proxy, num_usages = self.proxies[0]

        # If the proxy has already been used the specified number of times, remove it from the proxy list
        num_usages+=1
        if num_usages == self.max_request:

            # Remove the tuple proxy from the proxy list
            self.proxies.remove((selected_proxy, num_usages-1))

        # If not, update the number of proxy uses
        else:
            self.proxies[0] = (selected_proxy, num_usages)

        # return proxy
        return { 'http': selected_proxy }

    def __obtain_user_agents(self, max_count=30) -> None:
        '''
        Get user agents from the useragentstring.com API and save them in the user agent list
        '''
        # obtenerUserAgents
        user_agents_request = requests.get('https://www.useragentstring.com/pages/useragentstring.php?name=All').text
        soup = BeautifulSoup(user_agents_request, 'html.parser')

        div = soup.find(id="liste")     # Find the div element with id = liste
        lis = div.find_all("li")        # Search for all li elements within the div element

        # Stores user agents in a list
        count = 0
        for li in lis:

            # You only get the first 30 user agents
            if count == max_count:
                break

            # Add the user agent to the list            
            user_agent = li.text
            self.user_agents.append(user_agent)
            count+=1

    def __get_random_user_agent(self) -> Dict[str, str]:
        '''
        Get a random user agent from the user agent list

        Returns
        -------
        Dict[str, str]
            Dictionary with the user agent, in the format {'User-Agent': 'user agent'} used in the requests library
        '''

        # If the User Agents list is empty, get new user agents
        if self.user_agents == []:
            self.__obtain_user_agents()
        
        selected_user_agent = random.choice(self.user_agents)       # Select a random UserAgent
        self.user_agents.remove(selected_user_agent)                # Delete the User Agent from the list

        return {'User-Agent': selected_user_agent}

    def do_request(self, url, retry = False) -> bytes:
        '''
        Make an HTTP request and return the HTML of the response

        args:
            url (str): URL of the request

        Returns:
            bytes: HTML of the response
        '''
        try:

            # Get proxy and user agent
            proxy = self.__get_next_proxy()
            user_agent = self.__get_random_user_agent()

            # Make HTTP request
            response = requests.get(url, proxies=proxy, headers=user_agent, timeout=10)

            if retry:
                retry_count = 0

                # If the request fails, retry it
                while response.status_code != 200:

                    print_colored("Request failed as response:", RED)
                    print_colored("Proxy: " + str(proxy), RED)
                    print_colored("User agent: " + str(user_agent), RED)
                    print_colored("URL: " + url, RED)
                    print_colored("Error: " + str(response.status_code), RED)
                    print_colored("Retrying request", RED)
                    
                    response = requests.get(url, proxies=proxy, headers=user_agent, timeout=10)

                    # If the request fails 5 times in a row, change the proxy and user agent
                    if retry_count % 5 == 0:
                        print("Request failed 5 times. Changing proxy and user agent")
                        proxy = self.__get_next_proxy()
                        user_agent = self.__get_random_user_agent()
             
                    # Increment retry count
                    retry_count+=1

        except Exception as e:

            # Color red
            print_colored("Request failed as Exception:", RED)
            print_colored("Proxy: " + str(proxy), RED)
            print_colored("User agent: " + str(user_agent), RED)
            print_colored("URL: " + url, RED)
            print_colored("Error: " + str(e), RED)
            print_colored("Retrying request", RED)

            # Renew proxy and user agent
            proxy = self.__get_next_proxy()
            user_agent = self.__get_random_user_agent()

            # If the request fails, retry it
            response = self.do_request(url, retry=True)

        # return HTML
        return response
