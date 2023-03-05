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
from typing import List
from olivia_finder.package import Package
from olivia_finder.scraping.scraper import Scraper

class Repo:
    '''
    Class that represents a repository
    '''

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.packages = []

    def __str__(self):
        '''
        String representation of the object
        '''
        return self.name + " " + self.url
    
    def __eq__(self, other):
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
        return self.name == other.name and self.url == other.url
    
    def __hash__(self):
        '''
        Hash function

        Returns
        -------
        int
            Hash value
        '''
        return hash(self.name + self.url + len(self.packages))
    
    def obtain_package(self, pkg_name: str, scraper: Scraper) -> Package:
        '''
        Scrape a package from a repository

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
        return scraper.build_obj(pkg_name)
    
    def obtain_packages(self, 
                        pkg_names: List[str], scraper: Scraper, 
                        extend_repo = False) -> List[Package]:
        '''
        Scrape a list of packages from a repository

        Parameters
        ----------
        pkg_names : List[str]
            List of package names
        scraper : Scraper
            Scraper object
        extend_repo : bool, optional
            If True, the packages are added to the repo data structure, by default False

        Returns
        -------
        List[Package]
            List of Package objects
        '''
        progress = tqdm.tqdm(total=len(pkg_names))
        packages = scraper.build_obj_list(pkg_names, progress)
        progress.close()

        # Add packages to the repo
        if extend_repo:
            self.packages += packages

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
            'name': self.name,
            'url': self.url,
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
            raise Exception('CSV file does not have the correct structure')
        
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

        # We create the repository
        repo = cls('repo_name', 'url')
        repo.packages = list(packages.values())
        return repo