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
from typing import Dict, List, Optional
from ..utilities.logger import MyLogger

class DataSource(ABC):
    """
    Base class for data sources.
    This class is an abstract class, so it cannot be instantiated.
    The subclasses must implement the methods obtain_package_names, obtain_package_data and obtain_packages_data.


    """

    def __init__(self, name: str, description: str, auxiliary_datasources: Optional[List[DataSource]] = None):
        
        self.name: str = name
        self.description: str = description
        self.packages_data: dict = {}

        # We initialize the auxiliary data sources if there are any
        if auxiliary_datasources is not None:
            self.auxiliary_datasources = auxiliary_datasources
        else:
            self.auxiliary_datasources = []

    def get_info(self) -> Dict:
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

    def _auxyliary_search(self, package_name: str) -> Optional[Dict]:
        """
        Auxiliary method for searching a package in the auxiliary data sources.

        Parameters
        ----------
        package_name : str
            The name of the package to search

        Returns
        -------
        Optional[Dict]
            The data of the package if it is found, None otherwise

        Raises
        ------
        NotFoundInDataSourceException
            If the package is not found in any of the auxiliary data sources
        """

        package_data = None
        for aux_ds in self.auxiliary_datasources:
            try:
                package_data = aux_ds.obtain_package_data(package_name)
                MyLogger.log(f'Package {package_name} found using the auxiliary datasource {aux_ds.name}')
                break

            except NotFoundInDataSourceException:
                MyLogger.log(f'Package {package_name} not found using the auxiliary datasource {aux_ds.name}')
                continue
        
        return package_data



    def generate_package_dependency_network(self, package_name: str, dependency_network: Dict = None, deep_level: int = 5) -> Dict[str, List[str]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        dependency_network : dict, optional
            The dependency network of the package            
        deep_level : int, optional
            The deep level of the dependency network, by default 5

        Returns
        -------
        Dict[str, List[str]]
            The dependency network of a package from the data source as a dictionary of package name to a list of its dependencies
        """

        if dependency_network is None:
            dependency_network = {}

        if deep_level == 0:
            return dependency_network
        
        # Obtain the data of target package
        try:
            target_data = self.obtain_package_data(package_name)
        except ValueError:
            MyLogger.log(
                f"The package {package_name} does not exist in the data source {self.name}"
            )
            return dependency_network
                #    
        # Append the target package to the dependency network
        dependency_network[package_name] = target_data['dependencies']
        
        # Run the method recursively for each dependency while the deep level is not reached
        for dependency in target_data['dependencies']:

            dependency_name = dependency["name"]

            # Check if package is already in the dependency network
            if dependency_name in dependency_network:
                continue

            try:     
                self.generate_package_dependency_network(
                    dependency_name,                # The name of the dependency
                    dependency_network,             # The global dependency network
                    deep_level - 1                  # The deep level is reduced by 1
                )
            except Exception:
                MyLogger.log(
                    f"The package {dependency_name}, as dependency of {package_name} does not exist in the data source {self.name}"
                )
                continue

        return dependency_network


    # Abstract methods
    # ----------------

    # Implement the methods obtain_package_names, obtain_package_data and obtain_packages_data in the subclasses

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
    def obtain_package_data(self, package_name:str) -> Dict:
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
    def obtain_packages_data(self) -> List[Dict]:
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
    
    
