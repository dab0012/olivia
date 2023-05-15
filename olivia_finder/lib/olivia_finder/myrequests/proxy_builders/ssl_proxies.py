from typing_extensions import override
from bs4 import BeautifulSoup
import requests
from ..proxy_builder import ProxyBuilder


class SSLProxiesBuilder(ProxyBuilder):
    '''
    SSLProxies proxy builder, gets the proxies from https://www.sslproxies.org/
    Implements the abstract method _parse_request to parse the response 
    '''
    
    def __init__(self, request_timeout: int = 60):
        super().__init__(
            url="https://www.sslproxies.org/", 
            request_timeout=request_timeout
        )
    
    @override
    def _parse_request(self, response: requests.Response) -> list[str]:
        '''
        Parse the response and return a list of proxies
        Expected data:

        <tbody>
            <tr>
                <td>35.247.248.104</td>
                <td>3129</td><td>BR</td>
                <td class="hm">Brazil</td>
                <td>anonymous</td>
                <td class="hm"></td>
                <td class="hx">yes</td>
                <td class="hm">22 secs ago</td>
            </tr>
            ...
        </tbody>

        Parameters
        ----------
        response : requests.Response
            The response of the request

        Returns
        -------
        list[str]
            A list of proxies            
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