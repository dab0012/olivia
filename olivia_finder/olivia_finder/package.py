'''
File:              package.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:23:06 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from __future__ import annotations
from typing import Optional

class Package:
    '''
    Class that represents a package in the network
    
    Attributes
    ----------
    name : str
        Name of the package
    version : Optional[str]
        Version of the package
    url : Optional[str]
        URL of the package
    dependencies : Optional[list[Package]]
        List of dependencies of the package
        
    Examples
    --------
    >>> from olivia_finder.package import Package
    >>> package = Package("numpy", "1.0.0", "https://numpy.org")
    >>> package.print()
    '''
    
    # Class Attributes
    # ---------------------
    name: str
    version: Optional[str]
    url: Optional[str]
    dependencies: Optional[list[Package]]
    
    def __init__(
        self, 
        name: str, 
        version: Optional[str] = None, 
        url: Optional[str] = None, 
        dependencies: Optional[list[Package]] = None
    ):
        '''Constructor'''

        self.dependencies = [] if dependencies is None else dependencies
        self.name = name
        self.version = version
        self.url = url

    def print(self):
        '''
        Print the package data in the console
        
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.print()
        '''
        print("Package:")
        print(f"  name: {self.name}")
        print(f"  version: {self.version}")
        print(f"  url: {self.url}")
        print("  dependencies:")
        for dependency in self.dependencies:
            print(f"    {str(dependency)}")

    def __eq__(self, other) -> bool:
        '''
        Compare two packages for equality
        
        Parameters
        ----------
        other : Package
            Package to compare with
        
        Returns
        -------
        bool
            True if the packages are equal, False otherwise
            
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package1 = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package2 = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package1 == package2
            True    
        '''
        return self.name == other.name and self.version == other.version
    
    def __hash__(self) -> int:
        '''
        Hash code of the package
        
        Returns
        -------
        int
            Hash code of the package
        
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> hash(package)
        '''
        return hash(self.name + self.version)
    
    def __str__(self) -> str:
        '''
        String representation of the package

        Returns
        -------
        str
            String representation of the package
            
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> str(package)
        '''
        return self.name if self.version is None else f"{self.name}:{self.version}"

    def update(self, data: dict):
        '''
        Update the package with the data of a dictionary.
        Only the attributes version, url and dependencies are supported.

        Parameters
        ----------
        data : dict
            Dictionary with the data to update
            
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.update({"version": "1.0.1"})
        '''

        if 'version' in data:
            self.version = data['version']
        if 'url' in data:
            self.url = data['url']
        if 'dependencies' in data:
            self.dependencies = set(data['dependencies'])
            
    @classmethod
    def load(cls, data: dict):
        '''
        Loads a package from a dictionary
        It is assumed that the dictionary has the following structure:
        {   
            'name': str,
            'version': str,
            'url': str,
            'dependencies': list[dict]
        }

        Parameters
        ----------
        data : dict
            Dictionary with the data

        Returns
        -------
        Package
            Package loaded from the dictionary
            
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package.load({"name": "numpy", "version": "1.0.0", "url": "https://numpy.org"})
        '''

        # Create the packages of the dependencies
        dependencies = []
        for dependency in data['dependencies']:
            p = Package(dependency['name'], dependency['version'])
            dependencies.append(p)

        return cls(data['name'], data['version'], data['url'], dependencies)

    def to_dict(self):
        '''
        Convert the package to a dictionary with the following structure:
        {
            'name': str,
            'version': str,
            'url': str,
            'dependencies': list[dict]
        }
        
        Returns
        -------
        dict
            Dictionary with the data of the package
            
        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.to_dict()
        '''

        # Create the dictionary
        data = {
            'name': self.name,
            'version': self.version,
            'url': self.url,
            'dependencies': []
        }

        # Add the dependencies as a dictionary
        for dependency in self.dependencies:
            data['dependencies'].append(dependency.to_dict())

        return data
    

