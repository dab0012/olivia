'''
File:              proxy_builder.py
Project:           Olivia-Finder
Created Date:      Monday February 27th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Monday February 27th 2023 7:38:04 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup
import requests
from ..util import UtilLogger

class ProxyBuilder(ABC):
    '''
    Interface for proxy builders
    
    The ProxyBuilder interface defines the methods that must be implemented by
    proxy builders specific implementations.
    '''

    def __init__(self, proxy_list_timeout=20, logger=None):
        '''
        Constructor

        Parameters
        ----------
        proxy_list_timeout : int, optional
            Timeout for proxy list requests, by default 20
        logger : logging.Logger, optional
            Logger to use, by default None
        '''
        self.proxy_list_timeout = proxy_list_timeout
        self.logger = logger
        
    def get_proxies(self) -> List[str]:
        '''
        Returns a list of proxies from the proxy list URL

        Returns
        -------
        List[str]
            List of proxies
        '''

        # Do the request
        try:
            response = requests.get(self.URL, timeout=self.proxy_list_timeout)
        except requests.exceptions.RequestException as e:
            UtilLogger.log(f"Error getting proxies from {self.__class__.__name__}")
            UtilLogger.log(f"Error: {e}")
            return []
        
        # Parse the response
        proxies = []
        if response.status_code == 200:
            proxies = self.parse(response)
            UtilLogger.log(f"Found {len(proxies)} proxies from {self.__class__.__name__}")
        else:
            UtilLogger.log(f"Error getting proxies from {self.__class__.__name__}")
            UtilLogger.log(f"Request returned status code: {response.status_code}")

        return proxies

    @abstractmethod
    def parse(self, request: requests.Response) -> List[str]:
        '''
        Parses the proxy list, it must be implemented by subclasses
        '''
        pass

# --------------------------------------------------------------------------------
# Proxy builders implementations
# --------------------------------------------------------------------------------

class SSLProxies(ProxyBuilder):
    '''
    Proxy builder for SSLProxies.org
    This class implements the ProxyBuilder interface.
    It gets a list of proxies from https://www.sslproxies.org/
    '''
    URL = 'https://www.sslproxies.org/'
    
    def parse(self, response: requests.Response) -> List[str]:
        '''
        Parses the proxy list

        Parameters
        ----------
        text : str
            Text to parse

        Returns
        -------
        List[str]
            List of proxies
        '''
        proxies = []

        # Get the table using beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')
        tbody = soup.find('tbody')

        # iterate over the rows getting the data
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')

            # add the proxy to the list
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")
        
        return proxies
        
class FreeProxyList(ProxyBuilder):
    '''
    Proxy builder for FreeProxyList.net
    This class implements the ProxyBuilder interface.
    It gets a list of proxies from https://free-proxy-list.net/anonymous-proxy.html
    '''

    URL = 'https://free-proxy-list.net/anonymous-proxy.html'

    def parse(self, response:requests.Response) -> List[str]:
        '''
        Parses the proxy list

        Parameters
        ----------
        text : str
            Text to parse

        Returns
        -------
        List[str]
            List of proxies
        '''
        proxies = []

        # Get the table using beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('tbody')

        # iterate over the rows getting the data
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')

            # add the proxy to the list
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")

        return proxies

class GeonodeProxy(ProxyBuilder):
    '''
    Proxy builder for GeonodeProxy
    This class implements the ProxyBuilder interface.
    It gets a list of proxies from https://proxylist.geonode.com/
    '''

    URL = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'

    def parse(self, response:requests.Response) -> List[str]:
        '''
        Parses the proxy list

        Parameters
        ----------
        response : requests.Response
            Response to parse
        
        Returns
        -------
        List[str]
            List of proxies
        '''
        proxies = []
        
        # Get the json
        json = response.json()

        # Iterate over the proxies
        for proxy in json['data']:
            ip = proxy['ip']
            port = proxy['port']
            proxies.append(f"{ip}:{port}")

        return proxies
