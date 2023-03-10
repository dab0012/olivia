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
    def __init__(self, name:str = None, description:str = None):
        """Constructor method.

        :param name: name of the data source, defaults to None
        :type name: str, optional
        :param description: _description_, defaults to None
        :type description: str, optional
        """
        super.__init__(name, description)

    def load_data(self, file_path:str) -> None:
        """Loads the data from a CSV file.

        :param file_path: the path of the file to load, defaults to None
        :type file_path: str, optional
        :raises ValueError: when file path is None
        :raises FileNotFoundError: when file is not found
        :raises ValueError: when file is not a CSV file
        """

        if file_path is None:
            raise ValueError("File path cannot be None.")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")
        
        if not file_path.endswith(".csv"):
            raise ValueError(f"File {file_path} is not a CSV file.")
        
        self.data = pd.read_csv(file_path)

    @override
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.

        :return: list of package names
        """
        
        pass

    def obtain_package_data(self, package_name: str) -> Package:
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
        return Package(
            package_name, 
            row['version'].values[0], 
            row['description'].values[0], 
            row['url'].values[0], 
            row['license'].values[0], 
            row['dependencies'].values[0]
        )
   
    @abstractmethod
    def obtain_packages_data(self, pckg_names: List[str] = None, progress = None) -> List[Package]:
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