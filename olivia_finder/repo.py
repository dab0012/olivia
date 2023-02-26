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
from olivia_finder.scrape.scraper import Scraper

class Repo:
    '''
    Class that represents a repository
    '''

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.packages = []

    def scrape_package(self, pkg_name: str, scraper: Scraper) -> Package:
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
        return scraper.build(pkg_name)
    
    def scrape_packages(self, pkg_names: List[str], scraper: Scraper) -> List[Package]:
        '''
        Scrape a list of packages from a repository

        Parameters
        ----------
        pkg_names : List[str]
            List of package names
        scraper : Scraper
            Scraper object

        Returns
        -------
        List[Package]
            List of Package objects
        '''

        progress = tqdm.tqdm(total=len(pkg_names))
        for pkg_name in pkg_names:
            pkg = self.scrape_package(pkg_name, scraper)
            if pkg:
                self.packages.append(pkg)
            progress.update(1)
        progress.close()
        return self.packages
    
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
        '''
        return hash(self.name + self.url)
    
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

    def to_csv(self, path: str):
        '''
        Save the object to a CSV file

        Parameters
        ----------
        path : str
            Path to the CSV file
        '''
        df = pd.DataFrame([self.to_dict()])
        df.to_csv(path, index=False)
        
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

    @classmethod
    def load_csv(cls, path: str):
        '''
        Load a Repo object from a CSV file

        Parameters
        ----------
        path : str
            Path to the CSV file

        Returns
        -------
        Repo
            Repo object
        '''
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            return None
        
        return cls.load_dict(df.to_dict('records')[0])

    
        


