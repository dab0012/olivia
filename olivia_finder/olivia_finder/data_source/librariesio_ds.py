from typing import List, Dict
import requests
from ..utilities.config_ini import Configuration
from .data_source import DataSource

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
        """

        # Do the API call for obtain package version and url
        response = requests.get(
            self._build_package_url(package_name), 
            headers={'Accept': 'application/json'},
            timeout=500
        )

        if response.status_code != 200:
            raise Exception(
                f"Error obtaining package data for {package_name}: {response.status_code} - {response.text}"
            )

        # Response was successful
        # Parse the response
        data = response.json()

        version = data["latest_release_number"]
        url = data["package_manager_url"]

        # Do the API call
        response = requests.get(
            self._build_dependencies_url(package_name), 
            headers={'Accept': 'application/json'},
            timeout=500
        )

        if response.status_code != 200:
            raise Exception(
                f"Error obtaining package data for {package_name}: {response.status_code} - {response.text}"
            )
        
        # Response was successful
        # Parse the response
        data = response.json()

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

        return {
            "name": package_name,
            "version": version,
            "dependencies": dependencies,
            "url": url
        }


    def obtain_packages_data(self) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.
        '''
        # Obtener una lista de nombres de paquetes en la plataforma especificada
        package_names = self.obtain_package_names()
        
        # Obtener información sobre cada paquete
        packages_data = []
        for name in package_names:
            package_info = self.obtain_package_data(name)
            packages_data.append(package_info)
        
        return packages_data