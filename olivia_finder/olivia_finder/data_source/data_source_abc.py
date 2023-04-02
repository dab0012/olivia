'''
data_source_abc.py
==================

Description
-----------

Module that contains ...

File information:
    - File: data_source_abc.py
    - Project: data_source
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones

'''


from abc import ABC, abstractmethod

class DataSourceABC(ABC):
    """
    Interface class for data sources.
    """

    @abstractmethod
    def get_info(self) -> dict:
        '''
        Returns the information of the data source.

        Returns
        -------
        dict
            The information of the data source
        '''

    @abstractmethod
    def obtain_package_names(self) -> list:
        """
        Obtains the list of packages from the data source.
        Is an optional method, if the data source does not implement it, it will
        be considered that it does not have a list of packages available.

        Returns
        -------
        list
            The list of packages from the data source
        """

    @abstractmethod
    def obtain_package_data(self, package_name: str) -> dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            The name of the package to obtain the data
        
        Returns
        -------
        dict
            The data of a package from the data source as a dictionary
        """
    
    @abstractmethod
    def obtain_packages_data(self) -> list:
        '''
        Obtains the data of a list of package names from the data source.
        
        Returns
        -------
        list
            The data of a list of package names from the data source
        '''
    