import time
import requests
from threading import Thread

import tqdm

from .job import RequestJob
from .proxy_handler import ProxyHandler
from .useragent_handler import UserAgentHandler
from  ..utilities.logger import MyLogger

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

    Attributes
    ----------
    worker_id : int
        Worker id, used for logging purposes
    jobs_queue : queue.Queue
        Queue of RequestJob objects
    my_jobs : list
        List of RequestJob objects that this worker has done
    proxy_handler : ProxyHandler
        ProxyHandler object
    user_agent_handler : UserAgentHandler
        UserAgentHandler object
    '''

    # Constants
    RETRIES = 3
    RETRY_DELAY = 3
    TIMEOUT = 30
    
    def __init__(self, worker_id, jobs_queue, progress_bar: tqdm.tqdm = None):
        '''
        Constructor
        '''

        Thread.__init__(self)
        self.worker_id = worker_id
        self.jobs_queue = jobs_queue
        self.my_jobs = []
        self.progress_bar = progress_bar
        
        # Create handlers (Singletons)
        self.proxy_handler: ProxyHandler = ProxyHandler()
        self.user_agent_handler = UserAgentHandler()

        self.stopped = False

    def run(self):
        '''
        Run the worker
        '''

        while True:

            if self.stopped:
                break
            
            # Get next url from the queue
            job = self.jobs_queue.get()

            message = f"Worker {self.worker_id}: Got job from queue\n"
            message += f"Job key: {job.key}\n"
            message += f"url: {job.url}"
            MyLogger().get_logger().debug(message)


            # If exit string is received, break the loop
            if job.key == RequestJob.FINALIZE_KEY:
                break
            
            # Get proxy and user agent
            MyLogger().get_logger().debug(f"Worker {self.worker_id}: Obtaining proxy and user agent")
            proxy, user_agent = self._obtain_request_args()
            MyLogger().get_logger().debug(f"Worker {self.worker_id}: Obtained proxy: {proxy} and user agent: {user_agent}")

            
            # Do the request
            message = f"Worker {self.worker_id}: Doing request"
            MyLogger().get_logger().debug(message)

            try:

                # Do the request using requests
                response = self._do_request(
                    job.url, 
                    proxy=proxy, 
                    headers={"User-Agent": user_agent}, 
                    params=job.params
                )
                
            except Exception as e:
                MyLogger().get_logger().error(f"Worker {self.worker_id}: Error doing request job: {e}")
                response = None

            # Check if the response is valid
            if response is None or response.status_code != 200:
                MyLogger().get_logger().error(f"Worker {self.worker_id}: Error doing request job: {response}")
                response = None
            
            # Update the progress bar
            if self.progress_bar is not None:
                self.progress_bar.update(1)

            # Set the response in the job and add it to the list of jobs
            job.set_response(response)
            self.my_jobs.append(job)

            # Mark the task as done
            self.jobs_queue.task_done()
            MyLogger().get_logger().debug(f"Worker {self.worker_id}: Done for {job.url}")
            
    def _obtain_request_args(self) -> tuple:
        '''
        Obtain the proxy and user agent to use for the request

        Returns
        -------
        tuple
            Tuple with the proxy and user agent to use for the request
        '''
        
        # Protect the access to the objects
        
        # Get a proxy with the lock
        self.proxy_handler.lock.acquire()
        proxy = self.proxy_handler.get_next_proxy()
        self.proxy_handler.lock.release()
        
        # Get a user agent with the lock
        self.user_agent_handler.lock.acquire()
        user_agent = self.user_agent_handler.get_next_useragent()
        self.user_agent_handler.lock.release()
        
        return proxy, user_agent

        # return None, None
        
    def _do_request(
        self, 
        url,
        timeout=TIMEOUT,
        data=None,
        proxy=None,
        headers=None,
        params=None,
        retries=RETRIES,
        retry_delay=RETRY_DELAY
    ):
        '''
        Do a request using requests library, with retries, the parameters are the same as requests.get
        Handles the exceptions and retries


        Parameters
        ----------
        url : str
            URL to do the request
        timeout : int, optional
            Timeout for the request, by default TIMEOUT
        data : dict, optional
            Data to send with the request, by default None (POST request)
        params : dict, optional
            Parameters to send with the request, by default None (GET request)
        proxy : str, optional
            Proxy to use for the request, by default None
        headers : dict, optional
            Headers to use for the request, by default None
        retries : int, optional
            Number of retries to do, by default RETRIES
        retry_delay : int, optional
            Delay between retries, by default RETRIE_DELAY

        Returns
        -------
        requests.Response
            Response of the request

        '''
        

        try:
            # Do the request using requests

            curr_proxy = {
                "http": proxy
            }
            
            response = requests.get(
                url, 
                timeout=timeout, 
                headers=headers,
                proxies=curr_proxy,
                data=data,
                params=params,
            )

        except Exception as ex_1:

            MyLogger().get_logger().error(f"Worker {self.worker_id}: {url}, Exception: {ex_1}")
            response = None

            # Retry if there are retries left
            while response is None and retries > 0:
                retries -= 1
                time.sleep(retry_delay)
                MyLogger().get_logger().debug(f"Worker {self.worker_id}: Retrying {url}, Retries left: {retries}")
                try:
                    response = requests.get(
                        url, 
                        timeout=timeout, 
                        headers=headers,
                        proxies=curr_proxy,
                        data=data,
                    )
                except Exception as e_2:
                    MyLogger().get_logger().error(f"Worker {self.worker_id}: {url}, Exception: {e_2}")
                    response = None

        MyLogger().get_logger().debug(f"Worker {self.worker_id}: {url}, Response: {response}")
            
        return response
    
