'''
File:              repo.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:37:07 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

import tqdm
import pandas as pd
from typing import List, Optional
from olivia_finder.data_source import DataSource
from olivia_finder.package import Package

class PackageManager():
    '''
    Class that represents a package manager
    '''

    # Attributes
    data_source: DataSource = None
    packages: List[Package] = []
    NAME: Optional[str] = None
    URL: Optional[str] = None

    def __init__(self, data_source: DataSource, name: str = None, url: str = None):
        '''
        Constructor

        Parameters
        ----------
        data_source : DataSource
            Data source of the package manager

        name : str, optional
            Name of the package manager, by default None

        url : str, optional
            URL of the package manager, by default None
        '''
        self.data_source = data_source
        self.NAME = name
        self.URL = url
        
    def __str__(self) -> str:
        '''
        String representation of the object

        Returns
        -------
        str
            String representation of the object
        '''
        return self.NAME + ":" + self.URL + ":" + self.data_source.get_info()
    
    def __eq__(self, other) -> bool:
        '''
        Equality operator
        
        Parameters
        ----------
        other : Repo
            Other object to compare

        Returns
        -------
        bool
            True if both objects are equal, False otherwise
        '''
        return self.NAME == other.name and self.URL == other.url and self.packages == other.packages
    
    def __hash__(self) -> int:
        '''
        Hash function

        Returns
        -------
        int
            Hash value
        '''
        return hash(self.NAME + self.URL + len(self.packages))
    
    def obtain_package(self, pkg_name: str) -> Package:
        '''
        Scrape a package from a package manager

        Parameters
        ----------
        pkg_name : str
            Name of the package
        scraper : Scraper
            Scraper object

        Returns
        -------
        Package
            Package object
        '''
        return self.data_source.obtain_package(pkg_name)
    
    def obtain_packages(self, pkg_names: List[str], extend_repo = False) -> List[Package]:
        '''
        Scrape a list of packages from a package manager

        Parameters
        ----------
        pkg_names : List[str]
            List of package names
        data_source : DataSource
            Data source of the package manager
        extend_repo : bool, optional
            If True, the packages are added to the repo data structure, by default False

        Returns
        -------
        List[Package]
            List of Package objects
        '''
        progress = tqdm.tqdm(total=len(pkg_names))
        packages = self.data_source.obtain_dependency_network(pkg_names, progress)
        progress.close()

        # Add packages to the repo
        if extend_repo:
            self.packages += packages
            self.packages = list(set(self.packages))

        return packages

    def to_dict(self) -> dict:
        '''
        Convert the object to a dictionary

        Returns
        -------
        dict
            Dictionary representation of the object
        '''
        d = {
            'name': self.NAME,
            'url': self.URL,
            'packages': []
        }
        for package in self.packages:
            d['packages'].append(package.to_dict())
        return d
        
    @classmethod
    def load_dict(cls, data):
        '''
        Load a Repo object from a dictionary

        Parameters
        ----------
        data : dict
            Dictionary representation of the object

        Returns
        -------
        Repo
            Repo object
        '''
        repo = cls(data['name'], data['url'])
        for package in data['packages']:
            repo.packages.append(Package.load(package))
        return repo

    def to_adj_list(self) -> pd.DataFrame:
        '''
        Convert the object to a adjacency list

        Returns
        -------
        pd.DataFrame
            Dependency graph
        '''
        rows = []
        for package in self.packages:
            for dependency in package.dependencies:
                rows.append([package.name, dependency.name])
                
        return pd.DataFrame(rows, columns=['name', 'dependency'])
    
    def to_package_list(self) -> pd.DataFrame:
        '''
        Convert the object to a package graph

        Returns
        -------
        pd.DataFrame
            Package graph
        '''
        rows = []
        for package in self.packages:
            rows.append([package.name, package.version, package.url])
        return pd.DataFrame(rows, columns=['name', 'version', 'url'])
    
    def to_full_adj_list(self) -> pd.DataFrame:
        '''
        Convert the object to a package graph with dependencies and versions

        Returns
        -------
        pd.DataFrame
            Package graph with dependencies and versions
        '''

        rows = []
        for package in self.packages:
            if package.dependencies:
                for dependency in package.dependencies:
                    rows.append([package.name, package.version, package.url, dependency.name, dependency.version])
            else:
                rows.append([package.name, package.version, package.url, None, None])

        return pd.DataFrame(rows, columns=['name', 'version', 'url', 'dependency', 'dependency_version'])
    
    @classmethod
    def load_full_adj_list_csv(cls, path: str):
        '''
        Load a package graph from a csv file

        Parameters
        ----------
        path : str
            Path to the csv file

        '''

        data = pd.read_csv(path, index_col=0)

        # If the csv does not have the structure of to_package_graph_with_dependencies it cannot be loaded
        if not set(['name', 'version', 'url', 'dependency', 'dependency_version']).issubset(data.columns):
            raise PackageManagerLoadError('The csv file does not have the structure of to_package_graph_with_dependencies')
        
        # We create a dictionary with the packages
        packages = {}
        for index, row in data.iterrows():
            if row['name'] not in packages:
                packages[row['name']] = Package(row['name'], row['version'], row['url'])
            else:
                packages[row['name']].version = row['version']
                packages[row['name']].url = row['url']

        # We add the dependencies
        for index, row in data.iterrows():
            if row['dependency'] not in packages:
                packages[row['dependency']] = Package(row['dependency'], row['dependency_version'])
            else:
                packages[row['dependency']].version = row['dependency_version']
            packages[row['name']].dependencies.append(packages[row['dependency']])

        # We create the package manager
        repo = cls('repo_name', 'url')
        repo.packages = list(packages.values())
        return repo
    
class PackageManagerLoadError(Exception):
    """Raised when there is an error loading the package manager"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

