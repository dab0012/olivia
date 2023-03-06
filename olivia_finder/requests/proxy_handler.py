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

from logging import Logger
from typing import List, Optional, Union 
from olivia_finder.requests.proxy_builder import ProxyBuilder
from olivia_finder.util import UtilLogger

class ProxyHandler():
    '''Handles proxy rotation and proxy usage'''

    # Attributes
    PROXY_MAX_USES: int = 50                    # Maximum number of uses for each proxy
    proxy_builders: List[ProxyBuilder] = []     # List of proxy builders
    proxy_list: List[str] = []                  # proxy_list is a list str with the proxies
    proxy_uses: dict = {}                       # A dictionary with the number of uses for each proxy, uses the proxy as key
    logger: Optional[Logger] = None                       # Logger to use

    def __init__(self, 
                 builders: List[ProxyBuilder] = None, 
                 proxy_max_uses: int = PROXY_MAX_USES, 
                 logger: Logger = None
                ):
        '''
        Constructor

        Parameters
        ----------
        builders : List[ProxyBuilder]
            List of proxy builders
        proxy_max_uses : int, optional
            Maximum number of uses for each proxy, by default 50
        logger : logging.Logger, optional
            Logger to use, by default None
        '''
        
        # Set attributes
        self.logger = logger                                # Set logger
        self.PROXY_MAX_USES = proxy_max_uses                # Set proxy max uses
        if builders is None:                                # Set proxy builder, load default if none is provided
            self.proxy_builders = self._get_available_builders()
        else:
            # Check if builders are valid
            for builder in builders:
                if not isinstance(builder, ProxyBuilder):
                    raise TypeError(f"Invalid builder type: {type(builder)}")
            self.proxy_builders = builders

        # Get proxies from builder
        self.proxy_list = self._get_proxies()

        if self.logger is not None:
            UtilLogger.logg(self.logger, f"Proxy Handler initialized with {len(self.proxy_list)} proxies", "DEBUG")
            UtilLogger.logg(self.logger, f"Buidlers: {self.proxy_builders}", "DEBUG")



    def get_next_proxy(self) -> Union[str, None]:
        '''
        Get next proxy from the list and rotate it to the end of the list

        Returns
        -------
        Union[str, None]
            Next proxy or None if there are no proxies
        '''
        UtilLogger.logg(self.logger, "Getting next proxy", "DEBUG")

        # Check if proxies are empty and get new ones
        if len(self.proxy_list) == 0:
            UtilLogger.logg(self.logger, "No proxies available, trying to get new ones", "DEBUG")
            self.proxy_list = self._get_proxies()

        # Check if proxies are still empty
        if len(self.proxy_list) == 0:
            UtilLogger.logg(self.logger, "No proxies available after trying to get new ones", "DEBUG")
            return None

        # proxy rotation
        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        UtilLogger.logg(self.logger, f"Proxy list rotated, new: {self.proxy_list[0]}", "DEBUG")

        # Handle proxy usage lifetime
        self.handle_lifetime(proxy)

        # return proxy as fstring
        return f"http://{proxy}"
    
    def handle_lifetime(self, proxy: str) -> None:
        '''
        Handle proxy usage lifetime, if proxy has been used more than the limit it is removed from the list

        Parameters
        ----------
        proxy : str
            Proxy to handle
        '''
        # add proxy to dict if it is not there or increase its usage
        if proxy in self.proxy_uses:
            self.proxy_uses[proxy] += 1
        else:
            self.proxy_uses[proxy] = 1

        # remove proxy if it has been used more than the limit
        if self.proxy_uses[proxy] > self.PROXY_MAX_USES:
            del self.proxy_uses[proxy]
            self.proxy_list.remove(proxy)
            UtilLogger.logg(self.logger, f"Proxy {proxy} removed from list", "DEBUG")


    def _get_proxies(self) -> List[str]:
        '''
        Get proxies from builders defined in the constructor and return a list of unique proxies
        
        Returns
        -------
        List[str]
            List of proxies
        '''
        proxies = []
        for builder in self.proxy_builders:
            proxies += builder.get_proxies()

        # remove duplicates
        proxies = list(set(proxies))

        if self.logger is not None:
            UtilLogger.logg(self.logger, f"Proxies len: {len(proxies)}", "DEBUG")

        return proxies
    
    def _get_available_builders(self) -> Union[List[ProxyBuilder], None]:
        '''
        Get available proxy builders as a list of ProxyBuilder objects

        Returns
        -------
        List[ProxyBuilder]
            List of ProxyBuilder objects
        '''
        builders = []
        for builder in ProxyBuilder.__subclasses__():

            # append builder object
            builders.append(builder())
            UtilLogger.logg(self.logger, f"Added {builder.__name__} to proxy builders", "DEBUG")

        return builders