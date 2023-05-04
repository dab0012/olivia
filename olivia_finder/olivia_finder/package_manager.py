'''
Description
-----------

Module that contains the PackageManager class, which represents a package manager, which provides a 
way to obtain packages from a data source and store them

File information:
    - File: package_manager.py
    - Project: olivia_finder
    - Created Date: 2023-03-18 14:40:56
    - Author: Daniel Alonso Báscones
    - Copyright (c) 2023 Daniel Alonso Báscones
'''

from __future__ import annotations
from typing import Optional, Union
import pickle
import tqdm
import pandas as pd

from .myrequests.request_handler import RequestHandler
from .data_source.scraper_ds import ScraperDataSource
from .utilities.logger import MyLogger
from .data_source.data_source import DataSource
from .data_source.csv_ds import CSVDataSource
from .package import Package

class PackageManager():
    '''
    '''

    def __init__(self, name: str, data_sources: list[DataSource] = None):
        '''
        Constructor
        '''

        self.name: str = name

        if data_sources is None or not data_sources:
            raise ValueError("Data source cannot be None")

        self.data_sources: list[DataSource] = data_sources
        self.packages: dict[str, Package] = {}

    def save_package_manager(self, path: str):
        '''
        Saves the package manager to a file, normally it has the extension .olvpm for easy identification
        as an Olivia package manager file

        Parameters
        ----------
        path : str
            Path of the file to save the package manager
        '''

        # Remove redundant objects
        for data_source in self.data_sources:
            if isinstance(data_source, ScraperDataSource):
                data_source.request_handler = None

        # Use pickle to save the package manager
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_package_manager(cls, path: str):
        '''
        Load the package manager from a file, the file must have been created with the save method
        Normally, it has the extension .olvpm

        Parameters
        ----------
        path : str
            Path of the file to load the package manager

        Returns
        -------
        Union[PackageManager, None] 
            PackageManager object if the file exists and is valid, None otherwise
        '''
        # Try to load the package manager from the file
        try:
            # Use pickle to load the package manager
            with open(path, "rb") as f:
                obj = pickle.load(f)
        except PackageManagerLoadError:
            return None

        if not isinstance(obj, PackageManager):
            return None
        # Set the request handler for the scraper data sources
        for data_source in obj.data_sources:
            if isinstance(data_source, ScraperDataSource):
                data_source.request_handler = RequestHandler()

        return obj

    def initialize(self, package_names: list[str] = None, show_progress: bool = False, chunk_size: int = 10000):
        '''
        Initializes the package manager by loading the packages from the data source

        Parameters
        ----------
        package_list : list[str]
            List of package names to load, if None, all the packages will be loaded
        show_progress : bool
            If True, a progress bar will be shown
        chunk_size : int
            Size of the chunks to load the packages, this is done to avoid memory errors            
        '''

        # Get package names from the data sources if needed
        if package_names is None:
            for data_source in self.data_sources:
                try:
                    package_names = data_source.obtain_package_names()
                    break
                except NotImplementedError:
                    MyLogger().get_logger().debug(f"Data source {data_source.name} does not implement obtain_package_names method")
                    continue
                except Exception as e:
                    MyLogger().get_logger().error(f"Error while obtaining package names from data source {data_source.name}: {e}")
                    continue

        # Check if the package names are valid
        if package_names is None or not isinstance(package_names, list):
            raise ValueError("No valid package names found")
        
        # Instantiate the progress bar if needed
        progress_bar = tqdm.tqdm(
            total=len(package_names),
            colour="green",
            desc="Loading packages",
            unit="packages",
        ) if show_progress else None

        # Create a chunked list of package names
        # This is done to avoid memory errors
        package_names_chunked = [package_names[i:i + chunk_size] for i in range(0, len(package_names), chunk_size)]

        for package_names in package_names_chunked:
            # Obtain the packages data from the data source and store them
            self.obtain_packages(
                package_names=package_names, 
                progress_bar=progress_bar,
                extend=True
            )


    def obtain_package(self, package_name: str) -> Union[Package, None]:
        '''
        Builds a Package object using the data sources in order until one of them returns a valid package

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
        >>> package
        <Package: package_name>
        '''
        # Obtain the package data from the data sources in order
        package_data = None
        for data_source in self.data_sources:
            package_data = data_source.obtain_package_data(package_name)
            if package_data is not None:
                MyLogger().get_logger().debug(f"Package {package_name} found using {data_source.name}")
                break
            else:
                MyLogger().get_logger().debug(f"Package {package_name} not found using {data_source.name}")

        # Return the package if it exists
        return None if package_data is None else Package.load(package_data)

    def obtain_packages(
        self,
        package_names: Optional[list[str]],
        progress_bar: Optional[tqdm.tqdm],
        extend: bool = False
    ) -> list[Package]:
        '''
        '''

        # Check if the package names are valid
        if package_names is not None and not isinstance(package_names, list):
            raise ValueError("Package names must be a list")

        # Obtain the packages data from the data source
        pending_packages = package_names.copy()
        packages_data = []
        preferred_data_source = self.data_sources[0]

        # if datasource is instance of ScraperDataSource use the obtain_packages_data method for parallelization
        if isinstance(preferred_data_source, ScraperDataSource):
            
            data_found, not_found = preferred_data_source.obtain_packages_data(
                package_names=pending_packages, 
                progress_bar=progress_bar
            )
            packages_data.extend(data_found)
            # pending_packages = not_found
            MyLogger().get_logger().info(f"Packages found: {len(data_found)}")
            MyLogger().get_logger().info(f"Packages not found: {len(not_found)}")

        # if not use the obtain_package_data method for sequential processing using the data_sources of the list
        else:

            for package_name in pending_packages:
                package_data = self.obtain_package(package_name)
                if package_data is not None:
                    packages_data.append(package_data)
                pending_packages.remove(package_name)

                if progress_bar is not None:
                    progress_bar.update(1)

        if progress_bar is not None:
            progress_bar.close()
        
        MyLogger().get_logger().info(f"Total packages found: {len(packages_data)}")
        packages = [Package.load(package_data) for package_data in packages_data]

        # update the self.packages attribute overwriting the packages with the same name
        # but conserving the other packages
        if extend:
            MyLogger().get_logger().info(f"Extending data source with obtained packages")
            for package in packages:
                self.packages[package.name] = package

        return packages
            
    @classmethod
    def load_csv_adjlist(
        cls,
        csv_path: str,
        dependent_field: str = None,
        dependency_field: str = None, 
        version_field: str = None,
        dependency_version_field: str = None,
        url_field: str = None,
        default_format: bool = False
    ) -> PackageManager:
        '''
        Load a csv file into a PackageManager object

        Parameters
        ----------
        csv_path : str
            Path of the csv file to load
        dependent_field : str = None, optional
            Name of the dependent field, by default None
        dependency_field : str = None, optional
            Name of the dependency field, by default None
        version_field : str = None, optional
            Name of the version field, by default None
        dependency_version_field : str = None, optional
            Name of the dependency version field, by default None
        url_field : str = None, optional
            Name of the url field, by default None
        default_format : bool, optional
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
            raise PackageManagerLoadError(
                f"Error loading csv file: {e}") from e

        csv_fields = []

        if default_format:
            # If the csv has the structure of full_adjlist.csv, we use the default fields
            dependent_field = 'name'
            dependency_field = 'dependency'
            version_field = 'version'
            dependency_version_field = 'dependency_version'
            url_field = 'url'
            csv_fields = [dependent_field, dependency_field,
                        version_field, dependency_version_field, url_field]
        else:
            if dependent_field is None or dependency_field is None:
                raise PackageManagerLoadError(
                    "Dependent and dependency fields must be specified")

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
        data_source = CSVDataSource(
            file_path=csv_path,
            name="Package Manager CSV",
            description="Package Manager obtained from a csv file",
            dependent_field=dependent_field,
            dependency_field=dependency_field,
            dependent_version_field=version_field,
            dependency_version_field=dependency_version_field,
            dependent_url_field=url_field
        )

        # We create the package manager
        return cls(data_source)

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

    def list_packages(self) -> list[Package]:
        '''
        Obtain the list of packages of the package manager

        Returns
        -------
        list[Package]
            List of packages of the package manager

        Examples
        --------
        >>> package_list = package_manager.get_package_list()
        '''
        return list(self.packages.values())

    def list_package_names(self) -> list[str]:
        '''
        Obtain the list of package names of the package manager

        Returns
        -------
        list[str]
            List of package names of the package manager

        Examples
        --------
        >>> package_names = package_manager.get_package_names()
        '''
        return list(self.packages.keys())

    def export_adjlist(self, full_data = False) -> pd.DataFrame:
        '''
        Convert the object to a adjacency list, where each row represents a dependency
        If a package has'nt dependencies, it will appear in the list with dependency field empty

        Parameters
        ----------
        full_data : bool, optional
            If True, the adjacency list will contain the version and url of the packages, by default False

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

        if not self.packages:
            MyLogger().get_logger().debug("The package manager is empty")
            return pd.DataFrame()
                    

        rows = []

        if full_data:
            for package_name in self.packages.keys():
                package = self.get_package(package_name)


                for dependency in package.dependencies:
                    
                    try:
                        dependency_full = self.get_package(dependency.name)
                        rows.append(
                            [package.name, package.version, package.url, dependency_full.name, dependency_full.version, dependency_full.url]
                        )
                    except Exception:
                        if dependency.name is not None:
                            rows.append(
                                [package.name, package.version, package.url, dependency.name, None, None]
                            )


            return pd.DataFrame(rows, columns=['name', 'version', 'url', 'dependency', 'dependency_version', 'dependency_url'])
        else:
            for package_name in self.packages.keys():
                package = self.get_package(package_name)
                rows.extend(
                    [package.name, dependency.name]
                    for dependency in package.dependencies
                )
            return pd.DataFrame(rows, columns=['name', 'dependency'])

    def dependency_network(
            self, 
            package_name: str, 
            dependency_network: dict = None, 
            deep_level: int = 5,
            generate = False
        ) -> dict[str, list[Package]]:
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
        generate : bool, optional
            If True, the dependency network will be generated from the data source, by default False

        Returns
        -------
        dict[str, list[Package]]
            The dependency network of the package
        """

        # If the deep level is 0, we return the dependency network (Stop condition)
        if deep_level == 0:
            return dependency_network
        
        # If the dependency network is not specified, we create it (Initial case)
        if dependency_network is None:
            dependency_network = {}

        # If the dependency network is not specified, we create it obtaining the data from the package manager
        if generate:
            return self._generate_dependency_network(package_name, deep_level, dependency_network)
        
        # Use the data of the package manager
        current_package = self.get_package(package_name)
        if (current_package is not None) and (package_name not in dependency_network):

            # Get the dependencies of the package and add it to the dependency network if it is not already in it
            dependencies = current_package.get_dependencies_names()
            if dependencies:
                dependency_network[package_name] = dependencies
            
        # Append the dependencies of the package to the dependency network
        for dependency_name in dependencies:
            if (dependency_name not in dependency_network) and  (self.get_package(dependency_name) is not None):
                    
                dependency_network = self.dependency_network(
                    package_name = dependency_name, 
                    dependency_network = dependency_network, 
                    deep_level = deep_level - 1,
                    generate = False
                )
    
        return dependency_network

    def _generate_dependency_network(self, package_name: str, deep_level: int = 5, dependency_network: dict = None) -> dict[str, list[Package]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        deep_level : int, optional
            The deep level of the dependency network, by default 5
        dependency_network : dict, optional
            The dependency network of the package

        Returns
        -------
        dict[str, list[Package]]
            The dependency network of the package
        """
        
        # Obtain the data of target package
        try:
            current_package = self.obtain_package(package_name)
        except ValueError:
            MyLogger().get_logger().debug(
                f"The package {package_name} does not exist in the data source {self.name}"
            )
            return dependency_network

        # Get the dependencies of the package and add it to the dependency network if it is not already in it
        dependencies = current_package.get_dependencies_names()

        if (package_name not in dependency_network) and dependencies:
            dependency_network[package_name] = []

            # Append the dependencies of the target package to the dependency network
            for dependency_name in dependencies:
                dependency_network[package_name].append(dependency_name)

                if dependency_name in dependency_network:
                    continue
                try:     
                    self.dependency_network(
                        dependency_name,                # The name of the dependency
                        dependency_network,             # The global dependency network
                        deep_level - 1,                 # The deep level is reduced by 1
                        generate = True                 # The dependency network is generated
                    )

                except Exception:
                    MyLogger().get_logger().debug(
                        f"The package {dependency_name}, as dependency of {package_name} does not exist in the data source {self.name}"
                    )
        return dependency_network

class PackageManagerLoadError(Exception):
    """
    Exception raised when an error occurs while loading a package manager

    Attributes
    ----------
    message : str
        Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PackageManagerSaveError(Exception):
    """
    Exception raised when an error occurs while saving a package manager

    Attributes
    ----------
    message : str
        Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

