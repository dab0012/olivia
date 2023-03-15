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
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class DataSource(ABC):
    """
    Interface class for data sources.
    
    Attributes
    ----------
    name : str
        Name of the data source
    description : str
        Description of the data source
    """
    # Attributes
    # ---------------------
    name: str                   # Name of the data source
    description: str            # Description of the data source
    
    # Methods
    # ---------------------
    def __init__(self, name:Optional[str] = None, description:Optional[str] = None):
        """
        Constructor,
        If name is not defined, its used the class name.
        If description is not defined, use the default one else use the one defined.
        """
        self.name = self.__class__.__name__ if name is None else name
        if description is None:
            self.description = "No description available."
        else:
            self.description = description
        
    def get_info(self) -> str:
        """
        Gets a string with the information of the data source.

        Returns
        -------
        str
            The information of the data source
        """

        return f"Name: {self.name}\nDescription: {self.description}"

    # ------------------------------------------------
    #region Abstract Methods

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.

        Returns
        -------
        List[str]
            The list of packages

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass
        """
        pass

    @abstractmethod
    def obtain_package_data(self, package_name: str, override_previous: Optional[bool] = True) -> Dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Parameters  
        ----------
        package_name : str
            The name of the package
        override_previous : Optional[bool], optional
            If the data is already obtained, override it, by default None

        Returns 
        -------
        Dict
            The data of the package

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass
        """
        pass
    
    @abstractmethod
    def obtain_packages_data(
        self, 
        package_name_list: Optional[List[str]] = None, 
        progress_bar: Optional[tqdm.tqdm] = None
    ) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Parameters
        ----------
        package_name_list : Optional[List[str]], optional
            The list of package names, by default None
        progress_bar : Optional[tqdm.tqdm], optional
            The progress bar, by default None
            
        Returns
        -------
        List[Dict]
            The list of packages data   
            
        Raises
        ------
        NotImplementedError
            If the method is not implemented in the subclass
        '''
        pass
    
    #endregion