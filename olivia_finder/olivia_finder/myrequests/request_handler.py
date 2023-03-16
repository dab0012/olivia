""""""
'''
·········································································
File: request_handler.py
Project: Olivia-Finder
Created Date: Monday February 27th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''


import tqdm, requests
from typing import List, Optional, Tuple, Union
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from olivia_finder.myrequests.proxy_handler import ProxyHandler
from olivia_finder.myrequests.useragent_handler import UserAgentHandler
from olivia_finder.util.logger import UtilLogger
from olivia_finder.util.util import Util

class RequestHandler:
    '''
    Class that handles HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested 
    Basically, it manages the proxies and user agents so that scraping is not detected
    
    :param proxy_handler: Proxy handler to use, defaults to None
    :type proxy_handler: ProxyHandler, optional
    :param useragents_handler: User agent handler to use, defaults to None
    :type useragents_handler: UserAgentHandler, optional
    :param max_retry: Maximum number of retries for each request, defaults to REQUEST_MAX_RETRIES
    :type max_retry: int, optional
    :param request_timeout: Timeout for each request, defaults to REQUEST_TIMEOUT
    :type request_timeout: int, optional
    :param num_processes: Number of processes to use for parallel requests, defaults to NUM_PROCESSES
    :type num_processes: int, optional
    :return: RequestHandler
    :rtype: RequestHandler
    '''
    # Attributes
    # ----------
    proxy_handler: ProxyHandler                            # Proxy handler to use
    useragents_handler: UserAgentHandler                   # User agent handler to use
    current_proxy_index: int                               # Current proxy index
    current_useragent_index: int                           # Current user agent index
    LOCK: Lock                                             # Lock to use
    REQUEST_MAX_RETRIES: int                    = 5        # Maximum number of retries for each request
    REQUEST_TIMEOUT: int                        = 60       # Timeout for each request
    NUM_PROCESSES: int                          = 4        # Number of processes to use for parallel requests

    def __init__(
        self, 
        proxy_handler:          Optional[ProxyHandler] = None, 
        useragents_handler:     Optional[UserAgentHandler] = None, 
        max_retry:              Optional[int] = REQUEST_MAX_RETRIES, 
        request_timeout:        Optional[int] = REQUEST_TIMEOUT, 
        num_processes:          Optional[int] = NUM_PROCESSES, 
    ):
        '''Constructor'''


        # Check proxy handler
        self.proxy_handler = ProxyHandler() if proxy_handler is None else proxy_handler
    
        # Check user agent handler
        self.useragents_handler = UserAgentHandler() if useragents_handler is None else useragents_handler

        # Initialize attributes
        self.LOCK = Lock()
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.REQUEST_MAX_RETRIES = max_retry
        self.REQUEST_TIMEOUT = request_timeout

        # Check number of processes
        recommended_num_processes = Util.recommended_threads()
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
        
        :param url: Url to do the request
        :type url: str
        :param params: Parameters to pass to the request, defaults to None
        :type params: dict, optional
        :return: Tuple with the url and the response if the request was successful, None otherwise
        :rtype: Union[Tuple[str, requests.Response], None]
        :raises RequestError: If there is an error doing the request
        :return: Tuple with the url and the response if the request was successful, None otherwise
        :rtype: Union[Tuple[str, requests.Response], None]
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
        
    def do_parallel_requests(
        self, url_list: List[str], 
        param_list: Optional[List[dict]] = None, 
        progress_bar: Optional[tqdm.tqdm] = None
        ) -> List[Union[Tuple[str, requests.Response], None]]:
        '''
        Do parallel requests to the given urls, with the given parameters if any
        
        :param url_list: List of urls to do the requests
        :type url_list: List[str]
        :param param_list: List of parameters to pass to the requests, defaults to None
        :type param_list: List[dict], optional
        :param progress_bar: Progress bar to use, defaults to None
        :type progress_bar: tqdm.tqdm, optional
        :return: List of tuples with the url and the response if the request was successful, None otherwise
        :rtype: List[Union[Tuple[str, requests.Response], None]]
        '''

        # Check if num_processes is greater than the number of urls and adjust accordingly
        self.NUM_PROCESSES = min(self.NUM_PROCESSES, len(url_list))
        
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
        Do a request to the given url with retries, if the request fails for any reason
        
        :param url: Url to do the request
        :type url: str
        :param params: Parameters to pass to the request, defaults to None
        :type params: dict, optional
        :return: Tuple with the url and the response if the request was successful, None otherwise
        :rtype: Union[Tuple[str, requests.Response], None]        
        '''
        retry_count = 0
        while retry_count < self.REQUEST_MAX_RETRIES:
            response = self.do_request(url, params)
            if response[1] is not None:
                return (url, response[1])
            retry_count += 1
        return (url, None)

class RequestError(Exception):
    """Raised when there is an error making a request.
    
    :param response: Response object
    :type response: 
    """

    def __init__(self, response:requests.Response, message:str):

        if response is not None:
            proxy_used = response.request.proxy
            useragent_used = response.request.headers['User-Agent']
            base_message = f"Request to {response.url} failed with status code {response.status_code}:\n"
            base_message += f"Proxy used: {proxy_used}\n"
            base_message += f"User-Agent used: {useragent_used}\n"
        else:
            base_message = "Request failed: response is None"

        self.message = base_message + message
        super().__init__(self.message)

        # Log error
        UtilLogger.log(self.message)
        
    def __str__(self):
        return self.message
