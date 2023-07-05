
from __future__ import annotations
import os
from typing import List, Optional
import pandas as pd
import tqdm
from .data_source import DataSource

class CSVDataSource(DataSource):
    """
    Class that implements the methods for loading a network from a CSV file.
    Implements the **DataSource** abstract class.
    
    """
    
    def __init__(
        self,
        file_path: str, 
        dependent_field: Optional[str] = None,
        dependency_field: Optional[str] = None,
        dependent_version_field: Optional[str] = None,
        dependency_version_field: Optional[str] = None,
        dependent_url_field: Optional[str] = None
    ):
        """
        Constructor of the class

        Parameters
        ----------
        file_path : str
            The path to the CSV file
        dependent_field : str, optional
            The name of the field that contains the dependent packages, by default None
        dependency_field : str, optional
            The name of the field that contains the dependency packages, by default None
        dependent_version_field : str, optional
            The name of the field that contains the dependent packages versions, by default None
        dependency_version_field : str, optional
            The name of the field that contains the dependency packages versions, by default None
        dependent_url_field : str, optional
            The name of the field that contains the dependent packages urls, by default None

        Raises
        ------
        ValueError
            If the file path is None, If the file is not a CSV file, If the dependent field is None,
        """

        # Set the dataframe as None and the fields
        self.data: Optional[pd.DataFrame] = None
        self.dependent_field = dependent_field
        self.dependency_field = dependency_field
        self.dependent_version_field = dependent_version_field
        self.dependency_version_field = dependency_version_field
        self.dependent_url_field = dependent_url_field
        self.file_path = file_path

        # Initialize the logger
        super().__init__()

        # Load the data if the file path is setted
        if self.file_path is not None:
            self._load_data()
        else:
            self.logger.debug("File path is None. Data not loaded.")
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
        
        # Mandatory fields
        if self.dependent_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_field} not found on data.")
        
        if self.dependency_field not in self.data.columns:
            raise ValueError(f"Field {self.dependency_field} not found on data.")
        
        # Optional fields
        if self.dependent_version_field is not None and self.dependent_version_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_version_field} not found on data.")
        
        if self.dependency_version_field is not None and self.dependency_version_field not in self.data.columns:
            raise ValueError(f"Field {self.dependency_version_field} not found on data.")
        
        if self.dependent_url_field is not None and self.dependent_url_field not in self.data.columns:
            raise ValueError(f"Field {self.dependent_url_field} not found on data.")
          
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source, sorted alphabetically.

        Returns
        -------
        List[str]
            The list of package names in the data source    

        Examples
        --------
        >>> data_source = CSVDataSource("test.csv", "name", "dependency")
        >>> data_source.obtain_package_names()
        ["package1", "package2", "package3"]    
        """

        # Check if the data is loaded
        if self.data is None:
            raise ValueError("Data is not loaded.")
        
        # Return the list of packages
        return sorted(self.data[self.dependent_field].unique())
    
    def obtain_package_data(self, package_name: str, override_previous: bool = True) -> dict:
        """
        Obtains the package from the dataframe
        
        Parameters
        ----------
        package_name : str
            The name of the package
        override_previous : bool
            If True, it will override the previous data with the same name but different version
        
        Returns
        -------
        dict
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

        # Check if the data is loaded
        if self.data is None:
            raise ValueError("Data is not loaded.")

        # Get the rows of the package
        package_rows = self.data[self.data[self.dependent_field] == package_name]

        # Remove the previous data with the same name but different version
        if override_previous:
            # Get the last row
            last_version = package_rows[self.dependent_version_field].max()
            package_rows = package_rows[package_rows[self.dependent_version_field] == last_version]

        if package_rows.empty:
            self.logger.debug(f"Package {package_name} not found in data.")
            return None
            #raise ValueError(f"Package {package_name} not found in data.")

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
    
    def obtain_packages_data(
        self,
        package_names: List[str],
        progress_bar: Optional[tqdm.tqdm] = None
    ) -> tuple[List[dict], List[str]]:
        '''
        Obtains the data of a list of package names from the CSV file
        If the package name list is None, it will obtain the package names from the CSV file and load their data

        Parameters
        ----------
        package_names : List[str]
            The list of package names to obtain the data from
        progress_bar : tqdm.tqdm
            The progress bar to update

        Returns
        -------
        tuple[List[dict], List[str]]
            The list of packages data and the list of not found packages

        Examples
        --------
        >>> data_source = CSVDataSource("test.csv", "name", "dependency")
        >>> data_source.obtain_packages_data(["package1", "package2"])
        (
            [
                {
                    "name": "package1",
                    "version": "1.0.0",
                    "url": "
                    "dependencies": [ ... ]
                },
                {
                    "name": "package2",
                    "version": "1.0.0",
                    "url": "
                    "dependencies": [ ... ]
                }
            ],
            []
        )
        
        '''
        
        # Define the list of packages and the list of not found packages
        packages = []
        not_found = []

        # Iterate over the package names and obtain the data
        for package_name in package_names:
            try:
                packages.append(self.obtain_package_data(package_name))

            # If the package is not found, add it to the not found list, and continue
            except ValueError:
                self.logger.debug(f"Package {package_name} not found in data.")
                not_found.append(package_name)
                continue
            
            if progress_bar is not None:
                progress_bar.update(1)
                        
        return packages, not_found
