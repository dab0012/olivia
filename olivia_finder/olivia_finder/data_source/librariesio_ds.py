from typing import List, Dict, Tuple
import requests

from olivia_finder.utilities.logger import MyLogger
from ..utilities.config_ini import Configuration
from .data_source import DataSource, NotFoundInDataSourceException

class LibrariesioDataSource(DataSource):
    """
    Data source for the Libraries.io API
    """

    API_URL = 'https://libraries.io/api/'
    API_KEY = "DUMMY_KEY"
    
    def __init__(self, name: str, description: str, platform: str, api_key: str = None):
        super().__init__(name, description)
        self.platform = platform

        # define the libraries.io API key
        if api_key is not None:
            self.API_KEY = api_key
        else:
            self.API_KEY = Configuration().get_key('librariesio', 'api_key')


    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.
        """
        raise NotImplementedError
    
    def _build_package_url(self, package_name: str) -> str:
        """
        Builds a URL for the API call to obtain the data of a package.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain the data from

        Returns
        -------
        str
            URL for the API call to obtain the data of a package
        """
        
        return f"{self.API_URL}{self.platform}/{package_name}?api_key={self.API_KEY}"

    def _build_dependencies_url(self, package_name: str) -> str:
        """
        Builds a URL for the API call to obtain the data of a package.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain the data from

        Returns
        -------
        str
            URL for the API call to obtain the data of a package
        """
        
        return f"{self.API_URL}{self.platform}/{package_name}/dependents?api_key={self.API_KEY}"
    
    def obtain_package_data(self, package_name:str) -> Dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain the data from

        Returns
        -------
        Dict
            The data of the package as a dictionary

        Raises
        ------
        NotFoundInDataSourceException
            If the package is not found in the data source

        Example
        -------
        >>> data_source = LibrariesioDataSource('name', 'description', 'platform')
        >>> data_source.obtain_package_data('package_name')
        {'name': 'package_name', 'version': '1.0.0', 'dependencies': ['package1', 'package2'], 'url': 'www.example.com'}
        """

        # Get the package version and url
        MyLogger.log(f"Obtaining data of {package_name}")
        version, url = self._request_package_data(package_name)

        # Get the package dependencies
        try:
            dependencies = self._request_dependencies_data(package_name)
        except LibrariesIoException:
            MyLogger.log(f"Exception while obtaining dependencies of {package_name}")
            MyLogger.log("libraries.io API call failed")
            return {}
            
        return {
            "name": package_name,
            "version": version,
            "dependencies": dependencies,
            "url": url
        }
    

    def _request_package_data(self, package_name: str) -> Tuple[str, str]:
        # sourcery skip: class-extract-method
        '''
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain the data from

        Returns
        -------
        Tuple[str, str]
            The data of the package as a tuple with the version and url
        '''

        # Do the API call for obtain package version and url
        response = requests.get(
            self._build_package_url(package_name), 
            headers={'Accept': 'application/json'},
            timeout=500
        )

        # Check if response is empty
        # Sometime the api returns a response with a message, so we need to check it
        self._check_if_response_ok(response, package_name)

        # Response was successful :) Parse the response
        data = response.json()

        # Check if data is empty
        self._check_if_data_ok(data, package_name)

        # Extract the data
        return data["latest_release_number"], data["package_manager_url"]

    def _request_dependencies_data(self, package_name: str) -> List[Dict]:
        '''
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain the data from

        Returns
        -------
        List[Dict]
            The data of the package as a list of dictionaries
        '''
                
        # Do the API call
        response = requests.get(
            self._build_dependencies_url(package_name), 
            headers={'Accept': 'application/json'},
            timeout=500
        )
        self._check_if_response_ok(response, package_name)
        
        # Response was successful
        # Parse the response
        data = response.json()

        # Check if data is empty
        self._check_if_data_ok(data, package_name)

        # targets the field dependencies in the response
        dependencies = []

        # Process the response
        for package in data:

            dependency_name = package["name"]
            #dependency_url = package["package_manager_url"]
            dependency_version = package["latest_release_number"]

            dependency_data = {
                "name": dependency_name,
                "version": dependency_version,
                #"url": dependency_url
            }

            dependencies.append(dependency_data)

        return dependencies


    def obtain_packages_data(self, package_names: list[str]) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Returns
        -------
        List[Dict]
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
    

    def _check_if_data_ok(self, data, package_name):
        # Check if data is empty
        if data.get('message') is None:
            return 
        
        raise LibrariesIoException(f"Error obtaining package data for {package_name}: {data['message']}")

    def _check_if_response_ok(self, response, package_name):
        # Check if response is empty
        if response.status_code != 200:
            raise NotFoundInDataSourceException(package_name, self.name)
        


class LibrariesIoException(Exception):
    
    def __init__(self, message):
        MyLogger.log(message)

