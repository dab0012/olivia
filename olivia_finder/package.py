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

class Package:
    '''
    Class that represents a package
    '''

    def __init__(self, name: str, version: str = None, url: str = None, dependencies: list[Package] = None):
        '''
        Constructor

        Parameters
        ----------
        name : str
            Name of the package
        version : str, optional
            Version of the package, by default None
        url : str, optional
            URL of the package, by default None
        dependencies : list[Package], optional
            List of dependencies, by default None
        '''

        self.name = name
        self.version = version
        self.url = url
        self.dependencies = dependencies

    def print(self) -> None:
        '''
        Print the package data

        Returns
        -------
        None
        '''
        print("Package:")
        print("  repo: " + self.repo)
        print("  name: " + self.name)
        print("  version: " + self.version)
        print("  url: " + self.url)
        print("  dependencies:")
        for dependency in self.dependencies:
            print("    " + str(dependency))

    def __eq__(self, other) -> bool:
        '''
        Compare two packages
        
        Parameters
        ----------
        other : Package
            Package to compare
            
        Returns
        -------
        bool
            True if the packages are equal, False otherwise
        '''
        return self.name == other.name and self.version == other.version
    
    def __hash__(self) -> int:
        '''
        Hash function

        Returns
        -------
        int
            Hash of the package
        '''
        return hash(self.name + self.version)
    
    def __str__(self) -> str:
        '''
        String representation of the package

        Returns
        -------
        str
            String representation of the package
        '''
        if self.version == "" or self.version is None:
            self.version = "*"
        return self.repo + ":" + self.name + ":" + self.version

    def update(self, data) -> None:
        '''
        Update the package with the data

        Parameters
        ----------
        data : dict
            Dictionary with the data
        '''

        if 'version' in data:
            self.version = data['version']
        if 'url' in data:
            self.url = data['url']
        if 'dependencies' in data:
            self.dependencies = data['dependencies']
            
    @classmethod
    def load(cls, data):
        '''
        Load a package from a dictionary

        Parameters
        ----------
        data : dict
            Dictionary with the data

        Returns
        -------
        Package
            Package loaded from the dictionary
        '''

        package = cls(data['name'], data['version'], data['url'], data['dependencies'])
        return package

    def to_dict(self):
        '''
        Convert the package to a dictionary

        Returns
        -------
        dict
            Dictionary with the data
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
    

