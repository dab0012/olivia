# Module that implements a Dependency object
# Autor: Daniel Alonso Báscones
# Email: dab0012@alu.ubu.es

from sqlalchemy import Session
from Demo.modules.db.ORM_Model import Dependency_MySQL

class Dependency:

    # Class constructor
    def __init__(self):

        self.id = None
        self.name = None
        self.type = None
        self.version = None

    def create(self, name: str, type: str, version: str):

        self.name = name
        self.type = type
        self.version = version

    # String representation of the Dependency class
    def __str__(self):

        if self.version:
            return self.name + " (" + str(self.version) + ")" + " type: " + self.type
        else:
            return self.name + ", type: " + self.type

    # function to get the dependency from the database
    def build_from_db(self, session: Session):

        # If the dependency exists, initialize the dependency
        dependency_db = session.query(Dependency_MySQL).filter(Dependency_MySQL.id == self.id).first()
        if dependency_db:
            self.id = dependency_db.id
            self.name = dependency_db.name
            self.type = dependency_db.type
            self.version = dependency_db.version

    # function to save the dependency in the database
    def save_in_db(self, session: Session):

        # If the dependency does not have an id, insert it in the database
        if not self.id:

            d = Dependency_MySQL(name=self.name, version=self.version, type=self.type)
            session.add(d)
            session.commit()
            self.id = session.query(Dependency_MySQL).filter(Dependency_MySQL.name == self.name).first().id

        # If the dependency has an id, update it in the database
        else:
            self.update_in_db(session)

    # function to update the dependency in the database
    def update_in_db(self, session: Session):

        # Update the dependency in the database
        session.query(Dependency_MySQL).filter(Dependency_MySQL.id == self.id).update(
            {
                Dependency_MySQL.name: self.name,
                Dependency_MySQL.type: self.type,
                Dependency_MySQL.version: self.version
            }
        )
        session.commit()

    # function to print the data of the Dependency class

    def dump(self):
        return f'{self.type}:{self.name}:{self.version}'
