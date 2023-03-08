'''
File:              data_source.py
Project:           Olivia-Finder
Created Date:      Monday March 6th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Monday March 6th 2023 6:45:45 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''


from abc import ABC, abstractmethod
import os
from typing import List

import pandas as pd
from olivia_finder.package import Package

class DataSource(ABC):
    """
    Interface class for data sources.
    """
    # Attributes
    # ---------------------
    name: str                   # Name of the data source
    description: str            # Description of the data source
    PERSISTENCE_PATH:str        # Path to the persistence directory
    data: pd.DataFrame          # Data loaded from file

    # Methods
    # ---------------------
    def __init__(self, name = None, description = None):
        """
        Constructor

        ---
        Parameters
        -   name : str          (Name of the data source)
        -   description : str   (Description of the data source)

        """
        # If name is not defined, use the class name
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

        # if description is not defined, use the default one else use the one defined
        if description is None:
            self.description = "No description available."
        else:
            self.description = description
        
        
    def get_info(self) -> str:
        """
        Gets a string with the information of the data source.

        ---
        Returns
        -   str (String with the information of the data source)
        """
        return f"{self.name}: {self.description}, last updated on {self.last_update}"

    # Abstract methods to be implemented in subclasses
    # ------------------------------------------------

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.

        ---
        Returns
        -   List[str]   (List of package names)
        """
        pass

    @abstractmethod
    def obtain_package(self, package_name: str) -> Package:
        """
        Obtains the package from the data source given its name.
        To be implemented in subclasses.

        ---
        Parameters
        -   package_name: str  (Name of the package)

        ---
        Returns
        -   Package (Package object)
        """
        pass
    
    @abstractmethod
    def obtain_dependency_network(self, pckg_names: List[str] = None, progress = None) -> List[Package]:
        '''
        Build a list of Package objects from a list of package names to be
        used as a dependency network

        Parameters
        ----------
        pckg_names : List[str]
            List of package names

        Returns
        -------
        list
            List of Package objects
        '''
        pass