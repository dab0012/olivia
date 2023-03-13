'''
File:              proxy_handler.py
Project:           Olivia-Finder
Created Date:      Monday February 27th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Monday February 27th 2023 7:38:04 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from typing import List, Optional, Union 
from olivia_finder.requests.proxy_builder import ProxyBuilder
from olivia_finder.util.logger import UtilLogger

class ProxyHandler():
    '''
    Handles proxy rotation and proxy usage, it uses a list of proxy builders to get the proxies
    Its a utility class for the RequestHandler class
        
    :param builders: List of proxy builders, defaults to None
    :type builders: List[ProxyBuilder], optional
    :param proxy_max_uses: Maximum number of uses for each proxy, defaults to PROXY_MAX_USES
    :type proxy_max_uses: int, optional
    :return: ProxyHandler
    :rtype: ProxyHandler
    :raises TypeError: If a builder of builders param is not a ProxyBuilder instance
    '''

    # Attributes
    PROXY_MAX_USES: int = 50                    # Maximum number of uses for each proxy
    proxy_builders: List[ProxyBuilder] = []     # List of proxy builders
    proxy_list: List[str] = []                  # proxy_list is a list str with the proxies
    proxy_uses: dict = {}                       # A dictionary with the number of uses for each proxy, uses the proxy as key

    def __init__(
        self,
        builders: Optional[List[ProxyBuilder]]  = None, 
        proxy_max_uses: Optional[int]           = PROXY_MAX_USES, 
    ):
        '''Constructor'''

        # Set attributes
        self.PROXY_MAX_USES = proxy_max_uses                # override default value

        # Set proxy builders, if none, get default builders
        if builders is None:                                
            self.proxy_builders = self.__get_available_builders()
        else:
            # Check if builders are valid
            for builder in builders:
                if not isinstance(builder, ProxyBuilder):
                    raise TypeError(f"Invalid builder type: {type(builder)}")
            # Set builders
            self.proxy_builders = builders

        # Get proxies from builder
        self.proxy_list = self.__request_proxies()
        UtilLogger.log(f"Proxy Handler initialized with {len(self.proxy_list)} proxies")
        UtilLogger.log(f"Buidlers: {self.proxy_builders}")

    def get_next_proxy(self) -> Union[str, None]:
        '''
        Get theb next proxy from the proxies list and rotate it to the end of the list

        :return: Next proxy as str f'http://{ip}:{port}' or None if there are no proxies available
        :rtype: Union[str, None]
        '''
        UtilLogger.log("Getting next proxy")

        # Check if proxies are empty and get new ones
        if len(self.proxy_list) == 0:
            UtilLogger.log("No proxies available, trying to get new ones")
            self.proxy_list = self.__request_proxies()

        # Check if proxies are still empty
        if len(self.proxy_list) == 0:
            UtilLogger.log("No proxies available after trying to get new ones")
            return None

        # proxy rotation
        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        UtilLogger.log(f"Proxy list rotated, new: {self.proxy_list[0]}")

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
        self.proxy_uses[proxy] += 1 if proxy in self.proxy_uses else 1

        # remove proxy if it has been used more than the limit
        if self.proxy_uses[proxy] > self.PROXY_MAX_USES:
            del self.proxy_uses[proxy]
            self.proxy_list.remove(proxy)
            UtilLogger.log(f"Proxy {proxy} removed from list")

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
        UtilLogger.log(f"Proxies len: {len(proxies)}")

        return proxies
    
    def __get_available_builders(self) -> Union[List[ProxyBuilder], None]:
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
            UtilLogger.log(f"Added {builder.__name__} to proxy builders")

        return builders
    
    #endregion Private methods
