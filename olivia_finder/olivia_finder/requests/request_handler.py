'''
File:              request_handler.py
Project:           Olivia-Finder
Created Date:      Monday February 27th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Monday February 27th 2023 7:38:04 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import tqdm
from typing import List, Optional, Tuple, Union
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..util import UtilLogger, UtilMultiThreading
from .proxy_handler import ProxyHandler
from .useragent_handler import UserAgentHandler
import requests

class RequestHandler:
    '''
    Class that handles HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested 
    Basically, it manages the proxies and user agents so that scraping is not detected
    '''
    # Attributes
    # ----------
    proxy_handler: ProxyHandler                            # Proxy handler to use
    useragents_handler: UserAgentHandler                   # User agent handler to use
    current_proxy_index: int                               # Current proxy index
    current_useragent_index: int                           # Current user agent index
    LOCK: Lock                                             # Lock to use
    REQUEST_MAX_RETRIES: int                    = 5        # Maximum number of retries for each request
    REQUEST_TIMEOUT: int                        = 30       # Timeout for each request
    NUM_PROCESSES: int                          = 4        # Number of processes to use for parallel requests

    def __init__(
        self, 
        proxy_handler:          Optional[ProxyHandler] = None, 
        useragents_handler:     Optional[UserAgentHandler] = None, 
        max_retry:              Optional[int] = REQUEST_MAX_RETRIES, 
        request_timeout:        Optional[int] = REQUEST_TIMEOUT, 
        num_processes:          Optional[int] = NUM_PROCESSES, 
    ):
        '''
        Constructor

        ---
        Parameters
        
        -   proxy_handler: ProxyHandler, optional           -> Proxy handler to use, by default None
        -   useragents_handler: UserAgentHandler, optional  -> User agent handler to use, by default None
        -   max_retry: int, optional                        -> Maximum number of retries for each request, by default REQUEST_MAX_RETRIES
        -   request_timeout: int, optional                  -> Timeout for each request, by default REQUEST_TIMEOUT
        -   num_processes: int, optional                    -> Number of processes to use for parallel requests, by default NUM_PROCESSES
        '''

        # Check proxy handler
        if proxy_handler is None:
            self.proxy_handler = ProxyHandler()
        else:
            self.proxy_handler = proxy_handler

        # Check user agent handler
        if useragents_handler is None:
            self.useragents_handler = UserAgentHandler()
        else:
            self.useragents_handler = useragents_handler

        # Initialize attributes
        self.LOCK = Lock()
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.REQUEST_MAX_RETRIES = max_retry
        self.REQUEST_TIMEOUT = request_timeout

        # Check number of processes
        recommended_num_processes = UtilMultiThreading.recommended_threads()
        if num_processes > recommended_num_processes:
            UtilLogger.log(f"Number of processes ({num_processes}) is greater than the recommended number ({recommended_num_processes}).")
            self.NUM_PROCESSES = recommended_num_processes
        elif num_processes < 1:
            raise ValueError("num_processes must be greater than 0")
        else:
            self.NUM_PROCESSES = num_processes

    def do_request(self, url:str, params:dict = None) -> Union[Tuple[str, requests.Response], None]:
        '''
        Do a request to the given url
        
        Parameters
        ----------
        url : str
            URL to do the request
        params : dict, optional
            Parameters to pass to the request, by default None
            
        Returns
        -------
        Union[Tuple[str, requests.Response], None]
            Tuple with the url and the response if the request was successful, None otherwise
            
        Raises
        ------
        RequestError
            Exception doing request
        '''

        # Try to get proxy and user agent with lock for thread safety
        proxy = headers = None
        try:
            with self.LOCK:
                if self.proxy_handler is not None:
                    proxy_url = self.proxy_handler.get_next_proxy()
                    proxy = {"http": proxy_url}
                    UtilLogger.log(f"Using proxy: {proxy}")
                if self.useragents_handler is not None:
                    headers = {'User-Agent': self.useragents_handler.get_next_useragent()}
                    UtilLogger.log(f"Using user agent: {headers['User-Agent']}")
        except Exception as e:
            raise RequestError(url, f"Exception getting proxy and user agent: {e}") from e

        # Do the request
        response = None
        try:
            with requests.Session() as session:
                response = session.get(
                    url, 
                    headers=headers,
                    proxies=proxy, 
                    timeout=self.REQUEST_TIMEOUT, 
                    params=params
                )

            # Response is ok
            UtilLogger.log(f"Response status code: {response.status_code}")
            return (url, response)
                   
        # Handle exceptions
        except Exception as e:
            raise RequestError(response, f"Exception doing request: {e}") from e
      
    def do_parallel_requests(self, url_list:List[str], param_list:List[dict] = None, progress_bar:tqdm.tqdm = None):
        '''
        Do parallel requests to the given urls

        Parameters
        ----------
        url_list : List[str]
            List of urls to do the requests
        param_list : List[dict], optional
            List of parameters to pass to the requests, by default None
        progress_bar : tqdm.tqdm, optional
            Progress bar to use, by default None

        Returns
        -------
        Dict[str, requests.Response]
            Dictionary with the url as key and the response as value
        '''

        # Check if num_processes is greater than the number of urls and adjust accordingly
        if self.NUM_PROCESSES > len(url_list):
            self.NUM_PROCESSES = len(url_list)

        # Do requests in parallel
        with ThreadPoolExecutor(max_workers=self.NUM_PROCESSES) as executor:

            # init desired results to None, so that we can check if they are not None later
            results = {url: None for url in url_list}

            # Do requests with retries
            if param_list is None:
                futures = [executor.submit(self._do_request_with_retry, url, None) for url in url_list]
            else:
                futures = [executor.submit(self._do_request_with_retry, url, params) for url, params in zip(url_list, param_list)]

            # Get results
            for future in as_completed(futures):
                if isinstance(future.result(), Exception):
                    UtilLogger.log(f"Exception in thread: {future.result()}")
                else:
                    with self.LOCK:
                        response = future.result()

                        # Update progress bar
                        if progress_bar is not None:
                            progress_bar.update(1)

                        # Check if response is not None
                        if response is not None:
                            response_url, response_object = response
                            results[response_url] = response_object

        return results
    
    def _do_request_with_retry(self, url: str, params: dict) -> Union[Tuple[str, requests.Response], None]:
        '''
        Do a request to the given url with retries

        Parameters
        ----------
        url : str
            URL to do the request
        params : dict, optional
            Parameters to pass to the request, by default None
        
        '''
        retry_count = 0
        while retry_count < self.REQUEST_MAX_RETRIES:
            response = self.do_request(url, params)
            if response[1] is not None:
                return (url, response[1])
            retry_count += 1
        return (url, None)

class RequestError(Exception):
    """Raised when there is an error making a request."""

    def __init__(self, response:requests.Response, message:str):

        if response is not None:
            proxy_used = response.request.proxy
            useragent_used = response.request.headers['User-Agent']
            base_message = f"Request to {response.url} failed with status code {response.status_code}:\n"
            base_message += f"Proxy used: {proxy_used}\n"
            base_message += f"User-Agent used: {useragent_used}\n"
        else:
            base_message = f"Request failed: response is None"

        self.message = base_message + message
        super().__init__(self.message)

        # Log error
        UtilLogger.log(self.message)
        
    def __str__(self):
        return self.message