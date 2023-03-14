'''
File:              repo.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:37:07 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import tqdm, pandas as pd
from typing import Dict, List, Optional, Union
from olivia_finder.package import Package
from olivia_finder.data_source import DataSource
import pickle

class PackageManager():
    '''
    Class that represents a package manager, which is a collection of packages
    
    Parameters
    ----------
    data_source : DataSource
        Data source of the package manager
        
    Raises
    ------
    ValueError
        If the data source is invalid
    
    Attributes
    ----------
    data_source : DataSource
        Data source of the package manager
    packages : set[Package]
        Set of packages of the package manager
        
    Examples
    --------
    >>> from olivia_finder.package_manager import PackageManager
    >>> from olivia_finder.data_source import DataSource
    >>> package_manager = PackageManager(DataSource())
    '''

    # Attributes
    data_source: DataSource
    packages: Dict[str, Package]

    def __init__(self, data_source: DataSource):
        '''
        Constructor
        '''
        if data_source is None:
            raise ValueError("Data source cannot be None")

        self.data_source = data_source
        self.packages = {}
    
    def save(self, path:str):
        '''
        Save the package manager to a file
        
        Parameters
        ----------
        path : str
            Path of the file to save the package manager
        '''
        # Use pickle to save the package manager
        
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path:str):
        '''
        Load the package manager from a file
        
        Parameters
        ----------
        path : str
            Path of the file to load the package manager
        '''

        pm: PackageManager = None

        # Try to load the package manager from the file
        try:
            # Use pickle to load the package manager
            with open(path, "rb") as f:
                pm = pickle.load(f)
        except Exception as e:
            print("Error loading the package manager from file:", e)
            return None
        
        return pm
    
    # --------------------------------
    #region Builders
    def obtain_package(self, package_name: str) -> Union[Package, None]:
        '''
        Builds a Package object from the package manager's data source

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        Union[Package, None]
            Package object if the package exists, None otherwise
            
        Examples
        --------
        >>> package = package_manager.obtain_package("package_name")
        >>> print(package.name)
        '''

        package_data = self.data_source.obtain_package_data(package_name)
        return None if package_data is None else Package.load(package_data)
    
    def obtain_packages(
        self, 
        package_names: Optional[List[str]] = None, 
        extend: Optional[bool] = False, 
        show_progress: Optional[bool] = False
    ) -> List[Package]:
        '''
        Obtain a list of packages from the package manager's data source

        Parameters
        ----------
        package_names : Optional[List[str]], optional
            List of package names to obtain, by default None
            
        extend : Optional[bool], optional
            If True, the packages will be added to the existing ones, by default False
        
        show_progress : Optional[bool], optional
            If True, a progress bar will be shown, by default False
        
        Returns
        -------
        List[Package]
            List of packages obtained from the data source
            
        Examples
        --------
        >>> packages = package_manager.obtain_packages()
        >>> print(packages[0].name)
        '''

        # Obtain the packages if the list is empty
        if package_names is None or len(package_names) == 0:
            package_names = self.data_source.obtain_package_names()

        progress_bar = tqdm.tqdm(total=len(package_names)) if show_progress else None
        packages_data = self.data_source.obtain_packages_data(package_names, progress_bar=progress_bar)
        package_list = [
            Package.load(pkg_data)
            for pkg_data in packages_data
            if pkg_data is not None
        ]
        if progress_bar is not None:
            progress_bar.close()

        # Add packages to the repo
        if extend:
            for package in package_list:
                self.packages[package.name] = package

        return package_list

    #endregion Builders
    # --------------------------------
    #region Loaders
    
    @classmethod
    def load_from_dict(cls, data):
        '''
        Load a dictionary into a PackageManager object

        Parameters
        ----------
        data : dict
            Dictionary to load
            
        Returns
        -------
        PackageManager
            PackageManager object loaded from the dictionary
            
        Raises
        ------
        PackageManagerLoadError
            If the dictionary does not have the structure of : {'name': str, 'url': str, 'packages': List[dict]}
        
        Examples
        --------
        >>> pm_dict = pm.to_dict()
        >>> pm = PackageManager.load_dict(pm_dict)
        >>> print(pm.name)
        >>> print(pm.url)
        '''
        try:
            pm_dict = cls(data['name'], data['url'])
            for package in data['packages']:
                pm_dict.packages.append(Package.load(package))
            return pm_dict
        except KeyError as e:
            raise PackageManagerLoadError(f"Invalid dictionary format: {e}") from e
    
    @classmethod
    def load_csv_adjlist(cls, csv_path: str):
        '''
        Load a csv file into a PackageManager object
        
        Parameters
        ----------
        csv_path : str
            Path to the csv file
        
        Returns
        -------
        PackageManager
            PackageManager object loaded from the csv file
            
        Raises
        ------
        PackageManagerLoadError
            If the csv file does not have the structure of : [name, version, url, dependency, dependency_version]
            
        Examples
        --------
        >>> pm = PackageManager.load_csv_adjlist('path/to/csv')
        >>> print(pm.name)
        >>> print(pm.url)
            
        '''

        data = pd.read_csv(csv_path, index_col=0)

        # If the csv does not have the structure of to_package_graph_with_dependencies it cannot be loaded
        if not {
            'name',
            'version',
            'url',
            'dependency',
            'dependency_version',
        }.issubset(data.columns):
            raise PackageManagerLoadError('The csv file does not have the structure of to_package_graph_with_dependencies')

        # We create a dictionary with the packages
        packages = {}
        for row in data.iterrows()[1]:
            if row['name'] not in packages:
                packages[row['name']] = Package(row['name'], row['version'], row['url'])
            else:
                packages[row['name']].version = row['version']
                packages[row['name']].url = row['url']

        # We add the dependencies
        for row in data.iterrows()[1]:
            if row['dependency'] not in packages:
                packages[row['dependency']] = Package(row['dependency'], row['dependency_version'])
            else:
                packages[row['dependency']].version = row['dependency_version']
            packages[row['name']].dependencies.append(packages[row['dependency']])

        # We create the package manager
        package_manager = cls('repo_name', 'url')
        package_manager.packages = list(packages.values())
        return package_manager
    
    #endregion
    # --------------------------------
    #region Getters
    
    def get_package(self, package_name: str) -> Union[Package, None]:
        '''
        Obtain a package from the package manager
        
        Parameters
        ----------
        package_name : str
            Name of the package
            
        Returns
        -------
        Union[Package, None]
            Package object if the package exists, None otherwise
            
        Examples
        --------
        >>> package = package_manager.get_package("package_name")
        >>> print(package.name)
        '''
        return self.packages.get(package_name, None)
    
    def get_package_list(self) -> List[Package]:
        '''
        Obtain the list of packages of the package manager
        
        Returns
        -------
        List[Package]
            List of packages of the package manager
            
        Examples
        --------
        >>> package_list = package_manager.get_package_list()
        '''
        return list(self.packages.values())
        
    #endregion
    # --------------------------------
    #region Export
    
    def export_adjlist(self) -> pd.DataFrame:
        '''
        Convert the object to a adjacency list, where each row represents a dependency
        If a package has'nt dependencies, it will appear in the list with dependency field empty
        
        Returns
        -------
        pd.DataFrame
            Dependency network as an adjacency list
        
        Examples
        --------
        >>> adj_list = package_manager.export_adjlist()
        >>> print(adj_list)
            [name, dependency]
        '''
        rows = []
        for package in self.packages:
            rows.extend(
                [package.name, dependency.name]
                for dependency in package.dependencies
            )
        return pd.DataFrame(rows, columns=['name', 'dependency'])
    
    def export_full_adjlist(self) -> pd.DataFrame:
        '''
        Convert the object to a adjacency list, where each row represents a dependency
        If a package has'nt dependencies, it will appear in the list with dependency field empty
        The version of the package and the dependency will be included
        
        Returns
        -------
        pd.DataFrame
            Dependency network as an adjacency list

        Examples
        --------
        >>> adj_list = package_manager.export_full_adjlist()
        >>> print(adj_list)
            [name, version, dependency, dependency_version]
        '''

        rows = []
        for package_name in self.packages:

            package = self.get_package(package_name)

            if package.dependencies:
                rows.extend(
                    [
                        package_name.name,
                        package_name.version,
                        package_name.url,
                        dependency["name"],
                        dependency["version"]
                    ]
                    for dependency in package_name.dependencies
                )
            else:
                rows.append([package_name.name, package_name.version, package_name.url, None, None])

        return pd.DataFrame(rows, columns=['name', 'version', 'url', 'dependency', 'dependency_version'])
    
    #endregion Export

class PackageManagerLoadError(Exception):
    """
    Raised when there is an error loading the package manager
    
    Attributes
    ----------
    message : str
        Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

