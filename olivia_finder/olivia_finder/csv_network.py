import os, pandas as pd
from abc import abstractmethod
from typing import List
from typing_extensions import override
from .data_source import DataSource
from .package import Package

class CSVNetwork(DataSource):
    """
    Interface class for data sources.
    """
    # Attributes
    # ---------------------
    name: str
    description: str
    PERSISTENCE_PATH: str
    data: pd.DataFrame

    # Methods
    # ---------------------
    def __init__(self, name = None, description = None):
        """
        Constructor

        ---
        Parameters
        -   name: str -> Name of the data source.
        -   description: str -> Description of the data source.
        """
        super.__init__(name, description)

    def load_data(self, file_path = None) -> None:
        """
        Loads the data from csv file.

        ---
        Parameters
        -  file_path : str (Path to the file to load)

        Returns
        -   None
        """

        # If file_path is not defined, use the default one
        if file_path is None:
            raise ValueError("persistence_path is not defined.")
        
        # Read file as a pandas dataframe if it exists
        if os.path.exists(file_path):
            self.data = pd.read_csv(file_path)
        else:
            raise FileNotFoundError(f"File {file_path} not found.")

        # If persistence_path is still not defined, raise an error
        if file_path is None:
            raise ValueError("persistence_path is not defined.")

    @override
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.

        ---
        Returns
        -   List[str] -> List of package names.
        """
        pass

    def obtain_package(self, package_name: str) -> Package:
        """
        Obtains the package from the dataframe.

        ---
        Parameters
        -   package_name: str -> Name of the package to obtain.

        Returns
        -   Package -> Package object.
        """

        # Get the row of the package
        row = self.data.loc[self.data['package_name'] == package_name]

        # If the row is empty, raise an error
        if row.empty:
            raise ValueError(f"Package {package_name} not found.")

        # Create the package object
        package = Package(package_name, row['version'].values[0], row['description'].values[0], row['url'].values[0], row['license'].values[0], row['dependencies'].values[0])

        return package

    
    @abstractmethod
    def obtain_dependency_network(self, pckg_names: List[str] = None, progress = None) -> List[Package]:
        '''
        Build a list of Package objects from a list of package names to be
        used as a dependency network

        Parameters
        ----------
        pckg_names : List[str]
            List of package names

        Returns
        -------
        list
            List of Package objects
        '''
        pass