from typing_extensions import override
import requests
from .proxy_builder import ProxyBuilder


class ListProxyBuilder(ProxyBuilder):
    '''
    A generic proxy builder implementation, gets the proxies from a list in the format ip:port

    Parameters
    ----------
    url : str
        URL of the proxy list website to get the proxies
    request_timeout : int
        Timeout for the proxy list requests
        
    Raises
    ------
    ValueError
        If url parameter is None
    '''

    TIMEOUT = 60
    
    def __init__(self, url:str, request_timeout: int = TIMEOUT):
        '''
        Constructor
        '''

        super().__init__(
            url=url, 
            request_timeout=request_timeout
        )
    
    @override
    def _parse_request(self, response: requests.Response) -> list[str]:
        '''
        Parse the response and return a list of proxies
        Expected data:

        81.4.102.223:8081
        35.247.228.52:3129
        20.121.242.93:3128
        35.247.234.213:3129
        35.247.248.45:3129
        35.247.248.46:3129
        35.247.240.117:3129
        35.247.254.240:3129
        35.247.197.252:3129
        35.247.246.68:3129

        Parameters
        ----------
        response : requests.Response
            The response of the request

        Returns
        -------
        list[str]
            A list of proxies
        '''

        data = response.text.splitlines()
        return [] if data is None else data
        


