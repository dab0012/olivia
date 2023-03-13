'''
File:              csv_network.py
Project:           Olivia-Finder
Created Date:      Wednesday March 8th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Wednesday March 8th 2023 1:49:07 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''
import tqdm, os, pandas as pd
from typing import Dict, List, Optional
from typing_extensions import override
from olivia_finder.data_source import DataSource

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
    
    # Class Methods
    # ---------------------
    def load_data(self, file_path:str, dependent_field:str, dependency_field:str):
        """Loads the data from a CSV file.

        Parameters
        ----------
        file_path : str
            The path to the CSV file
        dependent_field : str
            The name of the field that contains the dependent packages
        dependency_field : str
            The name of the field that contains the dependency packages
            
        Raises
        ------
        FileNotFoundError
            If the file does not exist
        ValueError
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
        self.data = pd.read_csv(file_path)
        
        # Check if the fields are in the data
        if dependent_field not in self.data.columns:
            raise ValueError(f"Field {dependent_field} not found on data.")
        
        if dependency_field not in self.data.columns:
            raise ValueError(f"Field {dependency_field} not found on data.")
        
        self.dependent_field = dependent_field
        self.dependency_field = dependency_field

    # ---------------------
    #region Overridden methods
    @override
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source, sorted alphabetically.

        Returns
        -------
        List[str]
            The list of package names in the data source        
        """
        package_names = list(self.data[self.dependent_field].unique())
        return package_names.sort()
    
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

        # Get the dat rows of the package
        package_rows = self.data[self.data[self.dependent_field] == package_name]
        data = {row[self.dependency_field]: row["version"] for row in package_rows.iterrows()[1]}
        return data
    
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
            
        if progress_bar is None:
            progress_bar = tqdm.tqdm(package_name_list)
            
        return [self.obtain_package_data(package_name) for package_name in progress_bar]

    #endregion
