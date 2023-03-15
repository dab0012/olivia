""""""
'''
·········································································
File: csv_network.py
Project: Olivia-Finder
Created Date: Wednesday March 8th 2023
Author: Daniel Alonso Báscones
Copyright (c) 2023 Daniel Alonso Báscones
·········································································
'''


import tqdm, os, pandas as pd
from typing import Dict, List, Optional
from typing_extensions import override
from olivia_finder.data_source import DataSource
from olivia_finder.util.logger import UtilLogger

class CSVNetwork(DataSource):
    """
    Class that implements the methods for loading a network from a CSV file.
    Implements the DataSource interface.
    
    Attributes
    ----------
    data : pd.DataFrame
        The data loaded from the CSV file
    dependent_field : str
        The name of the field that contains the dependent packages
    dependency_field : str
        The name of the field that contains the dependency packages
        
    Examples
    --------
    >>> from olivia_finder.csv_network import CSVNetwork
    >>> csv_network = CSVNetwork()
    >>> csv_network.load_data("data.csv", "dependent", "dependency")
    >>> package_names = csv_network.obtain_package_names()
    """
    
    # Attributes
    # ---------------------
    data: pd.DataFrame
    dependent_field: str
    dependency_field: str
    dependent_version_field: str
    dependent_url_field: str
    
    # Class Methods
    # ---------------------
    @classmethod
    def load_data(
            cls, 
            file_path:str, 
            dependent_field:str,
            dependency_field:str,
            dependent_version_field:str = None,
            dependency_version_field:str = None,
            dependent_url_field:str = None
        ):
        """
        Loads the data from a CSV file like [name,version,url,dependency,dependency_version]
        The dependent_version_field and dependent_url_field parameters are optional

        Parameters
        ----------
        file_path : str
            The path to the CSV file
        dependent_field : str
            The name of the field that contains the dependent package names
        dependency_field : str
            The name of the field that contains the dependency packages names
        dependent_version_field : str, optional
            The name of the field that contains the dependent packages versions, by default None
        dependent_url_field : str, optional
            The name of the field that contains the dependent packages urls, by default None
            
        Raises
        ------
        FileNotFoundError: Exception
            If the file does not exist
        ValueError: Exception
            If the file path is None
            If the file is not a CSV file
            If the dependent field is None
            If the dependency field is None
            If the dependent field and dependency field are the same
        """

        # Check the parameters are valid
        # ------------------------------
        if file_path is None:
            raise ValueError("File path cannot be None.")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        
        if not file_path.endswith(".csv"):
            raise ValueError(f"File {file_path} is not a CSV file.")
        
        if dependent_field is None:
            raise ValueError("Dependent field cannot be None.")
        
        if dependency_field is None:
            raise ValueError("Dependency field cannot be None.")
        
        if dependent_field == dependency_field:
            raise ValueError("Dependent field and dependency field cannot be the same.")
        
        # Load the data
        # -------------
        cls.data = pd.read_csv(file_path)
        
        # Check if the fields are in the data
        if dependent_field not in cls.data.columns:
            raise ValueError(f"Field {dependent_field} not found on data.")
        
        if dependency_field not in cls.data.columns:
            raise ValueError(f"Field {dependency_field} not found on data.")
        
        cls.dependent_field = dependent_field
        cls.dependency_field = dependency_field
        cls.dependent_url_field = dependent_url_field
        cls.dependent_version_field = dependent_version_field
        cls.dependency_version_field = dependency_version_field
        
        # Init the dictionary of packages with the pakages in the data
        package_names = cls.obtain_package_names()
        for package_name in package_names:
            cls.packages[package_name] = None
        
        return cls()

    # ---------------------
    #region Overridden methods
    @override
    def obtain_package_names(self) -> List[str]:
        # sourcery skip: inline-immediately-returned-variable, skip-sorted-list-construction
        """
        Obtains the list of packages from the data source, sorted alphabetically.

        Returns
        -------
        List[str]
            The list of package names in the data source        
        """
        package_names = list(self.data[self.dependent_field].unique())
        package_names.sort()
        
        return package_names
    
    @override
    def obtain_package_data(self, package_name: str) -> Dict:
        """
        Obtains the package from the dataframe
        
        Parameters
        ----------
        package_name : str
            The name of the package to obtain the data from
        
        Returns
        -------
        Dict
            The data of the package in the form of a dictionary
        """

        # Get the with dependent field == package_name
        package_rows = self.data[self.data[self.dependent_field] == package_name]
        
        if package_rows.empty:
            UtilLogger.log(f"Package {package_name} not found in data.")
            raise ValueError(f"Package {package_name} not found in data.")

        # Get the dependencies
        dependencies = []
        dependencies_data = package_rows.values.tolist()
        for dependency_data in dependencies_data:
            dependency_name = dependency_data[3]
            try:
                dependency_version = dependency_data[4]
            except IndexError:
                dependency_version = None

            # Build the dependency dictionary
            dependency = {
                "name": dependency_name,
                "version": dependency_version
            }

            # Add the dependency to the list
            dependencies.append(dependency)

        # Return the data
        return {
            "name": package_name,
            "version": package_rows[self.dependent_version_field].values[0] if self.dependent_version_field is not None else None,
            "url": package_rows[self.dependent_url_field].values[0] if self.dependent_url_field is not None else None,
            "dependencies": dependencies
        }
    
    @override
    def obtain_packages_data(self, package_name_list: Optional[List[str]] = None, progress_bar: Optional[tqdm.tqdm] = None) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Parameters
        ----------
        package_name_list : Optional[List[str]], optional
            The list of package names to obtain the data from, by default None
        progress_bar : Optional[tqdm.tqdm], optional
            The progress bar to use, by default None

        Returns
        -------
        List[Dict]
            The list of dictionaries containing the data of the packages
        '''
        
        # for each package name, obtain the data
        
        if package_name_list is None:
            package_name_list = self.obtain_package_names()
            
        progress_bar = tqdm.tqdm(package_name_list) if progress_bar is None else progress_bar
            
        packages = []
        for package_name in package_name_list:
            try:
                packages.append(self.obtain_package_data(package_name))
            except ValueError:
                UtilLogger.log(f"Package {package_name} not found in data.")
                self.not_found.append(package_name)
                continue
            
            progress_bar.update() if progress_bar is not None else None
            
        return packages

    #endregion
