from abc import ABC, abstractmethod
from typing import List
import requests

class ProxyBuilder(ABC):
    '''Builds a list of proxies'''

    def __init__(self, proxy_list_timeout=20):
        self.proxy_list_timeout = proxy_list_timeout
        
    @abstractmethod
    def get_proxies(self) -> List[str]:
        pass

# Proxy builders implementations
# --------------------------------

class SSLProxies(ProxyBuilder):
    def get_proxies(self) -> List[str]:
        url = 'https://www.sslproxies.org/'
        response = requests.get(url)
        proxies = []
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                if '<tbody>' in line:
                    start = True
                elif '</tbody>' in line:
                    break
                elif start:
                    if '<td>' in line:
                        ip = line.split('<td>')[1].split('</td>')[0]
                        port = line.split('<td>')[2].split('</td>')[0]
                        proxies.append(f"{ip}:{port}")
        return proxies

class FreeProxyList(ProxyBuilder):
    def get_proxies(self) -> List[str]:
        url = 'https://free-proxy-list.net/anonymous-proxy.html'
        response = requests.get(url)
        proxies = []
        if response.status_code == 200:
            lines = response.text.split('\n')
            start = False
            for line in lines:
                if '<tbody>' in line:
                    start = True
                elif '</tbody>' in line:
                    break
                elif start:
                    if '<td>' in line:
                        ip = line.split('<td>')[0]
                        port = line.split('<td>')[1]
                        proxies.append(f"{ip}:{port}")
        return proxies
    
class GeonodeProxy(ProxyBuilder):

    def get_proxies(self) -> List[str]:
        url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'
        response = requests.get(url, timeout=self.proxy_list_timeout)
        proxies = []
        if response.status_code == 200:
            json_data = response.json()
            for proxy in json_data['data']:
                proxies.append(f"{proxy['ip']}:{proxy['port']}")
        return proxies

class NoProxy(ProxyBuilder):
    def get_proxies(self) -> List[str]:
        return []