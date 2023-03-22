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

from typing import Dict, List

from ..util.logger import MyLogger
from .data_source_abc import DataSourceABC

class DataSource(DataSourceABC):
    """
    Base class for data sources, it implements the DataSourceABC interface.
    This class is not intended to be used directly, but to be inherited by
    other classes that must override this class's methods.
    """

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.packages_data: dict = {}

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

    def obtain_package_data(self, package_name:str) -> Dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError

    def obtain_packages_data(self) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        '''
        raise NotImplementedError

    def generate_package_dependency_network(self, package_name: str, deep_level: int = 5) -> Dict[str, List[str]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        deep_level : int, optional
            The deep level of the dependency network, by default 5

        Returns
        -------
        Dict[str, List[str]]
            The dependency network of a package from the data source as a dictionary of package name to a list of its dependencies
        """

        if deep_level == 0:
            return {}

        try:
            # self.obtain_package_data(package_name) returns a dictionary with the data of the package
            # as {name: ..., version: ..., dependencies: [{name: ..., version: ...}, ...]
            target_data = self.obtain_package_data(package_name)
            dependency_network = {}

            # Add an entry to the dependency network dictionary for the current package with a list of its dependencies
            dependency_network[package_name] = [dependency["name"] for dependency in target_data['dependencies']]

            # Run the method recursively for each dependency while the deep level is not reached
            for dependency in target_data['dependencies']:
                # Obtain the dependency network of the dependency
                dependency_name = dependency["name"]
                dependency_data = self.generate_package_dependency_network(
                    dependency_name,  # The name of the dependency
                    deep_level - 1  # The deep level is reduced by 1
                )

                # Merge the dependency network data of the dependency with the current dependency network dictionary
                for package, dependencies in dependency_data.items():
                    if package not in dependency_network:
                        dependency_network[package] = dependencies
                    else:
                        dependency_network[package] = list(set(dependency_network[package] + dependencies))

        except ValueError:
            MyLogger.log(
                f"The package {package_name} does not exist in the data source {self.name}"
            )
            return {}

        return dependency_network


