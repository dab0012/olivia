from __future__ import annotations
import os
from typing import Dict, List, Optional
from typing_extensions import override
import pandas as pd
import tqdm
from ..util.logger import MyLogger
from .data_source import DataSource

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
    dependent_version_field : str
        The name of the field that contains the dependent packages versions
    dependency_version_field : str
        The name of the field that contains the dependency packages versions
    dependent_url_field : str
        The name of the field that contains the dependent packages urls
    
        
    Parameters
    ----------
    file_path : str
        Path to the CSV file with the data
    name : Optional[str]
        Name of the data source
    description : Optional[str]
        Description of the data source
    dependent_field : Optional[str]
        The name of the field that contains the dependent packages
    dependency_field : Optional[str]
        The name of the field that contains the dependency packages
    dependent_version_field : Optional[str]
        The name of the field that contains the dependent packages versions
    dependency_version_field : Optional[str]
        The name of the field that contains the dependency packages versions
    dependent_url_field : Optional[str]
        The name of the field that contains the dependent packages urls

    Examples
    --------
    >>> from olivia_finder.csv_network import CSVNetwork
    >>> csv_network = CSVNetwork()
    >>> csv_network.load_data("data.csv", "dependent", "dependency")
    >>> package_names = csv_network.obtain_package_names()
    """
    
    def __init__(
        self,
        file_path: str, 
        name: Optional[str] = None, 
        description: Optional[str] = None,
        dependent_field: Optional[str] = None,
        dependency_field: Optional[str] = None,
        dependent_version_field: Optional[str] = None,
        dependency_version_field: Optional[str] = None,
        dependent_url_field: Optional[str] = None,
    ):
        """
        Constructor of the class
        """

        # Set the name and description
        if name is None:
            name = "CSV Network"
        if description is None:
            description = "Network loaded from a CSV file"
        super().__init__(name, description)

        # Set the dataframe as None and the fields
        self.data: pd.DataFrame = None
        self.dependent_field: str = dependent_field
        self.dependency_field: str = dependency_field
        self.dependent_version_field: str = dependent_version_field
        self.dependency_version_field: str = dependency_version_field
        self.dependent_url_field: str = dependent_url_field
        self.file_path: str = file_path

        # Load the data if the file path is setted
        if self.file_path is not None:
            self._load_data()
        else:
            MyLogger().warning("File path is None. Data not loaded.")
            raise ValueError("File path cannot be None.")

    def _load_data(self):
        """
        Loads the data from a CSV file like [name,version,url,dependency,dependency_version]
        The dependent_version_field and dependent_url_field parameters are optional

        Parameters
        ----------
        file_path : str
            The path to the CSV file
            
        Raises
        ------
        FileNotFoundError: Exception
            If the file does not exist
        ValueError: Exception
            If the file path is None, If the file is not a CSV file, If the dependent field is None, 
            If the dependency field is None, If the dependent field and dependency field are the same
        """

        # Check the file is valid
        if self.file_path is None:
            raise ValueError("File path cannot be None.")
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found.")
        
        if not self.file_path.endswith(".csv"):
            raise ValueError(f"File {self.file_path} is not a CSV file.")
        
        # Check if the mandatory fields are setted and are valid
        if self.dependent_field is None:
            raise ValueError("Dependent field cannot be None.")
        
        if self.dependency_field is None:
            raise ValueError("Dependency field cannot be None.")
        
        if self.dependent_field == self.dependency_field:
            raise ValueError("Dependent field and dependency field cannot be the same.")
        
        # Load the data
        self.data = pd.read_csv(self.file_path)
        
        # Check if the other fields are in the data
        if self.dependent_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_field} not found on data.")
        
        if self.dependency_field not in self.data.columns:
            raise ValueError(f"Field {self.dependency_field} not found on data.")
        
        if self.dependent_version_field is not None and self.dependent_version_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_version_field} not found on data.")
        
        if self.dependency_version_field is not None and self.dependency_version_field not in self.data.columns:
            raise ValueError(f"Field {self.dependency_version_field} not found on data.")
        
        if self.dependent_url_field is not None and self.dependent_url_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_url_field} not found on data.")

        # Load the packages data
        self._load_packages_data()

    def _load_packages_data(self):
        """
        Loads the packages from the data
        """
        for index, row in self.data.iterrows():
            # Get the package name and version
            package_name = row[self.dependent_field]
            package_version = row[self.dependent_version_field] if self.dependent_version_field is not None else None
            package_url = row[self.dependent_url_field] if self.dependent_url_field is not None else None
            
            # Get the dependencies
            dependency_name = row[self.dependency_field]
            dependency_version = row[self.dependency_version_field] if self.dependency_version_field is not None else None
            
            # Check if the package data is on the dictionary
            if package_name not in self.packages_data:
                self.packages_data[package_name] = {
                    "name": package_name,
                    "version": package_version,
                    "url": package_url,
                    "dependencies": [],
                }

            # Add the dependency of the current row
            self.packages_data[package_name]["dependencies"].append({
                "name": dependency_name,
                "version": dependency_version,
            })

    @override
    def get_info(self):
        """
        Returns the information of the data source.
        """
        return {
            "name": self.name,
            "description": self.description,
        }
        
    @override
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source, sorted alphabetically.

        Returns
        -------
        List[str]
            The list of package names in the data source        
        """
        return sorted(self.data[self.dependent_field].unique())
    
    @override
    def obtain_package_data(self, package_name: str, override_previous: Optional[bool] = True) -> Dict:
        """
        Obtains the package from the dataframe
        
        Parameters
        ----------
        package_name : str
            The name of the package
        override_previous : Optional[bool]
            If True, it will override the previous data with the same name but different version
        
        Returns
        -------
        Dict
            The data of the package in the form of a dictionary

        Examples
        --------
        >>> data_source = CSVDataSource("test.csv", "name", "dependency")
        >>> data_source.obtain_package_data("package1")
            {
                "name": "package1",
                "version": "1.0.0",
                "url": "
                "dependencies": [
                    {
                        "name": "package2",
                        "version": "1.0.0"
                    },
                ]
            }
        """

        # Get the rows of the package
        package_rows = self.data[self.data[self.dependent_field] == package_name]

        # Remove the previous data with the same name but different version
        if override_previous:
            # Get the last row
            last_version = package_rows[self.dependent_version_field].max()
            package_rows = package_rows[package_rows[self.dependent_version_field] == last_version]

        if package_rows.empty:
            MyLogger.log(f"Package {package_name} not found in data.")
            raise ValueError(f"Package {package_name} not found in data.")

        # Get the dependencies
        dependencies = []

        # Get a list of rows
        package_rows = package_rows.to_dict("records")

        for row in package_rows:
            # Get the dependency name and version
            dependency_name = row[self.dependency_field]
            dependency_version = row[self.dependency_version_field] if self.dependency_version_field is not None else None
            
            # Build the dependency dictionary
            # Iggnore {'name': nan, 'version': nan}
            if pd.isna(dependency_name):
                continue

            dependency = {
                "name": dependency_name,
                "version": dependency_version
            }

            # Add the dependency to the list
            dependencies.append(dependency)

        # Return the data
        return {
            "name": package_name,
            "version": package_rows[0][self.dependent_version_field] if self.dependent_version_field is not None else None,
            "url": package_rows[0][self.dependent_url_field] if self.dependent_url_field is not None else None,
            "dependencies": dependencies
        }
    
    @override
    def obtain_packages_data(
        self, 
        package_name_list: Optional[List[str]] = None, 
        progress_bar: Optional[tqdm.tqdm] = None
    ) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the CSV file
        If the package name list is None, it will obtain the package names from the CSV file and load their data

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
        
        # If the package name list is None, obtain the package names from the csv data
        if package_name_list is None:
            package_name_list = self.obtain_package_names()
        
        # Define the list of packages and the list of not found packages
        packages = []
        not_found = []

        # Iterate over the package names and obtain the data
        for package_name in package_name_list:
            try:
                packages.append(self.obtain_package_data(package_name))

            # If the package is not found, add it to the not found list, and continue
            except ValueError:
                MyLogger.log(f"Package {package_name} not found in data.")
                not_found.append(package_name)
                continue
            
            if progress_bar is not None:
                progress_bar.update(1)
                        
        return packages, not_found
