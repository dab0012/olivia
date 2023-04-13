'''
proxy_builder.py
==================

Description
-----------

Module that contains ...

File information:
    - File: proxy_builder.py
    - Project: myrequests
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

from __future__ import annotations
from typing import List, Optional
from abc import ABC, abstractmethod
from typing_extensions import override
import requests
from bs4 import BeautifulSoup
from ..utilities.logger import MyLogger


class ProxyBuilder(ABC):
    '''
    Base class for proxy builders implementations. It musn't be used directly.
    The correct way to use it is to instantiate a subclass of this class where the
    URL attribute is defined and the _parse_request method is implemented.
    
    Parameters
    ----------
    url : str
        URL of the proxy list website to get the proxies
    proxy_list_timeout : Optional[int], optional
        Timeout for the proxy list requests, by default 60
    '''

    
    def __init__(
        self, url: str = None, proxy_list_timeout: Optional[int] = None
    ):
        
        # Check if this clas is not instantiated directly
        if self.__class__ == ProxyBuilder:
            raise TypeError("ProxyBuilder can't be instantiated directly, use a subclass instead")

        # URL of the proxy list website to get the proxies
        if url is None:
            raise ValueError("url parameter can't be None")
        self.url = url

        # Timeout for the proxy list requests
        self.proxy_list_timeout = proxy_list_timeout


    def get_proxies(self) -> List[str]:
        '''
        Do a request to the proxy list URL and returns a list of proxies if the request is successful,
        otherwise returns an empty list

        Returns
        -------
        List[str]
            List of proxies in string format {ip}:{port} or an empty list if the request fails for any reason

        Examples
        --------
        >>> from olivia_finder.requests.proxy_builder import ProxyBuilder
        >>> proxy_builder = ProxyBuilder(url="https://www.sslproxies.org/")
        >>> proxy_builder.get_proxies()
        [
            ip:port,
            ip:port
        ]
        '''

        # Do the request
        try:
            response = requests.get(self.url, timeout=self.proxy_list_timeout)
        except requests.exceptions.RequestException as e:
            MyLogger.log(f"Error getting proxies from {self.__class__.__name__}")
            MyLogger.log(f"Error: {e}")
            return []
        
        # Parse the response
        proxies = []
        if response.status_code == 200:
            proxies = self._parse_request(response)
            MyLogger.log(f"Found {len(proxies)} proxies from {self.__class__.__name__}")
        else:
            MyLogger.log(f"Error getting proxies from {self.__class__.__name__}")
            MyLogger.log(f"Request returned status code: {response.status_code}")

        return proxies
    
    @abstractmethod
    def _parse_request(self, response: requests.Response) -> List[str]:
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
        raise NotImplementedError

class SSLProxies(ProxyBuilder):
    '''
    Proxy builder for SSLProxies.org
    This class implements the ProxyBuilder interface.
    It gets a list of proxies from https://www.sslproxies.org/
    
    Attributes
    ----------
    url : str
        url of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import SSLProxies
    >>> ssl_proxies = SSLProxies()
    >>> ssl_proxies.get_proxies()
    [
        ip:port,
        ip:port,
        ...
    ]
    '''
    
    def __init__(self, proxy_list_timeout: Optional[int] = 60):
        super().__init__(url="https://www.sslproxies.org/", proxy_list_timeout=proxy_list_timeout)
    
    @override
    def _parse_request(self, response: requests.Response) -> List[str]:
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
        
        Examples
        --------
        >>> from olivia_finder.requests.proxy_builder import SSLProxies
        >>> ssl_proxies = SSLProxies()
        >>> ssl_proxies.get_proxies()
        [
            ip:port,
            ip:port,
            ...
        ]
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
    url : str
        url of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
    
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import FreeProxyList
    >>> free_proxy_list = FreeProxyList()
    >>> free_proxy_list.get_proxies()
    [
        ip:port,
        ip:port,
        ...
    ]
    '''

    def __init__(self, proxy_list_timeout: Optional[int] = 60):
        super().__init__(
            url='https://free-proxy-list.net/anonymous-proxy.html', 
            proxy_list_timeout=proxy_list_timeout
        )
        
    @override
    def _parse_request(self, response:requests.Response) -> List[str]:
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

        Examples
        --------
        >>> from olivia_finder.requests.proxy_builder import FreeProxyList
        >>> free_proxy_list = FreeProxyList()
        >>> free_proxy_list.get_proxies()
        [
            ip:port,
            ip:port,
            ...
        ]
        '''
        # Define the list of proxies
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
    url : str
        url of the proxy list website to get the proxies, its used by the get_proxies method at the ProxyBuilder class
        
    Examples
    --------
    >>> from olivia_finder.requests.proxy_builder import GeonodeProxy
    >>> geonode_proxy = GeonodeProxy()
    >>> geonode_proxy.get_proxies()
    [
        ip:port,
        ip:port,
        ...
    ]
    '''

    def __init__(self, proxy_list_timeout: Optional[int] = 60):
        super().__init__(
            url='https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc',
            proxy_list_timeout=proxy_list_timeout
        )
        
    @override
    def _parse_request(self, response:requests.Response) -> List[str]:
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

        Examples
        --------
        >>> from olivia_finder.requests.proxy_builder import GeonodeProxy
        >>> geonode_proxy = GeonodeProxy()
        >>> geonode_proxy.get_proxies()
        [
            ip:port,
            ip:port,
            ...
        ]
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
    
