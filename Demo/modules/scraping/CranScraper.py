# Author: Daniel Alonso Báscones
# Date: 2022-2-21
# Project: TFG OLIVIA

import re
from bs4 import BeautifulSoup
from modules.Package import Package
from modules.Dependency import Dependency
from modules.scraping.ProxyRequest import RequestHandler

from typing import Dict, List, Tuple


class CranScraper:
    '''
    Class that scrapes the CRAN website to obtain information about R packages
    '''

    def __init__(self, request_handler: RequestHandler) -> None:
        '''
        Class constructor
        
        Parameters
        ----------
        request_handler : RequestHandler
            Request handler object
            
        Returns
        -------
            None
        '''

        self.request_handler = request_handler

    def __parse_pkg_data(self, pkg_name) -> Dict[str, str]:
        '''
        Get data from a CRAN packet.
        It's obtained from the package page in the CRAN website.
        This function has to be called from the get_pkg_data function.
        Obtain the data through HTML scraping on the page, in addition, if any of the optional data is not found, the rest of the data is continued

        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        Dict[str, str]
            Dictionary with the data of the package

        Raises
        ------
        Exception
            If the package is not found or any of the optional data is not found
            If any of the optional data is not found, the scraper will continue handling the rest of the data

        '''

        # Make HTTP request to package page, the package must exist, otherwise an exception is raised
        url = f'https://cran.r-project.org/package={pkg_name}'
        try:
            response = self.request_handler.do_request(url)
        except Exception as e:
            print(f'Exception getting package {pkg_name}: {e}')
            return None

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get Name and Description
        # ------------------------
        name = soup.title.text.split(':')[0]
        description = soup.find('p').text.strip()

        # Get optional table data
        # -----------------------      

        #region OPTIONAL TABLE DATA

        # Get package version
        try:
            version = soup.find('td', text='Version:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting version for package {pkg_name}: {e}')

        # Get publication date
        try:
            publication_date = soup.find(
                'td', text='Published:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting publication date for package {pkg_name}: {e}')

        # Get author
        try:
            author = soup.find('td', text='Author:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting author for package {pkg_name}: {e}')

        # Get mantainer
        try:
            mantainer = soup.find('td', text='Maintainer:').find_next_sibling('td').text.strip().replace(' at ', '@')
        except Exception as e:
            print(f'Exception getting mantainer for package {pkg_name}: {e}')

        # Get license
        try:
            license = soup.find('td', text='License:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting license for package {pkg_name}: {e}')

        # Get compilation requirement
        try:
            requires_compilation = soup.find('td', text='NeedsCompilation:').find_next_sibling('td').text.strip()
            requires_compilation = requires_compilation == 'yes'    # Convert to boolean
        except Exception as e:
            print(f'Exception getting compilation requirement for package {pkg_name}: {e}')

        # Get dependencies
        try:
            depends = soup.find('td', text='Depends:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting dependencies for package {pkg_name}: {e}')

        # Get imports
        try:
            imports = soup.find('td', text='Imports:').find_next_sibling('td').text.strip()
        except Exception as e:
            print(f'Exception getting imports for package {pkg_name}: {e}')

        #endregion

        # Build dictionary with package data
        return {
            'name': name,
            'description': description,
            'version': version,
            'publication_date': publication_date,
            'author': author,
            'mantainer': mantainer,
            'license': license,
            'requires_compilation': requires_compilation,
            'depends': depends,
            'imports': imports
        }

    def __parse_dependencies(self, dependencies_str, type) -> List[Tuple[str, str]]:
        '''
        Parse dependencies data and handle exceptions

        Parameters
        ----------
        dependencies_str : str
            String with dependencies data
        type : str
            Type of dependency

        Returns
        List[Tuple[str, str]]
            List of dependencies
        '''

        # Remove unnecessary line breaks, tabs, and spaces
        patron = r'\S+\s*(?:\(([^\)]*)\))?'

        # Get names and versions of dependencies
        versiones = [re.findall(patron, dep)[0] if re.findall(patron, dep) else '' for dep in dependencies_str.split(",")]
        nombres = [re.sub(r'\s*\(.*\)', '', nombre.strip()) for nombre in dependencies_str.split(",")]

        dependencies = []
        # Return list of dependency objects
        for i in range(len(nombres)):
            d = Dependency()
            d.create(nombres[i], type, versiones[i])
            dependencies.append(d)

        return dependencies

    def pkg_builder(self, pkg_name) -> Package:
        '''
        Build a Package object with the data of the scraped package

        Parameters
        ----------
        pkg_name : str
            Name of the package

        Returns
        -------
        Package
            Package object with the data of the scraped package
        ''' 

        # Get package data from HTML scraping
        pkg_data = self.__parse_pkg_data(pkg_name)

        # Parse dependencies data and handle exceptions
        dep_list = []
        for dep_type in ['depends', 'imports']:
            try:
                dep_list += self.__parse_dependencies(pkg_data.get(dep_type), dep_type)
            except Exception as e:
                print(f'Exception parsing dependencies of package {pkg_name}: {e}')
                dep_list = []

        # Set package attributes
        package = Package()
        package.name = pkg_name
        package.description = pkg_data['description']
        package.version = pkg_data['version']
        package.publication_date = pkg_data['publication_date']
        package.author_data = pkg_data['author']
        package.mantainer = pkg_data['mantainer']
        package.license = pkg_data['license']
        package.requires_compilation = pkg_data['requires_compilation']
        package.dependencies = dep_list
        package.url = f'https://cran.r-project.org/package={pkg_name}'

        # Return package
        return package
