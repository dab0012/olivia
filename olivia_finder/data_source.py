from abc import ABC, abstractmethod
import os, pickle
from typing import List
from olivia_finder.package import Package


class DataSource(ABC):
    """
    Interface class for data sources.
    """
    # Attributes
    # ---------------------
    name = None
    description = None
    PERSISTENCE_PATH = None

    # Methods
    # ---------------------
    def __init__(self, name = None, description = None):
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the data source.
        description : str
            Description of the data source.
        """
        # If name is not defined, use the class name
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

        # if description is not defined, use the default one else use the one defined
        if description is None:
            self.description = "No description available."
        else:
            self.description = description
        
    def load_data(self, persistence_path = None) -> dict:
        """
        Loads the data from the persistence directory.
        It loads the latest data file.

        Parameters
        ----------
        persistence_path : str
            Path to the persistence directory.

        Returns
        -------
        dict
            Dictionary with the data. The keys are the names of the data sources and the values are the data.
            keys : ['package_list', 'dependency_graph', 'info']
        """

        # If persistence_path is not defined, use the default one
        if persistence_path is None:
            persistence_path = self.PERSISTENCE_PATH

        # If persistence_path is still not defined, raise an error
        if persistence_path is None:
            raise ValueError("persistence_path is not defined.")
        
        # Get the latest data file
        files = os.listdir(persistence_path)

        # Filter the files by the name of the data source and sort them by timestamp
        files = [f for f in files if f.startswith(self.name)]
        files.sort()

        # Get the latest file
        latest_file = files[-1]
        filepath = os.path.join(persistence_path, latest_file)

        # Load the data from ods (olivia data source) file format and unpickle it
        # its a pickle file with the package name list as a csv and the package graph as a csv an a csv file with info about the data source
        pickled_data = pickle.load(open(filepath, "rb"))

        # return the data as a dictionary
        return pickled_data
        
    def get_info(self) -> str:
        """
        Returns information about the data source.
        """
        return f"{self.name}: {self.description}, last updated on {self.last_update}"

    # Abstract methods to be implemented in subclasses
    # ------------------------------------------------

    @abstractmethod
    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.

        Returns
        -------
        List[str]
            List of package names.
        """
        pass

    @abstractmethod
    def obtain_package(self, package_name: str) -> Package:
        """
        Obtains the package from the data source given its name.
        To be implemented in subclasses.

        Parameters
        ----------
        package_name : str
            Name of the package.

        Returns
        -------
        Package
            Package object.
        """
        pass
    
    @abstractmethod
    def obtain_dependency_network(self, pckg_names: List[str]) -> List[Package]:
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