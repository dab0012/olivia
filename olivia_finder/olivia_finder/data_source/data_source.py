
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ..utilities.config import Configuration
from ..utilities.logger import MyLogger

class DataSource(ABC):
    '''
    Base class for data sources.

    .. warning:: 
    
        This class is an abstract class, so it can't be instantiated.

    The subclasses must implement the methods:
    - `DataSource.obtain_package_names`
    - `DataSource.obtain_package_data`
    - `DataSource.obtain_packages_data`


    .. note::

        The `name` and `description` parameters are mandatory, and must be passed as arguments.
        The use of this parameters is to be able to identify the data source, and to be able to show a description of it.
    '''

    def __init__(self):
        '''
        Initialize the class
        '''
        self.logger = MyLogger().get_logger("logger_datasource")

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.
        
        Is an optional method, if the data source does not implement it, it will
        be considered that it does not have a list of packages available.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError

    @abstractmethod
    def obtain_package_data(self, package_name:str) -> dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            The name of the package to obtain the data

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError

    @abstractmethod
    def obtain_packages_data(self, package_names: List[str]) -> List[dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        '''
        raise NotImplementedError


    
    
