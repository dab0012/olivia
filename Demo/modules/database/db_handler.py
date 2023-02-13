# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

from abc import ABC, abstractmethod

class DatabaseHandler(ABC):
    '''
    Class for connecting to the database
    This class implements the Singleton pattern so that only one instance of the class exists.    
    '''
    
    # Attribute to store the single instance of the class
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        Method to create a new instance of the class

        Parameters:
        -----------
            cls (DatabaseHandler): Class object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
        --------
            DatabaseHandler: Single instance of the class
        '''

        # If an instance of the class already exists, that instance is returned
        if cls._instance is None:
            # If no instance exists, a new one is created and stored in the _instance attribute
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def __init__(self):
        '''
        Method to initialize the class
        '''
        # To implement in subclass ...
        pass
    
    @abstractmethod
    def get_connection(self):
        '''
        Method to get the connection to the database
        '''
        pass

    @abstractmethod
    def open_connection(self):
        '''
        Method to open the connection to the database
        '''
        pass

    @abstractmethod
    def close_connection(self):
        '''
        Method to close the connection to the database
        '''
        pass

    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> list[tuple]:
        '''
        Method to execute a query in the database

        Parameters:
        -----------
            query (str): Query to be executed
            params (tuple): Parameters of the query

        Returns:
        --------
            list[tuple]: List of tuples with the result of the query
        '''

        # To implemnt in subclass
        pass

    @abstractmethod
    def get_QueryBuilder(self):
        '''
        Method to get the query builder
        '''
        pass