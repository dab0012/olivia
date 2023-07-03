"""

Define the data structure of a package



```python
from olivia_finder.package import Package


package = Package(
        "AER", "3.1.1", "https://cran.r-project.org/web/packages/AER/index.html", 
        [
                Package("car", "3.0-10", "https://cran.r-project.org/web/packages/car/index.html", []),
                Package("effects", "4.2-0","https://cran.r-project.org/web/packages/effects/index.html", []),
                Package("foreign", "0.8-80", "https://cran.r-project.org/web/packages/foreign/index.html", []),
        ]
)

package.print()
```

    Package:
      name: AER
      version: 3.1.1
      url: https://cran.r-project.org/web/packages/AER/index.html
      dependencies:
        car:3.0-10
        effects:4.2-0
        foreign:0.8-80



```python
package.to_dict()
```

    {'name': 'AER',
     'version': '3.1.1',
     'url': 'https://cran.r-project.org/web/packages/AER/index.html',
     'dependencies': [{'name': 'car',
       'version': '3.0-10',
       'url': 'https://cran.r-project.org/web/packages/car/index.html',
       'dependencies': []},
      {'name': 'effects',
       'version': '4.2-0',
       'url': 'https://cran.r-project.org/web/packages/effects/index.html',
       'dependencies': []},
      {'name': 'foreign',
       'version': '0.8-80',
       'url': 'https://cran.r-project.org/web/packages/foreign/index.html',
       'dependencies': []}]}




```python
package.load(
    {
        "name": "AER",
        "version": "3.1.1",
        "url": "https://cran.r-project.org/web/packages/AER/index.html",
        "dependencies": [
            {
                "name": "car",
                "version": "3.0-10",
                "url": "https://cran.r-project.org/web/packages/car/index.html",
                "dependencies": []
            },
            {
                "name": "effects",
                "version": "4.2-0",
                "url": "https://cran.r-project.org/web/packages/effects/index.html",
                "dependencies": []
            },
            {
                "name": "foreign",
                "version": "0.8-80",
                "url": "https://cran.r-project.org/web/packages/foreign/index.html",
                "dependencies": []
            }
        ]
    }

)
```




    <olivia_finder.package.Package at 0x7f3c2eb5c2e0>

"""

from __future__ import annotations
from typing import List, Optional

class Package:
    '''
    Class that represents a package in the network
    '''

    def __init__(
        self,
        name: str,
        version: Optional[str] = None,
        url: Optional[str] = None,
        dependencies: Optional[List[Package]] = None
    ):
        '''
        Constructor of the class

        Parameters
        ----------
        name : str
            Name of the package
        version : Optional[str], optional
            Version of the package, by default None
        url : Optional[str], optional
            Url of the package, by default None
        dependencies : Optional[List[Package]], optional
            List of dependencies of the package, by default None

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        
        '''

        self.name: str = name
        self.version: Optional[str] = version
        self.url: Optional[str] = url
        self.dependencies: List[Package] = [] if dependencies is None else dependencies

    def print(self):
        '''
        Print the package data in the console

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.print()
        
        Package:
            name: package
            version: 1.0.0
            url: https://package.org
            dependencies:
                dependency1:1.0.0
                dependency2:1.0.0
        '''
        print("Package:")
        print(f"  name: {self.name}")
        print(f"  version: {self.version}")
        print(f"  url: {self.url}")
        print("  dependencies:")
        for dependency in self.dependencies:
            print(f"    {str(dependency)}")

    def __eq__(self, other) -> bool:
        '''
        Compare two packages for equality

        Parameters
        ----------
        other : Package
            Package to compare with

        Returns
        -------
        bool
            True if the packages are equal, False otherwise

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package1 = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package2 = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package1 == package2
        '''
        return self.name == other.name and self.version == other.version

    def __hash__(self) -> int:
        '''
        Hash code of the package

        Returns
        -------
        int
            Hash code of the package

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> hash(package)
        '''
        
        hash_code = 0
        if self.name is not None:
            hash_code += hash(self.name)
        if self.version is not None:
            hash_code += hash(self.version)
        if self.url is not None:
            hash_code += hash(self.url)
        if self.dependencies is not None:
            hash_code += hash(tuple(self.dependencies))
        return hash_code

    def __str__(self) -> str:
        '''
        String representation of the package

        Returns
        -------
        str
            String representation of the package

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> str(package)
        numpy:1.0.0
        '''
        return self.name if self.version is None else f"{self.name}:{self.version}"

    def update(self, data: dict):
        '''
        Update the package with the data of a dictionary.
        Only the attributes version, url and dependencies are supported.

        Parameters
        ----------
        data : dict
            dictionary with the data to update

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.update({"version": "1.0.1"})
        '''

        if 'version' in data:
            self.version = data['version']
        if 'url' in data:
            self.url = data['url']
        if 'dependencies' in data:
            self.dependencies = list(set(data['dependencies']))

    def to_dict(self):
        '''
        Convert the package to a dictionary with the following structure:
            {
                'name': str,
                'version': str,
                'url': str,
                'dependencies': List[dict]
            }

        Returns
        -------
        dict
            dictionary with the data of the package

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.to_dict()
        '''

        # Create the dictionary
        data = {
            'name': self.name,
            'version': self.version,
            'url': self.url,
            'dependencies': []
        }

        # Add the dependencies as a dictionary
        for dependency in self.dependencies:
            data['dependencies'].append(dependency.to_dict())

        return data

    @classmethod
    def load(cls, data: dict):
        '''
        Loads a package from a dictionary. 
        It is assumed that the dictionary has the following structure::
        
            {   
                'name': str,
                'version': str,
                'url': str,
                'dependencies': List[dict]
            }

        Parameters
        ----------
        data : dict
            dictionary with the data

        Returns
        -------
        Package
            Package loaded from the dictionary

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package.load(
                {"name": "numpy", "version": "1.0.0", "url": "https://numpy.org"}
            )
        '''
        dependencies = [
            Package(dependency['name'], dependency['version'])
            for dependency in data['dependencies']
        ]
        return cls(data['name'], data['version'], data['url'], dependencies)

    def get_dependencies(self) -> List[Package]:
        '''
        Get the dependencies of the package or an empty list if there are no dependencies

        Returns
        -------
        List[Package]
            List with the dependencies

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.get_dependencies()
        '''
        return self.dependencies

    def get_dependencies_names(self) -> List[str]:
        '''
        Get the names of the dependencies of the package or an empty list if there are no dependencies

        Returns
        -------
        List[str]
            List with the names of the dependencies

        Examples
        --------
        >>> from olivia_finder.package import Package
        >>> package = Package("numpy", "1.0.0", "https://numpy.org")
        >>> package.get_dependencies_names()
        '''
        return [dependency.name for dependency in self.dependencies]