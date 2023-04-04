from typing import List, Dict
from pybraries import Search
from .data_source import DataSource

class LibrariesioDataSource(DataSource):
    
    def __init__(self, name: str, description: str, platform: str, api_key: str):
        super().__init__(name, description)
        self.platform = platform
        self.lib = Search(api_key)

    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.
        """
        # Buscar proyectos en la plataforma especificada
        projects = self.lib.project_search(keywords='', platforms=self.platform)

        # Devolver una lista de nombres de proyectos
        return [project['name'] for project in projects]

    def obtain_package_data(self, package_name:str) -> Dict:
        """
        Obtains the data of a package from the data source as a dictionary.
        """
        # Obtener información sobre el paquete especificado en la plataforma especificada
        package_info = self.lib.project(self.platform, package_name)
        
        return package_info

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