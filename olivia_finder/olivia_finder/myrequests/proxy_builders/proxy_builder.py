
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import requests

from ...utilities.config import Configuration
from ...utilities.logger import MyLogger

class ProxyBuilder(ABC):
    '''
    Abstract class to represent a proxy builder

    .. warning::
        This class can't be instantiated directly, use a subclass instead

            
    - :class:`olivia_finder.myrequests.proxy_builders.ssl_proxies.SSLProxiesBuilder`
    - :class:`olivia_finder.myrequests.proxy_builders.list_builder.ListProxyBuilder`

    '''

    def __init__(self, url: str = None, request_timeout: int = None):
        '''
        Constructor
        
        Parameters
        ----------
        url : str
            URL of the proxy list website to get the proxies
        request_timeout : int
            Timeout for the proxy list requests
        '''
        
        # Get logger name from config file
        self.logger = MyLogger.get_logger(
            Configuration().get_key('logger', 'myrequests_name')
        )

        # Check if this clas is not instantiated directly
        if self.__class__ == ProxyBuilder:
            raise TypeError("ProxyBuilder can't be instantiated directly, use a subclass instead")

        # URL of the proxy list website to get the proxies
        if url is None:
            raise ValueError("url parameter can't be None")
        self.url = url

        # Timeout for the proxy list requests
        self.request_timeout = request_timeout

    def get_proxies(self) -> List[str]:
        '''
        Get the proxies from the website, parse the response and return a list of proxies

        Returns
        -------
        List[str]
            A list of proxies

        Raises
        ------
        Exception
            If there is an error getting the proxies

        Examples
        --------
        >>> from proxy_builders.ssl_proxies import SSLProxies
        >>> ssl_proxies = SSLProxies()
        >>> proxies = ssl_proxies.get_proxies()
        '''

        # Do the request, if there is an error return an empty list
        try:
            response = requests.get(self.url, timeout=self.request_timeout)
        except Exception as e:
            message = f"Error getting proxies from {self.__class__.__name__}: {e}"
            message += f"URL: {self.url}"
            self.logger.error(message)
            return []
        
        # Reesponse is OK, parse the response and return the proxies
        proxies = []
        if response.status_code == 200:
            proxies = self._parse_request(response)
            self.logger.debug(f"Found {len(proxies)} proxies from {self.__class__.__name__}")
        else:
            message = f"Error getting proxies from {self.__class__.__name__}"
            message += f"Request returned status code: {response.status_code}"
            self.logger.error(message)

        return proxies
    
    @abstractmethod
    def _parse_request(self, response: requests.Response) -> List[str]:
        '''
        Abstract method to parse the response from the request

        Parameters
        ----------
        response : requests.Response
            The response from the request

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass

        Returns
        -------
        List[str]
            A list of proxies
        '''

        raise NotImplementedError


        
