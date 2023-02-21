# Module that implements the database data model using SQLAlchemy
# Autor: Daniel Alonso Báscones
# Email: dab0012@alu.ubu.es

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Base class for the model
Base = declarative_base()

class Package_MySQL(Base):
    '''
    Table that stores the packages

    Attributes
    ----------
    id : int
        Id of the package
    name : str
        Name of the package
    description : str
        Description of the package
    version : str
        Version of the package
    publication_date : date
        Publication date of the package
    requires_compilation : bool
        True if the package requires compilation
    in_cran : bool
        True if the package is in CRAN
    in_bioconductor : bool
        True if the package is in Bioconductor
    mantainer : str
        Mantainer of the package
    author_data : str
        Authors of the package
    license : str
        License of the package
    url : str
        Url of the package

    '''

    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String(255), nullable=True)
    publication_date = Column(Date, nullable=True)
    requires_compilation = Column(Boolean, nullable=True)
    in_cran = Column(Boolean)
    in_bioconductor = Column(Boolean)
    mantainer = Column(String(255), nullable=True)
    author_data = Column(Text)
    license = Column(String(255), nullable=True)
    url = Column(String(255), nullable=False)
    dependencies = relationship('Dependency_MySQL', secondary='package_dependency')

class Dependency_MySQL(Base):
    '''
    Table that stores the dependencies of the packages

    Attributes
    ----------
    id : int
        Id of the dependency
    name : str
        Name of the dependency
    version : str
        Version of the dependency
    type : str
        Type of the dependency
    '''
    __tablename__ = 'dependencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=True)
    type = Column(String(255), nullable=False)


class PackageDependency_MySQL(Base):
    '''
    Association table between packages and dependencies

    Attributes
    ----------
    package_id : int
        Id of the package
    dependency_id : int
        Id of the dependency
    '''
    __tablename__ = 'package_dependency'
    package_id = Column(Integer, ForeignKey('packages.id'), primary_key=True)
    dependency_id = Column(Integer, ForeignKey(
        'dependencies.id'), primary_key=True)
