from typing import Dict, List
from .data_source_abc import DataSourceABC

class DataSource(DataSourceABC):
    """
    Base class for data sources, it implements the DataSourceABC interface.
    This class is not intended to be used directly, but to be inherited by
    other classes that must override this class's methods.
    """

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.packages_data: dict = {}

    def get_info(self) -> Dict:
        '''
        Returns the datasource information data.

        Returns
        -------
        dict
            The information of the data source
        
        Example
        -------
        >>> data_source = DataSource('name', 'description')
        >>> data_source.get_info()
        {'name': 'name', 'description': 'description'}
        '''
        return {
            'name': self.name,
            'description': self.description
        }

    def obtain_package_names(self) -> List[str]:
        """
        Obtains the list of packages from the data source.
        Is an optional method, if the data source does not implement it, it will
        be considered that it does not have a list of packages available.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError
    
    def obtain_package_data(self) -> Dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError
    
    def obtain_packages_data(self) -> List[Dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        '''
        raise NotImplementedError
    