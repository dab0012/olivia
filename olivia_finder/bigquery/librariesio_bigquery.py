from olivia_finder.bigquery.bigquery_handler import BigQueryClient

class LibrariesioBigQuery:
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
        project_id : str
            ID of the project to connect to.
        dataset_id : str
            ID of the dataset to connect to.
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
            FROM `bigquery-public-data.libraries_io.packages`
            ORDER BY platform
        '''
        query_job = self.client.run_query(query)
        return [row.platform for row in query_job]
    
    def obtain_package_names(self) -> list:
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
            FROM `bigquery-public-data.libraries_io.packages`
            WHERE platform = '{}'
            ORDER BY name
        '''.format(self.package_manager)

        # Run the query
        result_query = self.client.run_query(query)

        return [row.name for row in result_query]
    



    
