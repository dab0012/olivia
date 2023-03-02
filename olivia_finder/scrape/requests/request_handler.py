import logging, requests, tqdm
from typing import Tuple, Union
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler

class RequestHandler:
    '''
    Class that handles HTTP requests in a more transparent way in scraping and denial of service environments
    by the servers from which the data is requested 
    Basically, it manages the proxies and user agents so that scraping is not detected
    '''

    def __init__(self, 
                 proxy_handler: ProxyHandler, 
                 useragents_handler: UserAgentHandler, max_retry = 5, request_timeout=10, num_processes=32):
        '''
        Constructor of the class

        Parameters
        ----------
        proxy_handler : ProxyHandler
            ProxyHandler object to manage the proxies
        useragents_handler : UserAgentHandler
            UserAgentHandler object to manage the user agents
        max_retry : int, optional
            Maximum number of retries to do a request, by default 5
        request_timeout : int, optional
            Timeout of the requests, by default 10
        num_processes : int, optional
            Number of processes to do the requests, by default 8
        '''
        self.proxy_handler = proxy_handler
        self.useragents_handler = useragents_handler
        self.lock = Lock()
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.max_retry = max_retry
        self.request_timeout = request_timeout
        self.num_processes = num_processes
    
    def do_request(self, url, retry_count=0) -> Union[Tuple[str, requests.Response], None]:
        '''
        Do a request to the given url

        Parameters
        ----------
        url : str
            URL to do the request
        retry_count : int, optional
            Number of retries, by default 0

        Returns
        -------
        Union[Tuple[str, requests.Response], None]
            Tuple with the url and the response if the request was successful, None otherwise
        '''
        # Get proxy
        proxy = self.proxy_handler.get_next_proxy()
        if proxy is not None:
            proxy = f"http://{proxy}"

        # Get useragent
        headers = {'User-Agent': self.useragents_handler.get_next_useragent()}

        # Do request
        try:
            # if response == OK, return response
            with requests.Session() as session:
                response = session.get(url, headers=headers, proxies={'http': proxy}, timeout=self.request_timeout)
            return (url, response)
        
        except Exception as e:

            # if response != OK, retry request if retry_count < max_retry
            logging.error(f"Error: {e}")
            logging.error(f"Proxy: {proxy}")
            logging.error(f"Useragent: {headers['User-Agent']}")
            logging.info(f"Retrying request: {url}")

            if retry_count < self.max_retry:
                return self.do_request(url, retry_count=retry_count+1)
            else:
                logging.error(f"Max retry count reached for {url}")
                return (url, None)
            
    def do_parallel_requests(self, urls, progress_bar: tqdm.tqdm = None):
        '''
        Do parallel requests to the given urls

        Parameters
        ----------
        urls : List[str]
            List of URLs to do the requests
        progress_bar : tqdm.tqdm, optional
            Progress bar to update, by default None, is passed as value, then the progress bar is updated

        Returns
        -------
        Dict[str, requests.Response]
            Dictionary with the url as key and the response as value
        '''
        # Check if num_processes is greater than the number of urls and adjust accordingly
        if self.num_processes > len(urls):
            self.num_processes = len(urls)

        # Do parallel requests
        results = {}
        with ThreadPoolExecutor(max_workers=self.num_processes) as executor:

            # init desired results
            for url in urls:
                # If response is None,
                # then the request failed and the result is already None
                results[url] = None

            futures = [executor.submit(self.do_request, url) for url in urls]
            for future in as_completed(futures):
                if isinstance(future.result(), Exception):
                    logging.error(f"Error: {future.result()}")
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