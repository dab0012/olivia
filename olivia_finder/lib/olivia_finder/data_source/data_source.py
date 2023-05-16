
from __future__ import annotations
from abc import ABC, abstractmethod

class DataSource(ABC):
    '''
    Base class for data sources.

    .. warning:: 
    
        This class is an abstract class, so it can't be instantiated.

    The subclasses must implement the methods:
    - `DataSource.obtain_package_names`
    - `DataSource.obtain_package_data`
    - `DataSource.obtain_packages_data`


    .. note::

        The `name` and `description` parameters are mandatory, and must be passed as arguments.
        The use of this parameters is to be able to identify the data source, and to be able to show a description of it.
    '''

    def __init__(self, name: str, description: str):
        '''
        Constructor of the DataSource class.

        Parameters
        ----------

        name : str
            The name of the data source
        description : str
            The description of the data source
        '''

            
        self.name: str = name
        self.description: str = description

    def get_info(self) -> dict:
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


    # Abstract methods
    # ----------------

    # Implement the methods obtain_package_names, obtain_package_data and obtain_packages_data in the subclasses

    @abstractmethod
    def obtain_package_names(self) -> list[str]:
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

    @abstractmethod
    def obtain_package_data(self, package_name:str) -> dict:
        """
        Obtains the data of a package from the data source as a dictionary.

        Parameters
        ----------
        package_name : str
            The name of the package to obtain the data

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        """
        raise NotImplementedError

    @abstractmethod
    def obtain_packages_data(self, package_names: list[str]) -> list[dict]:
        '''
        Obtains the data of a list of package names from the data source.

        Raises
        ------
        NotImplementedError
            Because this method is not implemented in the base class
        '''
        raise NotImplementedError

class NotFoundInDataSourceException(Exception):
    """
    Exception that is raised when a package is not found in a data source.
    """
    
    def __init__(self, package_name: str, data_source_name: str):
        self.package_name = package_name
        self.data_source_name = data_source_name

    def __str__(self):
        return f'The package {self.package_name} was not found in the data source {self.data_source_name}'
    
    
