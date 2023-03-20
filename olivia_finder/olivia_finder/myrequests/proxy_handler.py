'''
proxy_handler.py
==================

Description
-----------

Module proxy_handler that contains the functions to handle the proxy rotation.
It uses a list of proxy builders to get the proxies.
It is a utility class for the RequestHandler class.

File information:
    - File: proxy_handler.py
    - Project: myrequests
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''

from typing import List, Optional, Union 
from .proxy_builder import ProxyBuilder, ProxyBuilderABC
from ..util.logger import MyLogger

class ProxyHandler():
    '''
    Handles proxy rotation and proxy usage, it uses a list of proxy builders to get the proxies
    Its a utility class for the RequestHandler class
        
    Attributes
    ----------
    PROXY_MAX_USES : int
        Maximum number of uses for each proxy
    proxy_builders : List[ProxyBuilderABC]
        List of proxy builders
    proxy_list : List[str]
        proxy_list is a list str with the proxies
    proxy_uses : dict
        A dictionary with the number of uses for each proxy, uses the proxy as key
    '''

    # Attributes
    proxy_max_uses: int = 50                    # Maximum number of uses for each proxy
    proxy_builders: List[ProxyBuilderABC] = []     # List of proxy builders
    proxy_list: List[str] = []                  # proxy_list is a list str with the proxies
    proxy_uses: dict = {}                       # A dictionary with the number of uses for each proxy, uses the proxy as key

    def __init__(
        self,
        builders: Optional[List[ProxyBuilderABC]] = None, 
        proxy_max_uses: Optional[int] = 50
    ):
        '''Constructor'''

        # Set attributes
        self.proxy_max_uses = proxy_max_uses                # override default value

        # Set proxy builders, if none, get default builders
        if builders is None:                                
            self.proxy_builders = self.__get_available_builders()
        else:
            # Check if builders are valid
            for builder in builders:
                # if any of the builders is not valid, ignore and continue with the next one
                if not isinstance(builder, ProxyBuilderABC):
                    MyLogger.log(f"Builder {builder} is not a valid ProxyBuilderABC, ignoring")
                    continue
                else:
                    MyLogger.log(f"Builder {builder} is valid, adding to list")
                    self.proxy_builders.append(builder)
            
            # Check if any builder is valid
            if len(self.proxy_builders) == 0:
                MyLogger.log("No valid proxy builders were provided")
                raise ValueError("No valid proxy builders were provided")

            # Set builders
            self.proxy_builders = builders

        # Get proxies from builder
        self.proxy_list = self.__request_proxies()
        MyLogger.log(f"Proxy Handler initialized with {len(self.proxy_list)} proxies")

    def get_next_proxy(self) -> Union[str, None]:
        '''
        Get theb next proxy from the proxies list and rotate it to the end of the list

        :return: Next proxy as str f'http://{ip}:{port}' or None if there are no proxies available
        :rtype: Union[str, None]
        '''
        MyLogger.log("Getting next proxy")

        # Check if proxies are empty and get new ones
        if len(self.proxy_list) == 0:
            MyLogger.log("No proxies available, trying to get new ones")
            self.proxy_list = self.__request_proxies()

        # Check if proxies are still empty
        if len(self.proxy_list) == 0:
            MyLogger.log("No proxies available after trying to get new ones")
            return None

        # proxy rotation
        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        MyLogger.log(f"Proxy list rotated, using {proxy}, next will be {self.proxy_list[0]}")

        # Handle proxy usage lifetime
        self.__handle_lifetime(proxy)

        # return proxy as fstring
        return f"http://{proxy}"
    
    # ----------------------------------------------------
    #region Private methods
    
    def __handle_lifetime(self, proxy: str):
        '''
        Handle proxy usage lifetime, if proxy has been used more than the limit it is removed from the list
        Removes the proxy from the dict and the list

        Parameters
        ----------
        proxy : str
            Proxy as str f'http://{ip}:{port}'    
        '''
        # add proxy to dict if it is not there or increase its usage           
        if proxy not in self.proxy_uses:
            self.proxy_uses[proxy] = 1
        else:
            self.proxy_uses[proxy] += 1

        # remove proxy if it has been used more than the limit
        if self.proxy_uses[proxy] > self.proxy_max_uses:
            del self.proxy_uses[proxy]
            self.proxy_list.remove(proxy)
            MyLogger.log(f"Proxy {proxy} removed from list")

    def __request_proxies(self) -> List[str]:
        '''
        Get proxies from builders defined in the constructor and return a list of unique proxies
        
        Returns
        -------
        List[str]
            List of proxies as str f'http://{ip}:{port}'
        '''
        # Load the proxie list from the builders
        proxies = []
        for builder in self.proxy_builders:
            proxies += builder.get_proxies()

        # remove duplicates
        proxies = list(set(proxies))
        MyLogger.log(f"Proxies len: {len(proxies)}")

        return proxies
    
    def __get_available_builders(self) -> Union[List[ProxyBuilderABC], None]:
        '''
        Get available proxy builders as a list of ProxyBuilder objects

        Returns
        -------
        Union[List[ProxyBuilder], None]
            List of ProxyBuilder objects or None if there are no builders
        '''
        builders = []
        for builder in ProxyBuilder.__subclasses__():

            # append builder object
            builders.append(builder())
            MyLogger.log(f"Added {builder.__name__} to proxy builders")

        return builders
    
    #endregion Private methods
