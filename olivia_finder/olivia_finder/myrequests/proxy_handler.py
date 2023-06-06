from threading import Lock
from typing import List, Optional, Union
from .proxy_builders.proxy_builder import ProxyBuilder
from .proxy_builders.ssl_proxies import SSLProxiesBuilder
from .proxy_builders.list_builder import ListProxyBuilder 
from ..utilities.logger import MyLogger
from ..utilities.singleton_decorator import singleton
from ..utilities.config import Configuration

@singleton
class ProxyHandler():
    '''
    ProxyHandler class, handles the proxies, gets them from the builders and rotates them

    Parameters
    ----------
    builders : List[ProxyBuilder]
        List of proxy builders to get the proxies, if None, get the default builders
    proxy_max_uses : int
        Maximum number of uses for a proxy before it is removed from the list

        
    Attributes
    ----------
    proxy_list : List[str]
        List of proxies, each proxy is a string in the format ip:port, has to be accessed with a lock
    proxy_uses : dict
        A dictionary with the number of uses for each proxy, uses the proxy as key, has to be accessed with a lock
    proxy_builders : List[ProxyBuilder]
        List of proxy builders to get the proxies, has to be accessed with a lock
    lock : threading.Lock
        Lock to prevent concurrent access to the proxy list

    Raises
    ------
    ValueError
        If there is no valid proxy builder   

    '''

    PROXY_MAX_USES = 50

    def __init__(
        self,
        builders: Optional[List[ProxyBuilder]] = None,
        proxy_max_uses: int = PROXY_MAX_USES
    ):
        '''Constructor'''

        # Lock to prevent concurrent access to the proxy list
        self.lock = Lock()

        # Get logger name from config file
        self.logger = MyLogger.get_logger(
            Configuration().get_key("logger_myrequests", "name")
        )

        # Set attributes
        self.proxy_max_uses = proxy_max_uses             # override default value
        self.proxy_list: List[str] = []                  # proxy_list is a list str with the proxies
        self.proxy_uses: dict = {}                       # A dictionary with the number of uses for each proxy, uses the proxy as key
        self.proxy_builders: List[ProxyBuilder] = []     # List of proxy builders

        # Set proxy builders, if none, get default builders
        if builders is None:                                
            self.proxy_builders = self._get_available_builders()
        else:
            # Check if builders are valid
            for builder in builders:
                # if any of the builders is not valid, ignore and continue with the next one
                if not isinstance(builder, ProxyBuilder):
                    self.logger.debug(f"Builder {builder} is not a valid ProxyBuilderABC, ignoring")
                else:
                    self.logger.debug(f"Builder {builder} is valid, adding to list")
                    self.proxy_builders.append(builder)
            
            # Check if any builder is valid
            if len(self.proxy_builders) == 0:
                self.logger.debug("No valid proxy builders were provided")
                raise ValueError("No valid proxy builders were provided")

            # Set builders
            self.proxy_builders = builders

        # Get proxies from builder
        self.proxy_list = self._request_proxies()
        self.logger.info(f"Proxy Handler initialized with {len(self.proxy_list)} proxies")

    def get_next_proxy(self) -> Union[str, None]:
        '''
        Get the next proxy from the proxies list and rotate it to the end of the list

        Returns
        -------
        str
            The next proxy
            
        Examples
        --------
        >>> from proxy_handler import ProxyHandler
        >>> proxy_handler = ProxyHandler()
        >>> proxy = proxy_handler.get_next_proxy()
            'http://1.1.1.1:8080'
        '''

        # Check if proxies are empty and get new ones
        if len(self.proxy_list) == 0:
            self.logger.info("No proxies available, trying to get new ones")
            self.proxy_list = self._request_proxies()

        # Check if proxies are still empty
        if len(self.proxy_list) == 0:
            self.logger.warning("No proxies available after trying to get new ones")
            return None

        # proxy rotation
        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        self.logger.debug(f"Next proxy: {proxy}")

        # Handle proxy usage lifetime
        self._handle_lifetime(proxy)

        # return proxy as fstring
        return f"http://{proxy}"
    
    def _handle_lifetime(self, proxy: str):
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
            self.logger.debug(f"Proxy {proxy} removed from list")

    def _request_proxies(self) -> List[str]:
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
        self.logger.debug(f"Proxies len: {len(proxies)}")

        return proxies
    
    def _get_available_builders(self) -> List[ProxyBuilder]:
        '''
        Get available proxy builders as a list of ProxyBuilder objects

        Returns
        -------
        Union[List[ProxyBuilder], None]
            List of ProxyBuilder objects or None if there are no builders

        '''

        # Get available builders
        return [
            SSLProxiesBuilder(),
            ListProxyBuilder(url="https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"),
            ListProxyBuilder(url="https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")
        ]

        
    

