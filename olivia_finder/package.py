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

    def __init__(self, repo: str, name: str, version: str = None, url: str = None, dependencies: list[Package] = None):
        self.repo = repo
        self.name = name
        self.version = version
        self.url = url
        self.dependencies = dependencies

    def print(self):
        print("Package:")
        print("  repo: " + self.repo)
        print("  name: " + self.name)
        print("  version: " + self.version)
        print("  url: " + self.url)
        print("  dependencies:")
        for dependency in self.dependencies:
            print("    " + str(dependency))

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version
    
    def __hash__(self):
        return hash(self.name + self.version)
    
    def __str__(self):
        if self.version == "" or self.version is None:
            self.version = "*"
        return self.repo + ":" + self.name + ":" + self.version

    def update(self, data):
        if 'version' in data:
            self.version = data['version']
        if 'url' in data:
            self.url = data['url']
        if 'dependencies' in data:
            self.dependencies = data['dependencies']
    
    def store_in_db(self, db):
        pass
        
    @classmethod
    def load(cls, data):
        package = cls(data['name'], data['version'], data['author'], data['url'], data['dependencies'])
        return package

    def to_dict(self):
        return {
            'repo': self.repo,
            'name': self.name,
            'version': self.version,
            'url': self.url,
            'dependencies': self.dependencies
        }
    

