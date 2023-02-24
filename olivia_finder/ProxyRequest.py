# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: Olivia Finder
# Description: This module implements the request handler class to handle HTTP requests

import requests
import random
from bs4 import BeautifulSoup
from typing import Dict, Union
from .LoadConfig import logging

class RequestHandler():
    ''' 
    Class to handle HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested
    Basically, it manages the proxies and user agents so that scraping is not detected
    '''

    def __init__(self, max_request=5):
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

        self.proxies = {}                   # Initialize the proxy list
        self.user_agents = []               # Initialize the user agent list
        self.max_request = max_request      # Maximum number of requests to be made with the same proxy

        # URL of the proxyscape API
        self.proxyscape_url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all'

        # URL of the useragentstring API
        self.useragentstring_url = 'https://www.useragentstring.com/pages/useragentstring.php?name=All'


    def __obtain_proxies(self) -> bool:
        '''
        Get proxies from proxyscrape.com API using the free plan and save them in the proxy list

        Returns
        -------
        bool
            True if the proxies were obtained correctly, False otherwise
        '''

        # Get proxy
        # Be careful with the request!!!
        try:
            proxies = requests.get(self.proxyscape_url).text
        except Exception as e:
            logging.warning("Error getting proxies (RequestHandler.__obtain_proxies): ", e)
            return False
        
        # Save (proxy, number_uses) in proxy list
        proxies = proxies.splitlines()
        self.proxies = [(f'http://{proxy}', 0) for proxy in proxies]
        return True

    def __get_next_proxy(self) -> Union[Dict[str, str], None]:
        '''
        Get next proxy from the proxy list

        Returns
        -------
        Dict[str, str]
            Dictionary with the proxy, in the format {'http': 'http://ip:port'} used in the requests library

        '''

        # If the proxy list is empty, get new proxies
        if not self.proxies:

            # Try to get the proxies 5 times from the API
            # If it fails, use the default IP
            requests_count = 0
            while not self.__obtain_proxies():
                requests_count+=1
                if requests_count == 5:
                    logging.warning("Error getting proxies: failed 5 times (RequestHandler.__get_next_proxy)")
                    logging.warning("Using default IP")
                    return None

        # Select the next proxy
        selected_proxy, num_usages = self.proxies[0]

        # If the proxy has already been used the specified number of times, remove it from the proxy list
        num_usages+=1
        if num_usages == self.max_request:
            self.proxies.remove((selected_proxy, num_usages-1))

        # If not, update the number of proxy uses
        else:
            self.proxies[0] = (selected_proxy, num_usages)

        return { 'http': selected_proxy }

    def __obtain_user_agents(self, max_count=30) -> bool:
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
        # Get user agents
        # Be careful with the request!!!
        try:
            user_agents_request = requests.get(self.useragentstring_url).text
        except Exception as e:
            logging.warning("Error getting user agents (RequestHandler.__obtain_user_agents): ", e)
            return False
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(user_agents_request, 'html.parser')
            div = soup.find(id="liste")     # Find the div element with id = liste
            lis = div.find_all("li")        # Search for all li elements within the div element

            # Stores user agents in a list
            count = 0
            for li in lis:
                if count == max_count:
                    break

                # Add the user agent to the list            
                user_agent = li.text
                self.user_agents.append(user_agent)
                count+=1

            return True
        
        except Exception as e:
            logging.warning("Error parsing user agents (RequestHandler.__obtain_user_agents): ", e)
            return False

    def __get_next_user_agent(self) -> Dict[str, str]:
        '''
        Get a random user agent from the user agent list

        Returns
        -------
        Dict[str, str]
            Dictionary with the user agent, in the format {'User-Agent': 'user agent'} used in the requests library
        '''

        # If the User Agents list is empty, get new user agents
        if self.user_agents == []:

            # Try to get the user agents 5 times from the API
            # If it fails, use the default user agent
            requests_count = 0
            while not self.__obtain_user_agents():
                requests_count+=1
                if requests_count == 5:
                    logging.warning("Error getting user agents: failed 5 times (RequestHandler.__get_next_user_agent)")
                    logging.warning("Using default user agent")
                    return {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        selected_user_agent = random.choice(self.user_agents)       # Select a random UserAgent

        # Delete the User Agent from the list if throw a coin and it is heads
        # This is done to avoid using the same User Agent multiple times and to avoid useragentstring.com blocking the IP
        # while making requests to the API
        if random.randint(0, 1) == 0:
            self.user_agents.remove(selected_user_agent)

        return {'User-Agent': selected_user_agent}

    def do_request(self, url: str, max_retry = 5) -> Union[requests.Response, None]:
        '''
        Make an HTTP request and return the HTML of the response

        args:
            url (str): URL of the request
            max_retry (int): Maximum number of retries if the request fails

        Returns:
            Union[requests.Response, None]: Response of the request or None if the request fails
        '''

        finalized = False
        retry_count = 0
        
        while not finalized:
            # Get proxy and user agent
            proxy = self.__get_next_proxy()
            user_agent = self.__get_next_user_agent()

            # Make HTTP request
            try:
                response = requests.get(url, proxies=proxy, headers=user_agent)
                finalized = True
            except Exception as e:
                logging.warning("Error making request (RequestHandler.do_request): ", e)
                retry_count+=1

                # If the request fails <max_retry> times, return None
                if retry_count == max_retry:
                    logging.warning("Error making request: failed 5 times (RequestHandler.do_request)")
                    return None

        return response
