# Module that implements a Dependency object
# Autor: Daniel Alonso Báscones
# Email: dab0012@alu.ubu.es

from sqlalchemy.orm import Session
from modules.db.ORM_Model import Dependency_MySQL, PackageDependency_MySQL

class Dependency:

    # Class constructor
    def __init__(self, name: str = None, type: str = None, version: str = None):

        self.id = None
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
    def save_in_db(self, session: Session, package_id: int):
            
        # If the dependency does not have an id
        if not self.id:

            # Check if the dependency exists in the database
            dependency_db = session.query(Dependency_MySQL).filter(Dependency_MySQL.name == self.name).first()
            
            # If the dependency exists, update the dependency
            if dependency_db:
                self.id = dependency_db.id
                self.update_in_db(session)

            else: 
                # If the dependency does not exist, insert it in the database
                try:
                    d = Dependency_MySQL(name=self.name, version=self.version, type=self.type)
                    session.add(d)
                    session.commit()
                    self.id = session.query(Dependency_MySQL).filter(Dependency_MySQL.name == self.name).first().id
                except Exception as e:
                    print("Exception while inserting dependency in the database: ", e)
                    session.rollback()

            # Check if the dependency is already associated with the package
            package_dependency_db = session.query(PackageDependency_MySQL).filter(PackageDependency_MySQL.package_id == package_id).filter(PackageDependency_MySQL.dependency_id == self.id).first()

            # If the dependency is not associated with the package, insert the relation in the database
            if not package_dependency_db:
                try:
                    p_d = PackageDependency_MySQL(package_id=package_id, dependency_id=self.id)
                    session.add(p_d)
                    session.commit()
                except Exception as e:
                    print("Exception while inserting package-dependency relation in the database: ", e)
                    session.rollback()

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
