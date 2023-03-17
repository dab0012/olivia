""""""
'''
·········································································
File: data_source.py
Project: Olivia-Finder
Created Date: Monday March 6th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''

from abc import ABC, abstractmethod

class DataSourceABC(ABC):
    """
    Interface class for data sources.
    """

    @abstractmethod        
    def get_info(self):
        '''
        Returns the information of the data source.
        '''
        pass

    @abstractmethod
    def obtain_package_names(self):
        """
        Obtains the list of packages from the data source.
        """
        pass

    @abstractmethod
    def obtain_package_data(self):
        """
        Obtains the data of a package from the data source as a dictionary.
        """
        pass
    
    @abstractmethod
    def obtain_packages_data(self):
        '''
        Obtains the data of a list of package names from the data source.
        '''
        pass
    