import tqdm, requests
from typing import List, Optional, Tuple, Union
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from .proxy_handler import ProxyHandler
from .useragent_handler import UserAgentHandler
from ..util.logger import MyLogger
from ..util.util import Util

class RequestHandler:
    '''
    Class that handles HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested 
    Basically, it manages the proxies and user agents so that scraping is not detected

    Attributes
    ----------
    proxy_handler : ProxyHandler
        Proxy handler
    useragents_handler : UserAgentHandler
        User agent handler
    current_proxy_index : int
        Current proxy index
    current_useragent_index : int
        Current user agent index
    REQUEST_MAX_RETRIES : int
        Maximum number of retries for each request
    REQUEST_TIMEOUT : int
        Timeout for each request
    NUM_PROCESSES : int
        Number of processes to use for parallel requests
    lock : Lock
        Lock for the current proxy and user agent indexes for multi-threading

    Parameters
    ----------
    proxy_handler : Optional[ProxyHandler]
        Proxy handler, if None, it will be initialized with a generic ProxyHandler
    useragents_handler : Optional[UserAgentHandler]
        User agent handler, if None, it will be initialized with a generic UserAgentHandler
    max_retry : Optional[int]
        Maximum number of retries for each request, if None, it will be initialized with the default value
    request_timeout : Optional[int]
        Timeout for each request, if None, it will be initialized with the default value
    num_processes : Optional[int]
        Number of processes to use for parallel requests, if None, it will be initialized with the default value
    '''

    def __init__(
        self, 
        proxy_handler:          Optional[ProxyHandler] = None, 
        useragents_handler:     Optional[UserAgentHandler] = None, 
        max_retry:              Optional[int] = 5, 
        request_timeout:        Optional[int] = 60, 
        num_processes:          Optional[int] = 4, 
    ):
        '''Constructor'''

        # Check proxy handler
        self.proxy_handler = ProxyHandler() if proxy_handler is None else proxy_handler
    
        # Check user agent handler
        self.useragents_handler = UserAgentHandler() if useragents_handler is None else useragents_handler

        # Initialize attributes
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.REQUEST_MAX_RETRIES = max_retry
        self.REQUEST_TIMEOUT = request_timeout
        self.lock = Lock()

        # Check number of processes
        recommended_num_processes = Util.recommended_threads()
        if num_processes > recommended_num_processes:
            MyLogger.log(f"Number of processes ({num_processes}) is greater than the recommended number ({recommended_num_processes}).")
            self.NUM_PROCESSES = recommended_num_processes
        elif num_processes < 1:
            raise ValueError("num_processes must be greater than 0")
        else:
            self.NUM_PROCESSES = num_processes

    def do_request(self, url: str, params: dict = None) -> Union[Tuple[str, requests.Response], None]:
        '''
        Do a request to the given url and return the response.
        It uses a proxy and a user agent if they are available.

        Parameters
        ----------
        url : str
            Url to do the request
        params : dict, optional
            Parameters to pass to the request, by default None

        Raises
        ------
        RequestError
            If there is an error doing the request

        Returns
        -------
        Union[Tuple[str, requests.Response], None]
            Tuple with the url and the response if the request was successful, None otherwise

        Examples
        --------
        >>> request_handler = RequestHandler()
        >>> request_handler.do_request("https://www.google.com")
        ('https://www.google.com', <Response [200]>)
        '''

        # Try to get proxy and user agent with lock for thread safety
        proxy = headers = None

        try:
            with self.lock:
                if self.proxy_handler is not None:
                    proxy_url = self.proxy_handler.get_next_proxy()
                    proxy = {"http": proxy_url}
                    MyLogger.log(f"Using proxy: {proxy}")
                if self.useragents_handler is not None:
                    headers = {'User-Agent': self.useragents_handler.get_next_useragent()}
                    MyLogger.log(f"Using user agent: {headers['User-Agent']}")
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
            MyLogger.log(f"Response status code: {response.status_code}")
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
        Do requests to the given urls.
        It uses multiprocessing to do the requests in parallel.
        
        Parameters
        ----------
        url_list : List[str]
            List of urls to do the requests
        param_list : Optional[List[dict]], optional
            List of parameters to pass to the requests, by default None
        progress_bar : Optional[tqdm.tqdm], optional
            Progress bar to use, by default None

        Returns
        -------
        List[Union[Tuple[str, requests.Response], None]]
            List of tuples with the url and the response if the request was successful, None otherwise

        Examples
        --------
        >>> url_list = ["https://www.google.com", "https://www.yahoo.com"]
        >>> param_list = [{"q": "test"}, {"q": "test2"}]
        >>> request_handler = RequestHandler()
        >>> request_handler.do_parallel_requests(url_list, param_list)
        [('https://www.google.com', <Response [200]>), ('https://www.yahoo.com', <Response [200]>)]
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

                # If there was an exception, log it and continue
                if isinstance(future.result(), Exception):
                    MyLogger.log(f"Exception in thread: {future.result()}")
                else:
                    with self.lock:
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
        
        Parameters
        ----------
        url : str
            Url to do the request
        params : dict
            Parameters to pass to the request

        Returns
        -------
        Union[Tuple[str, requests.Response], None]
            Tuple with the url and the response if the request was successful, None otherwise     
        '''
        retry_count = 0
        while retry_count < self.REQUEST_MAX_RETRIES:
            response = self.do_request(url, params)
            if response[1] is not None:
                return (url, response[1])
            retry_count += 1
        return (url, None)

class RequestError(Exception):
    """
    Exception raised when there is an error doing a request

    Attributes
    ----------
    response : requests.Response
        Response object, used to get the url and the status code
    message : str
        Error message
    """

    def __init__(self, response:requests.Response, message:str):
        '''
        Constructor
        '''

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
        MyLogger.log(self.message)
        
    def __str__(self):
        '''
        String representation of the exception

        Returns
        -------
        str
            String representation of the exception
        '''
        return self.message
