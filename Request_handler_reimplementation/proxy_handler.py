from __future__ import annotations
from abc import ABC
import logging 
from proxy_builder import NoProxy, ProxyBuilder

class ProxyHandler(ABC):
    '''Handles proxy rotation and proxy usage'''

    # Contains a list of tuples (proxy, uses)
    proxy_uses = {}
    proxy_list = []
    # Default proxy builder (no proxy)
    proxy_builder = NoProxy()

    def __init__(self, proxy_builder: ProxyBuilder = proxy_builder, proxy_max_uses=20):
        self.proxy_max_uses = proxy_max_uses
        self.proxy_builder = proxy_builder
        self.proxy_list = self.proxy_builder.get_proxies()

    def get_next_proxy(self):

        # Check if proxies are empty and get new ones
        if len(self.proxy_list) == 0:
            self.proxy_list = self.proxy_builder.get_proxies()

        # Check if proxies are still empty
        if len(self.proxy_list) == 0:
            logging.warning("No proxies available")
            logging.warning("Proceeding without proxies")
            return None

        # proxy rotation
        proxy = self.proxy_list[0]
        self.proxy_list = self.proxy_list[1:]
        
        # Handle proxy usage lifetime
        self.handle_lifetime(proxy)

        return proxy
    
    def handle_lifetime(self, proxy):
        if proxy in self.proxy_uses:
            self.proxy_uses[proxy] += 1
        else:
            self.proxy_uses[proxy] = 1

        # remove proxy if it has been used more than the limit
        if self.proxy_uses[proxy] > self.proxy_max_uses:
            del self.proxy_uses[proxy]
  