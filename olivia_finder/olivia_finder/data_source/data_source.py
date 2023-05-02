'''
Description
-----------

Module that contains the DataSource class, which is the base class for data sources.

File information:
    - File: data_source.py
    - Project: data_source
    - Created Date: 2023-03-21 19:09:54
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones
'''

from __future__ import annotations
from abc import ABC, abstractmethod

class DataSource(ABC):
    """
    Base class for data sources.
    This class is an abstract class, so it cannot be instantiated.
    The subclasses must implement the methods obtain_package_names, obtain_package_data and obtain_packages_data.

    Parameters
    ----------
    name : str
        Name of the data source
    description : str
        Description of the data source
    auxiliary_datasources : Optional[list[DataSource]], optional
        List of auxiliary data sources, by default None

    Attributes
    ----------
    name : str
        Name of the data source
    description : str
        Description of the data source
    packages_data : dict
        dictionary with the data of the packages

    """

    def __init__(self, name: str, description: str):
        
        self.name: str = name
        self.description: str = description
        self.packages_data: dict = {}


    def get_info(self) -> dict:
        '''
        Returns the datasource information data.

        Returns
        -------
        dict
            The information of the data source
        
        Example
        -------
        >>> data_source = DataSource('name', 'description')
        >>> data_source.get_info()
        {'name': 'name', 'description': 'description'}
        '''
        return {
            'name': self.name,
            'description': self.description
        }


    # Abstract methods
    # ----------------

    # Implement the methods obtain_package_names, obtain_package_data and obtain_packages_data in the subclasses

    @abstractmethod
    def obtain_package_names(self) -> list[str]:
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
    def obtain_packages_data(self, package_names: list[str]) -> list[dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        '''
        raise NotImplementedError

class NotFoundInDataSourceException(Exception):
    """
    Exception that is raised when a package is not found in a data source.
    """
    
    def __init__(self, package_name: str, data_source_name: str):
        self.package_name = package_name
        self.data_source_name = data_source_name

    def __str__(self):
        return f'The package {self.package_name} was not found in the data source {self.data_source_name}'
    
    
