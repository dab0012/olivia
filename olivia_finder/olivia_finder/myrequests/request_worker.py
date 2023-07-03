import queue
import time
from typing import Optional, Tuple
import requests
from threading import Thread
import tqdm
from .job import RequestJob
from .proxy_handler import ProxyHandler
from .useragent_handler import UserAgentHandler
from ..utilities.logger import MyLogger
from ..utilities.config import Configuration


class RequestWorker(Thread):
    '''
    RequestWorker class, inherits from Thread, so it can be run in parallel
    This class is responsible for doing the requests and storing the results in the RequestJob objects
    Use the run() method to start the worker
    The worker has a queue of RequestJob objects, it will get the next job from the queue and do the request
    The worker has access to the ProxyHandler and UserAgentHandler objects, so it can get a proxy and a user agent for each request
    The worker will store the results in the RequestJob object and add it to the list of jobs that it has done
    The worker will keep working till it receives an exit string from the queue
    The exit string is a RequestJob object with key = RequestJob.FINALIZE_KEY

    '''

    # Constants
    RETRIES = 0
    RETRY_DELAY = 0
    TIMEOUT = 30
    
    def __init__(
            self, 
            worker_id: int, 
            jobs_queue: queue.Queue, 
            progress_bar: Optional[tqdm.tqdm] = None):
        '''
        Constructor

        Parameters
        ----------
        worker_id : int
            Id of the worker
        jobs_queue : queue.Queue
            Queue of RequestJob objects
        progress_bar : tqdm.tqdm
            Progress bar, if None, no progress bar will be shown

        '''

        Thread.__init__(self)
        self.worker_id = worker_id
        self.jobs_queue = jobs_queue
        self.my_jobs = []
        self.progress_bar = progress_bar
        
        # Create handlers (Singletons)
        self.proxy_handler = ProxyHandler()
        self.user_agent_handler = UserAgentHandler()
        self.stopped = False

        # Get logger name from config file
        self.logger = MyLogger.get_logger('logger_myrequests')
        self.logger.debug(f"Creating RequestWorker object {self.worker_id}")


    def run(self):
        '''
        Run the worker thread till it receives an exit signal
        '''

        while not self.stopped:

            # Get next url from the queue
            job = self.jobs_queue.get()
            message =   f"Worker {self.worker_id}: Got job from queue\n" + \
                        f"Worker {self.worker_id}: {job}" + \
                        f"Worker {self.worker_id}: Queue size: {self.jobs_queue.qsize()}"

            self.logger.debug(message)

            # If exit string is received, break the loop
            if job.key == RequestJob.FINALIZE_KEY:
                break

            # Do the request
            message = f"Worker {self.worker_id}: Doing request"
            self.logger.debug(message)
            try:
                proxy, user_agent = self._obtain_request_args()
                response = self._do_request(job.url, 
                                            proxy=proxy, 
                                            headers={"User-Agent": user_agent}, 
                                            params=job.params)
            except Exception as e:
                self.logger.error(f"Worker {self.worker_id}: Error doing request job: {e}")
                response = None

            # Check if the response is valid
            if response is None or response.status_code != 200:
                self.logger.error(f"Worker {self.worker_id}: Error doing request job: {response}")
                response = None

            # Set the response in the job and add it to the list of jobs
            job.set_response(response)
            self.my_jobs.append(job)
            self.jobs_queue.task_done()

            if self.progress_bar is not None:
                self.progress_bar.update(1)
            
    def _obtain_request_args(self) -> Tuple[str, str]:
        '''
        Obtain the proxy and user agent to use for the request

        Returns
        -------
        tuple[str, str]
            Tuple with the proxy and user agent to use for the request
        '''

        # Get a proxy with the lock
        self.proxy_handler.lock.acquire()
        proxy = self.proxy_handler.get_next_proxy()
        self.proxy_handler.lock.release()
        
        # Get a user agent with the lock
        self.user_agent_handler.lock.acquire()
        user_agent = self.user_agent_handler.get_next_useragent()
        self.user_agent_handler.lock.release()
        
        return proxy, user_agent
        
    def _do_request(self, 
                    url: str,
                    timeout: int = TIMEOUT,
                    retries: int = RETRIES,
                    retry_delay: int = RETRY_DELAY,
                    data: Optional[dict] = None,
                    proxy: Optional[str] = None,
                    headers: Optional[dict] = None,
                    params: Optional[dict] = None) -> Optional[requests.Response]:

        '''
        Do a request using requests library, with retries, the parameters are the same as requests.get
        Handles the exceptions and retries


        Parameters
        ----------
        url : str
            Url to do the request
        timeout : int, optional
            Timeout for the request, by default TIMEOUT
        retries : int, optional
            Number of retries, by default RETRIES
        retry_delay : int, optional
            Delay between retries, by default RETRY_DELAY
        data : dict = None, optional
            Data to send with the request, by default None
        proxy : str = None, optional
            Proxy to use for the request, by default None
        headers : dict = None, optional
            Headers to use for the request, by default None
        params : dict = None, optional
            Parameters to use for the request, by default None

        Returns
        -------
        requests.Response
            Response of the request

        '''
        
        # Do the request
        if proxy is None:
            curr_proxy = None
        else:
            curr_proxy = {"http": proxy}

        try:
            response = requests.get(url, 
                                    timeout=timeout, 
                                    headers=headers,
                                    proxies=curr_proxy,
                                    data=data,
                                    params=params)

        except Exception as e1:

            # Retry if there are retries left
            self.logger.error(f"Worker {self.worker_id}: {url}, Exception: {e1}")
            response = None
            while response is None and retries > 0:
                retries -= 1
                time.sleep(retry_delay)
                self.logger.debug(f"Worker {self.worker_id}: Retrying {url}, Retries left: {retries}")
                try:
                    response = requests.get(url, 
                                            timeout=timeout, 
                                            headers=headers,
                                            proxies=curr_proxy,
                                            data=data)
                except Exception as e2:
                    self.logger.error(f"Worker {self.worker_id}: {url}, Exception: {e2}")
                    response = None

        self.logger.debug(f"Worker {self.worker_id}: {url}, Response: {response}")
            
        return response
    
