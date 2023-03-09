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

import tqdm
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .util.logger import UtilLogger

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
        -   List[str] -> List of package names
        """
        pass

    @abstractmethod
    def obtain_package_data(self, package_name: str) -> Dict:
        """
        Obtains the data of a package from the data source.

        ---
        Parameters
        -   package_name: str -> Name of the package to be obtained

        ---
        Returns
        -   Dict -> Dictionary with the data of the package
        """
        pass
    
    @abstractmethod
    def obtain_packages_data(self, pckg_names: Optional[List[str]] = None, progress_bar: Optional[tqdm.tqdm] = None) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        ---
        Parameters
        -   pckg_names: List[str]  -> List of package names to be obtained
        -   progress_bar: tqdm.tqdm -> Progress bar to show the progress

        ---
        Returns
        -   List[Dict] -> List of dictionaries with the data of the packages
        '''
        pass


    def enable_logger(self):
        """
        Enables the logger
        """
        UtilLogger.enable_logger()

    def disable_logger(self):
        """
        Disables the logger
        """
        UtilLogger.disable_logger()