# Module that implements the database data model using SQLAlchemy
# Autor: Daniel Alonso Báscones 
# Email: dab0012@alu.ubu.es

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Package_MySQL(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    requires_compilation = Column(Boolean, nullable=False)
    in_cran = Column(Boolean)
    in_bioconductor = Column(Boolean)
    mantainer = Column(String(255), nullable=False)
    author_data = Column(Text)
    license = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    dependencies = relationship('Dependency_MySQL', secondary='package_dependency')

class Dependency_MySQL(Base):
    __tablename__ = 'dependencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    version = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

class PackageDependency_MySQL(Base):
    __tablename__ = 'package_dependency'
    package_id = Column(Integer, ForeignKey('packages.id'), primary_key=True)
    dependency_id = Column(Integer, ForeignKey('dependencies.id'), primary_key=True)