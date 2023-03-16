""""""
from __future__ import annotations

'''
·········································································
File: proxy_builder.py
Project: Olivia-Finder
Created Date: Monday February 27th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''

import requests
from typing import List
from bs4 import BeautifulSoup
from typing_extensions import override
from abc import ABC, abstractmethod
from olivia_finder.util.logger import UtilLogger

class ProxyBuilder(ABC):
    '''
    Interface for proxy builders implementations.
    The ProxyBuilder interface defines the methods that must be implemented by
    proxy builders specific implementations.
    
    Parameters
    ----------
    proxy_list_timeout : int, optional
        Timeout for the proxy list requests, by default ProxyBuilder.DEFAULT_TIMEOUT
    
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import SSLProxies
    >>> ssl_proxies = SSLProxies()
    >>> ssl_proxies.get_proxies()
    '''
    
    DEFAULT_TIMEOUT = 60    # Default timeout for proxy list requests

    def __init__(self, proxy_list_timeout=DEFAULT_TIMEOUT):
        '''Constructor'''

        self.proxy_list_timeout = proxy_list_timeout
        
    def get_proxies(self) -> List[str]:
        '''
        Do a request to the proxy list URL and returns a list of proxies if the request is successful,
        otherwise returns an empty list

        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request fails for any reason
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
            proxies = self.__parse_request(response)
            UtilLogger.log(f"Found {len(proxies)} proxies from {self.__class__.__name__}")
        else:
            UtilLogger.log(f"Error getting proxies from {self.__class__.__name__}")
            UtilLogger.log(f"Request returned status code: {response.status_code}")

        return proxies

    @abstractmethod
    def __parse_request(self, request: requests.Response) -> List[str]:
        '''
        Parses the proxy list, it must be implemented by subclasses
        
        Parameters
        ----------
        request : requests.Response
            Request response to parse for extracting the proxies
        
        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request was not successful
        '''
        pass

# ------------------------------------------------
#region Proxy builders implementations

class SSLProxies(ProxyBuilder):
    '''
    Proxy builder for SSLProxies.org
    This class implements the ProxyBuilder interface.
    It gets a list of proxies from https://www.sslproxies.org/
    
    Attributes
    ----------
    URL : str
        URL of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import SSLProxies
    >>> ssl_proxies = SSLProxies()
    >>> ssl_proxies.get_proxies()
    '''
    
    URL = 'https://www.sslproxies.org/'
    
    @override
    def _ProxyBuilder__parse_request(self, response: requests.Response) -> List[str]:
        '''
        Parses the proxy list from the response, returns a list of proxies in string format {ip}:{port}
        Overrides the ProxyBuilder.parse method
        
        Parameters
        ----------
        response : requests.Response
            Request response to parse for extracting the proxies 
        
        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request was not successful
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
    
    Attributes
    ----------
    URL : str
        URL of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import FreeProxyList
    >>> free_proxy_list = FreeProxyList()
    >>> free_proxy_list.get_proxies()
    '''

    # URL of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    URL = 'https://free-proxy-list.net/anonymous-proxy.html'

    @override
    def _ProxyBuilder__parse_request(self, response:requests.Response) -> List[str]:
        '''
        Parses the proxy list from the response, returns a list of proxies in string format {ip}:{port}
        Overrides the ProxyBuilder.parse method

        Parameters
        ----------
        response : requests.Response
            Request response to parse for extracting the proxies
            
        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request was not successful
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
    
    Attributes
    ----------
    URL : str
        URL of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
        
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import GeonodeProxy
    >>> geonode_proxy = GeonodeProxy()
    >>> geonode_proxy.get_proxies()
    '''

    # URL of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    URL = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'

    @override
    def _ProxyBuilder__parse_request(self, response:requests.Response) -> List[str]:
        '''
        Parses the proxy list from the response, returns a list of proxies in string format {ip}:{port}
        Overrides the ProxyBuilder.parse method
        
        Parameters
        ----------
        response : requests.Response
            Request response to parse for extracting the proxies

        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request was not successful
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
    
    #endregion