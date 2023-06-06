import queue
from typing import List, Optional
import tqdm
from .job import RequestJob
from .request_worker import RequestWorker
from ..utilities.logger import MyLogger
from ..utilities.config import Configuration


class RequestHandler:
    '''
    Class to handle requests in with concurrent workers
    '''

    PARALLEL_WORKERS = 8

    def __init__(self):
        '''
        Constructor for RequestHandler class
        '''

        # Get logger name from config file
        self.logger = MyLogger.get_logger(
            Configuration().get_key('logger_myrequests', 'name')
        )

        self.logger.debug("Creating RequestHandler object")

        # Create jobs queue
        self.jobs_queue = queue.Queue()

        # Number of workers
        self.num_workers = 1
        self.workers: List[RequestWorker] = []

    
    def _clear(self):
        '''
        Reset the RequestHandler object
        '''
        
        # Delete the objects
        del self.jobs_queue
        del self.workers
        
        # Create jobs queue
        self.jobs_queue = queue.Queue()
        
        # Number of workers
        self.num_workers = 1
        self.workers: List[RequestWorker] = []


    def _setup_jobs(self, request_jobs: List[RequestJob], num_workers: int, progress_bar: Optional[tqdm.tqdm] = None):
        '''
        Setup the jobs

        Parameters
        ----------
        request_jobs : List[RequestJob]
            List of RequestJob objects
        num_workers : int
            Number of workers
        progress_bar : Optional[tqdm.tqdm], optional
            Progress bar, by default None
        '''
        
        # Enqueue jobs
        for job in request_jobs:
            # job.progress_bar = progress_bar
            self.jobs_queue.put(job)

        self.logger.debug(f"Jobs queue size: {self.jobs_queue.qsize()}")

        # Workers keep working till they receive an exit string
        # So we need to add the number of workers times the exit string to the queue
        self.num_workers = num_workers
        for _ in range(self.num_workers):
            self.jobs_queue.put(RequestJob.end_job_signal())

        # Create workers and add to the queue
        self.logger.debug("Creating workers")

        for i in range(self.num_workers):
            worker = RequestWorker(i, self.jobs_queue, progress_bar)
            self.workers.append(worker)

        self.logger.debug(f"Created workers: {len(self.workers)}")

    
    def _setup_job(self, request_job: RequestJob):
        '''
        Setup a single job

        Parameters
        ----------
        request_job : RequestJob
            The RequestJob object
        '''
        
        # Enqueue jobs
        self.jobs_queue.put(request_job)

        # Workers keep working till they receive an exit string
        # So we need to add the number of workers times the exit string to the queue
        self.jobs_queue.put(RequestJob.end_job_signal())

        # Create workers and add to the queue
        self.workers.append(
            RequestWorker(0, self.jobs_queue)
        )
        self.logger.debug("Job created")


    def do_requests(self, request_jobs: List[RequestJob], num_workers: int = PARALLEL_WORKERS, progress_bar: Optional[tqdm.tqdm] = None) -> List[RequestJob]:
        '''
        Do the requests

        Parameters
        ----------
        request_jobs : List[RequestJob]
            List of RequestJob objects
        num_workers : int, optional
            Number of workers, by default PARALLEL_WORKERS
        progress_bar : Optional[tqdm.tqdm], optional
            Progress bar, by default None
        
        Returns
        -------
        list
            List of RequestJob objects

        Examples
        --------
        >>> rh = RequestHandler(jobs)
        >>> results = rh.do_requests()
        >>> for job in results:
        >>>     print(f'key: {job.key}, url: {job.url}, response: {job.response}')
        '''

        # reet the class
        self._clear()

        self.logger.info("Starting requests")
        self.logger.debug(f"Number of jobs: {len(request_jobs)}")

        # Setup jobs
        self._setup_jobs(request_jobs, num_workers, progress_bar)
        
        # Start workers
        for worker in self.workers:
            self.logger.debug(f"Starting worker {worker.worker_id}")
            worker.start()
            
        # Join workers to wait till they finished
        for worker in self.workers:

            worker.join()
            self.logger.debug(f"Joining worker {worker.worker_id}")

        # Combine results from all workers
        workers_finalized_jobs = []
        for worker in self.workers:
            self.logger.debug(f"Worker {worker.worker_id} finished")
            workers_finalized_jobs.extend(worker.my_jobs.copy())

        self.logger.info("All requests finished")
        return workers_finalized_jobs

    def do_request(self, job: RequestJob):
        '''
        Do a single request
        
        Parameters
        ----------
        job : RequestJob
            The RequestJob object

        Returns
        -------
        RequestJob
            The RequestJob object with the response

        Examples
        --------
        >>> rh = RequestHandler()
        >>> job = RequestJob("single_job", "https://www.google.com")
        >>> result = rh.do_request(job)
        >>> print(f'key: {result.key}, url: {result.url}, response: {result.response}')
        '''

        # Clear the RequestHandler object
        self._clear()

        # Setup job
        self._setup_job(job)

        # Start worker
        worker = RequestWorker(0, self.jobs_queue)
        self.logger.debug(f"Starting worker {worker.worker_id}")

        self.logger.info(f"Starting request for {job.key}: {job.url}")
        worker.start()

        # Join worker to wait till it finished
        worker.join()
        self.logger.debug(f"Joining worker {worker.worker_id}")
        self.logger.info(f"Request for {job.key}: {job.url} finished")

        if worker.my_jobs[0].response is None:
            self.logger.info(f"Request for {job.key}: {job.url} failed: response is None")

        # Return the job
        return worker.my_jobs[0]
    