
from __future__ import annotations
from typing import Dict, List, Optional, Union
import pickle
import tqdm
import pandas as pd

from .data_source.repository_scrapers.github import GithubScraper
from .utilities.config import Configuration
from .myrequests.request_handler import RequestHandler
from .data_source.scraper_ds import ScraperDataSource
from .utilities.logger import MyLogger
from .data_source.data_source import DataSource
from .data_source.csv_ds import CSVDataSource
from .package import Package
import networkx as nx


class PackageManager():
    '''
    Class that represents a package manager, which provides a way to obtain packages from a data source and store them
    in a dictionary
    '''

    def __init__(self, data_sources: Optional[List[DataSource]] = None):
        '''
        Constructor of the PackageManager class

        Parameters
        ----------

        data_sources : Optional[List[DataSource]]
            List of data sources to obtain the packages, if None, an empty list will be used

        Raises
        ------
        ValueError
            If the data_sources parameter is None or empty

        Examples
        --------
        >>> package_manager = PackageManager("My package manager", [CSVDataSource("csv_data_source", "path/to/file.csv")])
        '''

        if not data_sources:
            raise ValueError("Data source cannot be empty")

        self.data_sources: List[DataSource] = data_sources
        self.packages: Dict[str, Package] = {}
        # Init the logger for the package manager
        MyLogger.configure("logger_packagemanager")
        self.logger = MyLogger.get_logger(
            logger_name=Configuration().get_key('logger_packagemanager', 'name')
        )


    def save(self, path: str):
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
                del data_source.request_handler

        # Use pickle to save the package manager
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_from_persistence(cls, path: str):
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

        # Init the logger for the package manager
        MyLogger.configure("logger_packagemanager")
        logger = MyLogger.get_logger(
            logger_name=Configuration().get_key('logger_packagemanager', 'name')
        )

        # Try to load the package manager from the file
        try:
            # Use pickle to load the package manager
            logger.info(f"Loading package manager from {path}")
            with open(path, "rb") as f:
                obj = pickle.load(f)
                logger.info("Package manager loaded")
        except PackageManagerLoadError:
            logger.error(f"Error loading package manager from {path}")
            return None

        if not isinstance(obj, PackageManager):
            return None
        
        # Set the request handler for the scraper data sources
        for data_source in obj.data_sources:
            if isinstance(data_source, ScraperDataSource):
                data_source.request_handler = RequestHandler()

        obj.logger = logger

        return obj

    @classmethod
    def load_from_csv(
        cls,
        csv_path: str,
        dependent_field: Optional[str] = None,
        dependency_field: Optional[str] = None, 
        version_field: Optional[str] = None,
        dependency_version_field: Optional[str] = None,
        url_field: Optional[str] = None,
        default_format: Optional[bool] = False,
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

        # Init the logger for the package manager
        MyLogger.configure("logger_packagemanager")
        logger = MyLogger.get_logger(
            logger_name=Configuration().get_key('logger_packagemanager', 'name')
        )

        try:
            logger.info(f"Loading csv file from {csv_path}")
            data = pd.read_csv(csv_path)
        except Exception as e:
            logger.error(f"Error loading csv file: {e}")
            raise PackageManagerLoadError(f"Error loading csv file: {e}") from e

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
            logger.error("Invalid csv format")
            raise PackageManagerLoadError("Invalid csv format")

        # We create the data source
        data_source = CSVDataSource(
            file_path=csv_path,
            dependent_field=dependent_field,
            dependency_field=dependency_field,
            dependent_version_field=version_field,
            dependency_version_field=dependency_version_field,
            dependent_url_field=url_field
        )

        obj = cls([data_source])

        # Add the logger to the package manager
        obj.logger = logger
        
        # return the package manager
        return obj

    def initialize(
        self, 
        package_names: Optional[List[str]] = None, 
        show_progress: Optional[bool] = False, 
        chunk_size: Optional[int] = 10000):
        '''
        Initializes the package manager by loading the packages from the data source

        Parameters
        ----------
        package_list : List[str]
            List of package names to load, if None, all the packages will be loaded
        show_progress : bool
            If True, a progress bar will be shown
        chunk_size : int
            Size of the chunks to load the packages, this is done to avoid memory errors

        .. warning:: for large package lists, this method can take a long time to complete

        '''

        # Get package names from the data sources if needed
        if package_names is None:
            for data_source in self.data_sources:
                try:
                    package_names = data_source.obtain_package_names()
                    break
                except NotImplementedError:
                    self.logger.debug(f"Data source does not implement obtain_package_names method")
                    continue
                except Exception as e:
                    self.logger.error(f"Error while obtaining package names from data source: {e}")
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
            self.fetch_packages(
                package_names=package_names, 
                progress_bar=progress_bar,
                extend=True
            )
        
        # Close the progress bar if needed
        if progress_bar is not None:
            progress_bar.close()

    def fetch_package(self, package_name: str) -> Union[Package, None]:
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
            
            if isinstance(data_source, GithubScraper):
                package_data = data_source.obtain_package_data(package_name)
                if package_data is not None:
                    self.logger.debug(f"Package {package_name} found using {data_source.__class__.__name__}")
                    break
                else:
                    self.logger.debug(f"Package {package_name} not found using {data_source.__class__.__name__}")

            
            package_data = data_source.obtain_package_data(package_name)
            if package_data is not None:
                self.logger.debug(f"Package {package_name} found using {data_source.__class__.__name__}")
                break
            else:
                self.logger.debug(f"Package {package_name} not found using {data_source.__class__.__name__}")

        # Return the package if it exists
        return None if package_data is None else Package.load(package_data)

    def fetch_packages(
        self,
        package_names: List[str],
        progress_bar: Optional[tqdm.tqdm],
        extend: bool = False
    ) -> List[Package]:
        '''
        Builds a list of Package objects using the data sources in order until one of them returns a valid package

        Parameters
        ----------
        package_names : List[str]
            List of package names
        progress_bar : tqdm.tqdm
            Progress bar to show the progress of the operation
        extend : bool
            If True, the packages will be added to the existing ones, otherwise, the existing ones will be replaced

        Returns
        -------
        List[Package]
            List of Package objects
            
        Examples
        --------
        >>> packages = package_manager.obtain_packages(["package_name_1", "package_name_2"])
        >>> packages
        [<Package: package_name_1>, <Package: package_name_2>]
        '''

        # Check if the package names are valid
        if not isinstance(package_names, list):
            raise ValueError("Package names must be a list")

        preferred_data_source = self.data_sources[0]

        # Return list
        packages = []

        # if datasource is instance of ScraperDataSource use the obtain_packages_data method for parallelization
        if isinstance(preferred_data_source, ScraperDataSource):
            
            packages_data = []
            data_found, not_found = preferred_data_source.obtain_packages_data(
                package_names=package_names, 
                progress_bar=progress_bar # type: ignore
            )
            packages_data.extend(data_found)
            # pending_packages = not_found
            self.logger.info(f"Packages found: {len(data_found)}, Packages not found: {len(not_found)}")
            packages = [Package.load(package_data) for package_data in packages_data]
            
        # if not use the obtain_package_data method for sequential processing using the data_sources of the list
        else:

            while len(package_names) > 0:
                
                package_name = package_names[0]
                package_data = self.fetch_package(package_name)
                if package_data is not None:
                    packages.append(package_data)

                # Remove the package from the pending packages
                del package_names[0]

                if progress_bar is not None:
                    progress_bar.update(1)
        
        self.logger.info(f"Total packages found: {len(packages)}")
        
        # update the self.packages attribute overwriting the packages with the same name
        # but conserving the other packages
        if extend:
            self.logger.info("Extending data source with obtained packages")
            for package in packages:
                self.packages[package.name] = package

        return packages
            
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

    def get_packages(self) -> List[Package]:
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

    def package_names(self) -> List[str]:
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

    def fetch_package_names(self) -> List[str]:
        '''
        Obtain the list of package names of the package manager

        Returns
        -------
        List[str]
            List of package names of the package manager

        Examples
        --------
        >>> package_names = package_manager.obtain_package_names()
        '''

        return self.data_sources[0].obtain_package_names()

    def export_dataframe(self, full_data = False) -> pd.DataFrame:
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
            self.logger.debug("The package manager is empty")
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

    def get_adjlist(
            self, 
            package_name: str, 
            adjlist: Optional[Dict] = {}, 
            deep_level: int = 5,
        ) -> Dict[str, List[str]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        adjlist : Optional[Dict], optional
            The dependency network of the package, by default {}
        deep_level : int, optional
            The deep level of the dependency network, by default 5

        Returns
        -------
        Dict[str, List[str]]
            The dependency network of the package
        """

        # If the deep level is 0, we return the dependency network (Stop condition)
        if deep_level == 0:
            return adjlist
        
        # If the dependency network is not specified, we create it (Initial case)
        if adjlist is None:
            adjlist = {}

        # If the package is already in the dependency network, we return it (Stop condition)
        if package_name in adjlist:
            return adjlist

        # Use the data of the package manager
        current_package = self.get_package(package_name)
        dependencies =  current_package.get_dependency_names() if current_package is not None else []

        # Get the dependencies of the package and add it to the dependency network if it is not already in it
        adjlist[package_name] = dependencies
            
        # Append the dependencies of the package to the dependency network
        for dependency_name in dependencies:

            if (dependency_name not in adjlist) and  (self.get_package(dependency_name) is not None):
                    
                adjlist = self.get_adjlist(
                    package_name = dependency_name, 
                    adjlist = adjlist, 
                    deep_level = deep_level - 1,
                )
    
        return adjlist

    def fetch_adjlist(self, package_name: str, deep_level: int = 5, adjlist: dict = None) -> Dict[str, List[str]]:
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
        Dict[str, List[str]]
            The dependency network of the package
        """

        if adjlist is None:
            adjlist = {}

        # If the deep level is 0, we return the adjacency list (Stop condition) 
        if deep_level == 0 or package_name in adjlist:
            return adjlist

        dependencies = []
        try:
            current_package = self.fetch_package(package_name)
            dependencies = current_package.get_dependencies_names()

        except Exception:
            self.logger.debug(f"Package {package_name} not found")

        # Add the package to the adjacency list if it is not already in it
        adjlist[package_name] = dependencies

        # Append the dependencies of the package to the adjacency list if they are not already in it
        for dependency_name in dependencies:
            if dependency_name not in adjlist:
                try:     
                    adjlist = self.fetch_adjlist(
                        package_name=dependency_name,                # The name of the dependency
                        deep_level=deep_level - 1,                   # The deep level is reduced by 1
                        adjlist=adjlist                              # The global adjacency list
                    )
                except Exception:
                    self.logger.debug(
                        f"The package {dependency_name}, as dependency of {package_name} does not exist in the data source"
                    )

        return adjlist

    def __add_chunk(self,
        df, G,
        filter_field=None,
        filter_value=None
    ):
        
        filtered = df[df[filter_field] == filter_value] if filter_field else df
        links = list(zip(filtered["dependency"], filtered["name"]))
        G.add_edges_from(links)
        return G

    def get_network(
        self,
        chunk_size = int(1e6),
        filter_field=None,
        filter_value=None,
    ) -> nx.DiGraph:
        """
        Builds a dependency network from a dataframe of dependencies.
        The dataframe must have two columns: dependent and dependency.

        Parameters
        ----------
        chunk_size : int
            Number of rows to process at a time
        dependent_field : str
            Name of the column containing the dependent
        dependency_field : str
            Name of the column containing the dependency
        filter_field : str, optional
            Name of the column to filter on, by default None
        filter_value : str, optional
            Value to filter on, by default None

        Returns
        -------
        nx.DiGraph
            Directed graph of dependencies
        """


        # If the default dtasource is a CSV_Datasource, we use custom implementation
        defaul_datasource = self.get_default_datasource()
        if isinstance(defaul_datasource, CSVDataSource):
            return nx.from_pandas_edgelist(defaul_datasource.data, source="name", target="dependency", create_using=nx.DiGraph())

        # If the default datasource is not a CSV_Datasource, we use the default implementation
        df = self.export_dataframe()
        try:
            # New NetworkX directed Graph
            G = nx.DiGraph()
            
            for i in range(0, len(df), chunk_size):
                chunk = df.iloc[i:i+chunk_size]
                # Add dependencies from chunk to G
                G = self.__add_chunk(
                    chunk,
                    G,
                    filter_field=filter_field,
                    filter_value=filter_value
                )
        
            return G
        
        except Exception as e:
            print('\n', e)

    def get_dependency_network(self, package_name: str, deep_level: int = 5, generate = False) -> nx.DiGraph:
        """
        Gets the dependency network of a package from the data source as a NetworkX graph.

        Parameters
        ----------
        package_name : str
            The name of the package to get the dependency network
        deep_level : int, optional
            The deep level of the dependency network, by default 5

        Returns
        -------
        nx.DiGraph
            The dependency network of the package
        """

        if generate:
            # Get the dependency network from the data source
            dependency_network = self.fetch_adjlist(package_name=package_name, deep_level=deep_level, adjlist={})

        else:
            # Get the dependency network from in-memory data
            dependency_network = self.get_adjlist(package_name=package_name, deep_level=deep_level)

        # Create a NetworkX graph from the dependency network
        G = nx.DiGraph()
        for package_name, dependencies in dependency_network.items():
            for dependency_name in dependencies:
                G.add_edge(package_name, dependency_name)

        return G
    
    def get_default_datasource(self):
        """
        Gets the default data source

        Returns
        -------
        DataSource
            The default data source
        """

        return self.data_sources[0] if len(self.data_sources) > 0 else None

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

