""""""
'''
·········································································
File: package_manager.py
Project: Olivia-Finder
Created Date: Monday March 6th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''



import tqdm, pandas as pd
from typing import Dict, List, Optional, Union
from olivia_finder.csv_network import CSVNetwork
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
    # region Builders
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
    # region Loaders
    
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
    def load_csv_adjlist(
        cls,
        csv_path: str,
        dependent_field: Optional[str] = None,
        dependency_field: Optional[str] = None,
        version_field: Optional[str] = None,
        dependency_version_field: Optional[str] = None,
        url_field: Optional[str] = None,
        default_format: Optional[bool] = False
    ):
        '''
        Load a csv file into a PackageManager object
        
        Parameters
        ----------
        csv_path : str
            Path of the csv file to load
        dependent_field : Optional[str], optional
            Name of the dependent field, by default None
        dependency_field : Optional[str], optional
            Name of the dependency field, by default None
        version_field : Optional[str], optional
            Name of the version field, by default None
        dependency_version_field : Optional[str], optional
            Name of the dependency version field, by default None
        url_field : Optional[str], optional
            Name of the url field, by default None
        default_format : Optional[bool], optional
            If True, the csv has the structure of full_adjlist.csv, by default False
        
        Examples
        --------
        >>> pm = PackageManager.load_csv_adjlist(
            "full_adjlist.csv", 
            dependent_field="dependent", 
            dependency_field="dependency", 
            version_field="version", 
            dependency_version_field="dependency_version", 
            url_field="url"
        )
        >>> pm = PackageManager.load_csv_adjlist("full_adjlist.csv", default_format=True)
        
        '''
        try:
            data = pd.read_csv(csv_path)
        except Exception as e:
            raise PackageManagerLoadError(f"Error loading csv file: {e}") from e

        csv_fields = []

        if default_format:
            # If the csv has the structure of full_adjlist.csv, we use the default fields
            dependent_field = 'name'
            dependency_field = 'dependency'
            version_field = 'version'
            dependency_version_field = 'dependency_version'
            url_field = 'url'
            csv_fields = [dependent_field, dependency_field, version_field, dependency_version_field, url_field]
        else:
            if dependent_field is None or dependency_field is None:
                raise PackageManagerLoadError("Dependent and dependency fields must be specified")

            csv_fields = [dependent_field, dependency_field]
            # If the optional fields are specified, we add them to the list
            if version_field is not None:
                csv_fields.append(version_field)
            if dependency_version_field is not None:
                csv_fields.append(dependency_version_field)
            if url_field is not None:
                csv_fields.append(url_field)

        # If the csv does not have the specified fields, we raise an error
        if any(col not in data.columns for col in csv_fields):
            raise PackageManagerLoadError("Invalid csv format")

        # We create the data source
        data_source = CSVNetwork.load_data(
            csv_path, dependent_field, dependency_field, version_field, dependency_version_field, url_field
        )
        data_source.name = "CSV File"
        data_source.url = csv_path

        # We create the package manager
        cls = cls(data_source)
        
        return cls


    #endregion
    # --------------------------------
    # region Getters
    
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
    
    def get_package_names(self) -> List[str]:
        '''
        Obtain the list of package names of the package manager
        
        Returns
        -------
        List[str]
            List of package names of the package manager
            
        Examples
        --------
        >>> package_names = package_manager.get_package_names()
        '''
        return list(self.packages.keys())
        
    #endregion
    # --------------------------------
    # region Export
    
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
                        package.name,
                        package.version,
                        package.url,
                        dependency.name,
                        dependency.version
                    ]
                    for dependency in package.dependencies
                )
            else:
                rows.append([package.name, package.version, package.url, None, None])

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

