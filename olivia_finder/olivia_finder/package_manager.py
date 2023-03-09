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
from .data_source import DataSource
from .package import Package

class PackageManager():
    '''
    Class that represents a package manager
    '''

    # Attributes
    data_source: DataSource
    packages: set[Package]

    def __init__(self, data_source: DataSource):
        '''
        Constructor

        Parameters
        ----------
        data_source : DataSource
            Data source of the package manager
        '''
        if data_source is None:
            raise ValueError("Data source cannot be None")
        
        self.data_source = data_source
        self.packages = set()
    
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

        pkg_data = self.data_source.obtain_package_data(pkg_name)
        if pkg_data is None:
            return None
        else:
            return Package.load(pkg_data)
    
    def obtain_packages(self, pkg_names: Optional[List[str]] = None, extend_repo = False, show_progress: bool = False) -> List[Package]:
        '''
        Scrape a list of packages from a package manager

        ---
        Parameters
        -   pkg_names: List[str]   -> List of package names to get from data source
        -   extend_repo: bool      -> If True, the packages are added to the package manager package list
        -   show_progress: bool    -> If True, a progress bar is shown

        ---
        Returns
        -   List[Package]          -> List of packages

        '''

        # Obtain the packages if the list is empty
        if pkg_names is None or len(pkg_names) == 0:
            pkg_names = self.data_source.obtain_package_names()

        if show_progress:
            progress_bar = tqdm.tqdm(total=len(pkg_names))
        else:
            progress_bar = None

        # Obtain the packages
        package_list = []
        packages_data = self.data_source.obtain_packages_data(pkg_names, progress_bar=progress_bar)
        for pkg_data in packages_data:
            if pkg_data is not None:
                package_list.append(Package.load(pkg_data))

        if progress_bar is not None:
            progress_bar.close()

        # Add packages to the repo
        if extend_repo:
            self.packages.update(package_list)

        return package_list

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
        for row in data.iterrows()[1]:
            if row['name'] not in packages:
                packages[row['name']] = Package(row['name'], row['version'], row['url'])
            else:
                packages[row['name']].version = row['version']
                packages[row['name']].url = row['url']

        # We add the dependencies
        for row in data.iterrows()[1]:
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

