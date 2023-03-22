from abc import ABC, abstractmethod

class DataSourceABC(ABC):
    """
    Interface class for data sources.
    """

    @abstractmethod
    def get_info(self) -> dict:
        '''
        Returns the information of the data source.

        Returns
        -------
        dict
            The information of the data source
        '''

    @abstractmethod
    def obtain_package_names(self) -> list:
        """
        Obtains the list of packages from the data source.
        Is an optional method, if the data source does not implement it, it will
        be considered that it does not have a list of packages available.

        Returns
        -------
        list
            The list of packages from the data source
        """

    @abstractmethod
    def obtain_package_data(self) -> dict:
        """
        Obtains the data of a package from the data source as a dictionary.
        
        Returns
        -------
        dict
            The data of a package from the data source as a dictionary
        """
    
    @abstractmethod
    def obtain_packages_data(self) -> list:
        '''
        Obtains the data of a list of package names from the data source.
        
        Returns
        -------
        list
            The data of a list of package names from the data source
        '''
    