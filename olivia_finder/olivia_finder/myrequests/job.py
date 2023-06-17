from __future__ import annotations
from typing import Dict, Optional
import requests

class RequestJob:
    '''
    A class to represent a job to be done by a worker.
            
    '''

    FINALIZE_KEY = "FINALIZE"

    def __init__(self, key: object, url: Optional[str], params: Optional[Dict[str, str]] = None):
        '''
        Constructor

        Parameters
        ----------
        key : object
            Key of the job
        url : Optional[str]
            Url of the request
        params : Dict[str, str]
            Parameters of the request
        '''

        self.key: object = key
        self.url: Optional[str] = url
        self.response: Optional[requests.Response] = None
        self.params: Optional[Dict[str, str]] = params

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
    def end_job_signal() -> RequestJob:
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