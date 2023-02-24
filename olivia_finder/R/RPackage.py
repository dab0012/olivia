# Module that implements an object of type Package
# Autor: Daniel Alonso Báscones
# Email: dab0012@alu.ubu.es

from sqlalchemy.orm import Session
from .ROrmModel import RDependencyMySQL, RPackageMySQL
from .RDependency import RDependency

class RPackage:
    '''
    Class that implements an object of type Package
    '''
 
    def __init__(self, name = None):
        ''' 
        Class constructor
        '''
  
        self.id = None
        self.name = name
        self.description = None
        self.version = None
        self.publication_date = None
        self.mantainer = None
        self.author_data = None
        self.dependencies : list[RDependency] = []
        self.license = None
        self.requires_compilation = None
        self.in_cran = None
        self.in_bioc = None
        self.url = None

    def __str__(self):
        '''
        Makes the object printable

        Returns
        -------
        str
            String representation of the object
        '''
        return self.name + " " + self.version

    def dump(self):
        '''
        Prints a representation of the object in stdout

        Returns
        -------
        None
        '''

        mantainers_str = self.mantainer
        dependencies_str = "\n".join(f"  - {dep}" for dep in self.dependencies)

        package_str = f"""\
Name: {self.name}
Description:
{self.description or "None"}
Version: {self.version or "None"}
Publication date: {self.publication_date or "None"}
Mantainer: {mantainers_str or "None"}
Authors:
{self.author_data or "None"}
Dependencies:
{dependencies_str or "None"}
Requires compilation: {self.requires_compilation or "None"}
In CRAN: {self.in_cran or "None"}
In Bioconductor: {self.in_bioc or "None"}
Licenses:
{self.license or "None"}
Links:
{self.url or "None"}
"""
        print(package_str)

    def build_from_db(self, session: Session) -> bool:
        '''
        Build the object from the information in the database
        
        Parameters
        ----------
        session : Session
            Database session
            
        Returns
        -------
        bool
            True if the package is in the database, False otherwise
        '''

        # Get the package from the database
        package_db = session.query(RPackageMySQL).filter(RPackageMySQL.name == self.name).first()

        # If the package is not in the database, return False
        if package_db is None:
            return False
        
        # If the package is in the database, build the object
        self.id = package_db.id
        self.name = package_db.name
        self.description = package_db.description
        self.version = package_db.version
        self.publication_date = package_db.publication_date
        self.mantainer = package_db.mantainer
        self.author_data = package_db.author_data
        self.requires_compilation = package_db.requires_compilation
        self.in_cran = package_db.in_cran
        self.in_bioc = package_db.in_bioconductor
        self.license = package_db.license
        self.url = package_db.url

        # Get the dependencies from the database
        dependencies_db = session.query(RDependencyMySQL).filter(RDependencyMySQL.id == self.id).all()
        self.dependencies = [RDependency().create(dep.name, dep.type, dep.version) for dep in dependencies_db]    

        return True
    
    def save_in_db(self, session: Session) -> bool:
        '''
        Save the package in the database

        Parameters
        ----------
        session : Session
            Database session

        Returns
        -------
        bool
            True if the package is saved, False otherwise
        '''

        # Check if the package is already in the database, 
        if self.id is not None:
            # Update the package
            self.update_in_db(session)

        else:
            # Create the package in the database
            package = RPackageMySQL()
            package.name = self.name
            package.description = self.description
            package.version = self.version
            package.publication_date = self.publication_date
            package.mantainer = self.mantainer
            package.author_data = self.author_data
            package.requires_compilation = self.requires_compilation
            package.in_cran = self.in_cran
            package.in_bioconductor = self.in_bioc
            package.license = self.license
            package.url = self.url
            session.add(package)
            session.commit()

            # Get the id of the package
            self.id = session.query(RPackageMySQL).filter(RPackageMySQL.name == self.name).first().id

            # Save the dependencies in the database
            for dependency in self.dependencies:
                dependency.save_in_db(session, self.id)      
            
            return True

    def update_in_db(self, session: Session) -> bool:
        '''
        Update the package in the database

        Parameters
        ----------
        session : Session
            Database session

        Returns
        -------
        bool
            True if the package is updated, False otherwise
        '''

        # Check if the package is in the database
        if self.id is None:
            return False

        # Update the package in the database
        package_db = session.query(RPackageMySQL).filter(RPackageMySQL.id == self.id).first()
        package_db.name = self.name
        package_db.description = self.description
        package_db.version = self.version
        package_db.publication_date = self.publication_date
        package_db.mantainer = self.mantainer
        package_db.author_data = self.author_data
        package_db.requires_compilation = self.requires_compilation
        package_db.in_cran = self.in_cran
        package_db.in_bioconductor = self.in_bioc
        package_db.license = self.license
        package_db.url = self.url
        session.commit()

        # Update the dependencies in the database
        for dependency in self.dependencies:
            dependency.update_in_db(session)

        return True