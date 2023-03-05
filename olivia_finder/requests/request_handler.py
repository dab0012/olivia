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

import logging, requests, tqdm, os
from typing import List, Tuple, Union
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

from olivia_finder.config import LoggerConfiguration
from olivia_finder.util import UtilLogger, UtilMultiThreading
from olivia_finder.requests.proxy_handler import ProxyHandler
from olivia_finder.requests.useragent_handler import UserAgentHandler

class RequestHandler:
    '''
    Class that handles HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested 
    Basically, it manages the proxies and user agents so that scraping is not detected
    '''
    # Attributes
    # ----------
    proxy_handler: ProxyHandler                 = None     # Proxy handler to use
    useragents_handler: UserAgentHandler        = None     # User agent handler to use
    current_proxy_index: int                    = 0        # Current proxy index
    current_useragent_index: int                = 0        # Current user agent index
    REQUEST_MAX_RETRIES: int                    = 5        # Maximum number of retries for each request
    REQUEST_TIMEOUT: int                        = 30       # Timeout for each request
    LOCK: Lock                                  = None     # Lock to use for thread safety
    NUM_PROCESSES: int                          = 4        # Number of processes to use for parallel requests
    LOGGER: logging.Logger                      = None     # Logger to use

    def __init__(self, 
                 proxy_handler: ProxyHandler, useragents_handler: UserAgentHandler, 
                 max_retry: int = REQUEST_MAX_RETRIES, request_timeout: int = REQUEST_TIMEOUT, 
                 num_processes: int = NUM_PROCESSES, use_logger: bool = False):
        '''
        Constructor
        
        Parameters
        ----------
        proxy_handler: ProxyHandler
            Proxy handler to use
        useragents_handler: UserAgentHandler
            User agent handler to use
        max_retry: int
            Maximum number of retries for each request
        request_timeout: int
            Timeout for each request
        num_processes: int
            Number of processes to use for parallel requests
        use_logger: bool
            If True, a logger is configured and used
        '''

        self.proxy_handler = proxy_handler
        self.useragents_handler = useragents_handler
        self.LOCK = Lock()
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.REQUEST_MAX_RETRIES = max_retry
        self.REQUEST_TIMEOUT = request_timeout

        # Check number of processes
        recommended_num_processes = UtilMultiThreading.recommended_threads()
        if num_processes > recommended_num_processes:
            UtilLogger.logg(self.LOGGER, f"Number of processes ({num_processes}) is greater than the recommended number ({recommended_num_processes}).", "WARNING")
            self.NUM_PROCESSES = recommended_num_processes
        elif num_processes < 1:
            raise ValueError("num_processes must be greater than 0")
        else:
            self.NUM_PROCESSES = num_processes

        # Configure logger
        if use_logger:
            self.LOGGER = UtilLogger.prepare_loger("RequestHandler")
            UtilLogger.logg(self.LOGGER, "Logger configured", "INFO")

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
                    proxy = self.proxy_handler.get_next_proxy()
                if self.useragents_handler is not None:
                    headers = {'User-Agent': self.useragents_handler.get_next_useragent()}
        except Exception as e:
            raise RequestError(url, f"Exception getting proxy and user agent: {e}", self.LOGGER) from e

        UtilLogger.logg(self.LOGGER, f"Using proxy: {proxy} and user agent: {headers['User-Agent']}", "DEBUG")

        # Do the request
        try:
            with requests.Session() as session:
                response = session.get(
                    url, 
                    headers=headers,
                    proxies={'http': proxy}, 
                    timeout=self.REQUEST_TIMEOUT, 
                    params=params
                )

            # Response is ok
            UtilLogger.logg(self.LOGGER, f"Response status code: {response.status_code}", "DEBUG")
            return (url, response)
                   
        # Handle exceptions
        except Exception as e:
            raise RequestError(response, f"Exception doing request: {e}", self.LOGGER) from e
      
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

        # Define a helper function to do the request with retries
        def do_request_with_retry(url, params):
            retry_count = 0
            while retry_count < self.REQUEST_MAX_RETRIES:
                response = self.do_request(url, params)
                if response[1] is not None:
                    return response
                retry_count += 1
            return (url, None)

        # Do requests in parallel
        with ThreadPoolExecutor(max_workers=self.NUM_PROCESSES) as executor:

            # init desired results to None, so that we can check if they are not None later
            results = {url: None for url in url_list}

            # Do requests with retries
            if param_list is None:
                futures = [executor.submit(do_request_with_retry, url, None) for url in url_list]
            else:
                futures = [executor.submit(do_request_with_retry, url, params) for url, params in zip(url_list, param_list)]

            # Get results
            for future in as_completed(futures):
                if isinstance(future.result(), Exception):
                    UtilLogger.logg(self.LOGGER, f"Exception in thread: {future.result()}", "ERROR")
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
    
class RequestError(Exception):
    """Raised when there is an error making a request."""

    def __init__(self, response:requests.Response, message:str, logger:logging.Logger = None):

        self.response = response
        proxy_used = response.request.proxy
        useragent_used = response.request.headers['User-Agent']

        base_message = f"Request to {response.url} failed with status code {response.status_code}:\n"
        base_message += f"Proxy used: {proxy_used}\n"
        base_message += f"User-Agent used: {useragent_used}\n"
        self.message = base_message + message

        super().__init__(self.message)

        # Log error
        UtilLogger.logg(logger, self.message, "ERROR")
        
    def __str__(self):
        return self.message