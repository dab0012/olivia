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
from package import Package
from scraper import Scraper
import pandas as pd
from typing import List

class Repo:

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.packages = []

    def scrape_package(self, pkg_name: str, scraper: Scraper) -> Package:
        return scraper.build(pkg_name)
    
    def scrape_packages(self, pkg_names: List[str], scraper: Scraper) -> List[Package]:

        progress = tqdm.tqdm(total=len(pkg_names))
        for pkg_name in pkg_names:
            pkg = self.scrape_package(pkg_name, scraper)
            if pkg:
                self.packages.append(pkg)
            progress.update(1)
        progress.close()
        return self.packages
    
    def __str__(self):
        return self.name + " " + self.url
    
    def __eq__(self, other):
        return self.name == other.name and self.url == other.url
    
    def __hash__(self):
        return hash(self.name + self.url)
    
    def to_dict(self):
        d = {
            'name': self.name,
            'url': self.url,
            'packages': []
        }
        for package in self.packages:
            d['packages'].append(package.to_dict())
        return d

    def to_csv(self, path: str):
        df = pd.DataFrame([self.to_dict()])
        df.to_csv(path, index=False)
        
    @classmethod
    def load(cls, data):
        repo = cls(data['name'], data['url'])
        for package in data['packages']:
            repo.packages.append(Package.load(package))
        return repo




    
        


