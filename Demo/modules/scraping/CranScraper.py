# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

import re
from bs4 import BeautifulSoup
from modules.Package import Package
from modules.Dependency import Dependency
from modules.scraping.ProxyRequest import RequestHandler

from typing import Dict, List, Tuple


class CranScraper:

    # Class constructor
    def __init__(self, request_handler: RequestHandler) -> None:

        self.request_handler = request_handler

    # Get data from a CRAN packet
    def __parse_pkg_data(self, pkg_name) -> Dict[str, str]:
        # Make HTTP request to package page
        url = f'https://cran.r-project.org/package={pkg_name}'
        response = self.request_handler.do_request(url)
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get elements of interest from HTML
        name = soup.title.text.split(':')[0]
        description = soup.find('p').text.strip().replace('\n', '').replace('\t', '').replace('   ', '')

        # Get optional table data
        try :
            version = soup.find('td', text='Version:').find_next_sibling('td').text.strip().replace('\n', '')
        except Exception as e:
            version = None
            print(f'Exception getting version for package {pkg_name}: {e}')

        try :
            publication_date = soup.find('td', text='Published:').find_next_sibling('td').text.strip()
        except Exception as e:
            publication_date = None
            print(f'Exception getting publication date for package {pkg_name}: {e}')

        try :
            author = soup.find('td', text='Author:').find_next_sibling('td').text.strip()
        except Exception as e:
            author = None
            print(f'Exception getting author for package {pkg_name}: {e}')

        try :
            mantainer = soup.find('td', text='Maintainer:').find_next_sibling('td').text.strip().replace(' at ', '@')
        except Exception as e:
            mantainer = None
            print(f'Exception getting mantainer for package {pkg_name}: {e}')

        try :
            license = soup.find('td', text='License:').find_next_sibling('td').text.strip()
        except Exception as e:
            license = None
            print(f'Exception getting license for package {pkg_name}: {e}')

        try :
            requires_compilation = soup.find('td', text='NeedsCompilation:').find_next_sibling('td').text.strip()
            requires_compilation = requires_compilation == 'yes'

        except Exception as e:
            requires_compilation = None
            print(f'Exception getting compilation requirement for package {pkg_name}: {e}')

        try :
            depends = soup.find('td', text='Depends:').find_next_sibling('td').text.strip()
        except Exception as e:
            depends = None
            print(f'Exception getting dependencies for package {pkg_name}: {e}')

        try :
            imports = soup.find('td', text='Imports:').find_next_sibling('td').text.strip()
        except Exception as e:
            imports = None
            print(f'Exception getting imports for package {pkg_name}: {e}')

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

    # Parse dependencies data
    def __parse_dependencies(self, dependencies_str, type) -> List[Tuple[str, str]]:
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

    # Construct object of class Package
    def pkg_builder(self, pkg_name) -> Package:

        # Get package data
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
        package.description =  pkg_data['description']
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