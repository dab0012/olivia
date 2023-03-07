from typing_extensions import override
from numpy import DataSource
from olivia_finder.bigquery.bigquery_handler import BigQueryClient
from olivia_finder.package import Package

class LibrariesioBigQuery(DataSource):
    '''Class to handle the Libraries.io BigQuery data'''

    PROJECT_ID: str = 'bigquery-public-data'
    DATASET_ID: str = 'libraries_io'
    client: BigQueryClient
    package_manager: str

    def __init__(self, package_manager: str = None):
        '''
        Constructor.

        Parameters
        ----------
        package_manager : str
            Package manager to use.
        '''
        self.client = BigQueryClient(self.PROJECT_ID, self.DATASET_ID)
        self.package_manager = package_manager

    def get_suported_package_managers(self) -> list:
        '''
        Gets the supported package managers.

        Returns
        -------
        list
            List of supported package managers.
        '''

        query = '''
            SELECT DISTINCT platform
            FROM `bigquery-public-data.libraries_io.projects`
            ORDER BY platform
        '''
        query_job = self.client.run_query(query)
        
        return [platform_name[0] for platform_name in query_job]
    
    @override
    def obtain_package_names(self, limit: int = None) -> list:
        '''
        Obtains the package names of the package manager specified in the constructor.

        Returns
        -------
        list
            List of package names.
        '''

        # Build the query
        query = '''
            SELECT DISTINCT name
            FROM `bigquery-public-data.libraries_io.projects`
            WHERE platform = '{}'
            ORDER BY name
        '''.format(self.package_manager)

        if limit is not None:
            query += ' LIMIT {}'.format(limit)

        # Run the query
        result_query = self.client.run_query(query)

        return [row[0] for row in result_query]
    
    @override
    def obtain_package(self, package_name: str) -> Package:
        '''
        Obtains the package with the specified name.

        Parameters
        ----------
        package_name : str
            Name of the package to obtain.

        Returns
        -------
        Package
            Package with the specified name.
        '''

        # Build the query to get the data of the latest version of the package
        query = '''
            SELECT 
                project_name, version_number, dependency_name, dependency_requirements 
            FROM `bigquery-public-data.libraries_io.dependencies` 
            where 
                project_name = '{}'
                and 
                platform = '{}'
                and version_number = (
                    SELECT 
                        MAX(version_number) 
                    FROM 
                        `bigquery-public-data.libraries_io.dependencies` 
                    where 
                        project_name = '{}' 
                        and 
                        platform = '{}'
                )'''.format(package_name, self.package_manager, package_name, self.package_manager)
            
        # Run the query
        result_query = self.client.run_query(query)

        # Check if the package exists
        if len(result_query) == 0:
            return None

        # Get package version
        package_version = result_query[0][1]

        # Build the dependencies
        dependencies = []
        for row in result_query:
            dep_name = row[2]
            dep_version = row[3]
            d = Package(name = dep_name, version = dep_version)
            dependencies.append(d)
    
        # Build the package
        package = Package(
            package_name,               # Name
            package_version,            # Version
            None,                       # URL
            dependencies                # Dependencies
        )

        return package
    



    
