from typing import List, Union
from ..utilities.exception import OliviaFinderException
from ..utilities.logger import MyLogger
from ..utilities.config import Configuration
from .data_source import DataSource
import sys
import time


# Load the Libraries.io API key before importing the librariesio package
# -----------------------------------------------------------------------

# try to load the API key from the configuration file
API_KEY = Configuration().get_key('librariesio', 'api_key')
if API_KEY is None:
    raise OliviaFinderException("API key for Libraries.io not found")

# Set as environment variable
import os
os.environ["LIBRARIES_API_KEY"] = API_KEY
from pybraries.search import Search

class LibrariesioDataSource(DataSource):
    """
    Data source for the Libraries.io API

    .. warning::

        - The API key must be set as an environment variable with the name `LIBRARIES_API_KEY`
        - The class will raise an exception if the API key is not found
        - The API key can be set in the configuration file
        - The API key can be obtained from the user's profile in Libraries.io

    """

    DEFAULT_DESCRIPTION = "Libraries.io data source"
    
    def __init__(self, platform: str):
        """
        Constructor of the class

        Parameters
        ----------
        platform : str
            Platform of the data source to search for packages

        Raises
        ------
        LibrariesIoException
            If the search object cannot be created
        """

        self.platform = platform
        logger_name = Configuration().get_key('logger', 'librariesio_name')
        self.logger = MyLogger.get_logger(
            logger_name=logger_name,
            level=Configuration().get_key('logger', 'global_level'),
            enable_console=Configuration().get_key('logger', 'librariesio_console'),
            console_level=Configuration().get_key('logger', 'librariesio_console_level'),
            filename=f"{Configuration().get_key('folders', 'logger')}/{Configuration().get_key('logger', 'librariesio_filename')}",
            file_level=Configuration().get_key('logger', 'librariesio_file_level')
        )

        if Configuration().get_key('logger', 'librariesio_status').lower() == 'disabled':
            MyLogger.disable_console(logger_name) 
            MyLogger.disable_file(logger_name)

        # Create the search object
        try:
            self.search = Search()
        except Exception as e:
            pass

    def obtain_package_names(self) -> List[str]:
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
        self.logger.debug(f"Obtaining data of {package_name}")

        # Redirect the output to /dev/null to avoid printing the output of the search (pybraries bug)
        stdout = sys.stdout     # Keep the standard output backed up
        sys.stdout = open('/dev/null', 'w')

        try:
            dependencies_data = self.search.project_dependencies(
                platforms=self.platform, project=package_name
            )

            # Check if data is empty
            if dependencies_data is None:

                # Sleep for 3 second to avoid the API rate limit
                self.logger.debug(f"Package {package_name} not found. Sleeping for 4 seconds for the API rate limit")
                time.sleep(4)

            # Try again
            dependencies_data = self.search.project_dependencies(
                platforms=self.platform, project=package_name
            )

            # Check if data is empty
            if dependencies_data is None:

                self.logger.debug(f"Package {package_name} not found")
                return None
            else:
                self.logger.debug(f"Package {package_name} found")

        except Exception as e:
            self.logger.error(f"Exception while obtaining {package_name} dependencies")
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
        
    def obtain_packages_data(self, package_names: List[str]) -> List[dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Returns
        -------
        List[dict]
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

