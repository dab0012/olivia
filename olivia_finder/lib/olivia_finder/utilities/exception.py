import logging
from typing import Optional
from .logger import MyLogger

class OliviaFinderException(Exception, BaseException):
    """Base class for exceptions in this module."""
    
    def __init__(self, message: str):
        '''
        Constructor of the class

        Parameters
        ----------
        message : str
            Message of the exception
        errors : list, optional
            List of errors, by default None
        '''
        super().__init__(message)
        self.message = message


    def __str__(self):
        '''String representation of the exception'''
        return f"EXCEPTION -> type: {self.__class__.__name__}, message: {self.message}"
    
    def __repr__(self):
        '''Representation of the exception'''
        return f"EXCEPTION -> type: {self.__class__.__name__}, message: {self.message}"
    
    
