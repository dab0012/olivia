from __future__ import annotations
import requests

class RequestJob:
    '''
    A class to represent a job to be done by a worker.
    
    Parameters
    ----------
    key : object
        Key to identify the job
    url : str
        URL to do the request

    Attributes
    ----------  
    key : object
        Key to identify the job
    url : str
        URL to do the request
    response : requests.Response
        Response of the request

    Constants
    ----------
    FINALIZE_KEY : str
        Key to signal the worker to end
        
    '''

    FINALIZE_KEY = "FINALIZE"

    def __init__(self, key: object, url: str, params: dict[str, str] = None):
        '''
        Constructor
        '''

        self.key: object = key
        self.url: str = url
        self.response: requests.Response = None
        self.params: dict[str, str] = params

    def set_response(self, job_response: requests.Response):
        '''
        Set the response of the job

        Parameters
        ----------
        job_response : requests.Response
            Response of the request
        '''

        self.response = job_response

    @staticmethod
    def end_job_signal():
        '''
        Returns a job that signals the worker to end

        Returns
        -------
        RequestJob
            A job that signals the worker to end
            
        '''
        
        return RequestJob(
            key=RequestJob.FINALIZE_KEY,
            url=None
        )