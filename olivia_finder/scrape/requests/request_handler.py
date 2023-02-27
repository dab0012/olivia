import logging
import requests
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
                 useragents_handler: UserAgentHandler, max_retry = 5, request_timeout=10):

        self.proxy_handler = proxy_handler
        self.useragents_handler = useragents_handler
        self.lock = Lock()
        self.current_proxy_index = 0
        self.current_useragent_index = 0
        self.max_retry = max_retry
        self.request_timeout = request_timeout
    

    
    def do_request(self, url, retry_count=0) -> Union[Tuple[str, requests.Response], None]:

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
                response = session.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=self.request_timeout)
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
            
    def do_parallel_requests(self, urls, num_processes):

        # Check if num_processes is greater than the number of urls and adjust accordingly
        if num_processes > len(urls):
            num_processes = len(urls)

        # Do parallel requests
        results = {}
        with ThreadPoolExecutor(max_workers=num_processes) as executor:

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

                        # Check if response is not None
                        if response is not None:
                            response_url, response_object = response
                            results[response_url] = response_object

        return results