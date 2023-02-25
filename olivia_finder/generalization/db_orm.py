'''
File:              db_orm.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 6:53:50 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define the base class for the ORM
Base = declarative_base()

# Define the ORM classes
class RepoMySQL(Base):
    __tablename__ = 'repo'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    packages = relationship("PackageMySQL", back_populates="repo")

class PackageMySQL(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(String)
    url = Column(String)
    repo_id = Column(Integer, ForeignKey('repo.id'))
    repo = relationship("RepoMySQL", back_populates="packages")
    dependencies = relationship("DependencyMySQL", back_populates="package")

class DependencyMySQL(Base):
    __tablename__ = 'dependency'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    package_id = Column(Integer, ForeignKey('package.id'))
    package = relationship("PackageMySQL", back_populates="dependencies")