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

import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Optional

import tqdm

from .util import UtilLogger
from .package import Package

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
    use_logger: bool            # If True, use logger

    # Methods
    # ---------------------
    def __init__(self, name = None, description = None, use_logger = False):
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

        if use_logger:
            UtilLogger.init_logger()
        
    def get_info(self) -> str:
        """
        Gets a string with the information of the data source.

        ---
        Returns
        -   str (String with the information of the data source)
        """

        return f"Name: {self.name}\nDescription: {self.description}"

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
    def obtain_dependency_network(self, pckg_names: Optional[List[str]] = None, progress_bar: Optional[tqdm.tqdm] = None) -> List[Package]:
        '''
        Build a list of Package objects from a list of package names to be used as a dependency network

        ---
        Parameters
        -   pckg_names: List[str]   -> List of package names to be used as a dependency network
        -   progress_bar: tqdm.tqdm -> Progress bar to be used to show the progress of the operation

        ---
        Returns
        -   List[Package] -> List of Package objects
        '''
        pass