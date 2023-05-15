from typing import Union
from ..utilities.exception import OliviaFinderException
from ..utilities.logger import MyLogger
from ..utilities.config import Configuration
from .data_source import DataSource
import sys

# Load the Libraries.io API key before importing the librariesio package
# -----------------------------------------------------------------------

# try to load the API key from the configuration file
API_KEY = Configuration().get_key('librariesio', 'api_key')
if API_KEY is None:
    MyLogger().get_logger().error("API key for Libraries.io not found")
    raise OliviaFinderException("API key for Libraries.io not found")

# Set as environment variable
import os
os.environ["LIBRARIES_API_KEY"] = API_KEY
from pybraries.search import Search

class LibrariesioDataSource(DataSource):
    """
    Data source for the Libraries.io API

    Attributes
    ----------
    name : str
        Name of the data source
    description : str
        Description of the data source
    platform : str
        Platform of the data source to search for packages
    search : Search
        Search object to search for packages in the data source
    """
    
    def __init__(self, name: str, description: str, platform: str):
        """
        Constructor of the class

        Parameters
        ----------
        name : str
            Name of the data source
        description : str
            Description of the data source
        platform : str
            Platform of the data source to search for packages

        Raises
        ------
        LibrariesIoException
            If the search object cannot be created
        """

        super().__init__(name, description)
        self.platform = platform

        # Create the search object
        try:
            self.search = Search()
        except LibrariesIoException("Error creating the search object"):
            pass


    def obtain_package_names(self) -> list[str]:
        """
        Obtains the list of packages from the data source.
        """
        raise NotImplementedError
    
    def obtain_package_data(self, package_name:str) -> Union[dict, None]:
        """
        Obtains the data of a package from the data source.

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        dict
            Dictionary with the package data
        None
            If the package is not found
            
        Example
        -------
        >>> data_source = LibrariesioDataSource('name', 'description', 'platform')
        >>> data_source.obtain_package_data('package_name')
        {'name': 'package_name', 'version': '1.0.0', 'dependencies': ['package1', 'package2'], 'url': 'www.example.com'}
        """

        # Get the package version and url
        MyLogger().get_logger().debug(f"Obtaining data of {package_name}")

        # Redirect the output to /dev/null to avoid printing the output of the search (pybraries bug)
        stdout = sys.stdout     # Keep the standard output backed up
        sys.stdout = open('/dev/null', 'w')

        try:
            dependencies_data = self.search.project_dependencies(
                platforms=self.platform, project=package_name
            )

            # Check if data is empty
            if dependencies_data is None:
                MyLogger().get_logger().debug(f"Package {package_name} not found")
                return None

        except LibrariesIoException(f"Exception while obtaining {package_name} dependencies"):
            return None
        
        finally:
            # Restore the original standard output
            sys.stdout.close()
            sys.stdout = stdout 
        
        version = dependencies_data["dependencies_for_version"]
        url = dependencies_data["package_manager_url"]

        
        # Obtain the dependencies (dependencies field, project_name)
        # Obtain the dependency version (atest_stable field)
        dependencies = []

        for dependency in dependencies_data["dependencies"]:
            dependency_name = dependency["project_name"]
            dependency_version = dependency["latest_stable"]

            dependency_data = {
                "name": dependency_name,
                "version": dependency_version,
            }

            dependencies.append(dependency_data)

        return {
            "name": package_name,
            "version": version,
            "dependencies": dependencies,
            "url": url
        }
        
    def obtain_packages_data(self, package_names: list[str]) -> list[dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Returns
        -------
        list[dict]
            The data of the packages as a list of dictionaries

        Example
        -------
        >>> data_source = LibrariesioDataSource('name', 'description', 'platform')
        >>> data_source.obtain_packages_data(['package1', 'package2'])
        [{'name': 'package1', 'version': '1.0.0', 'dependencies': ['package1', 'package2'], 'url': 'www.example.com'}, 
        {'name': 'package2', 'version': '1.0.0', 'dependencies': ['package1', 'package2'], 'url': 'www.example.com'}]
        '''

        packages_data = []

        for package_name in package_names:
            if package_data := self.obtain_package_data(package_name):
                packages_data.append(package_data)

        return packages_data

class LibrariesIoException(OliviaFinderException):
    """
    Exception for the LibrariesioDataSource class
    """

