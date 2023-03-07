import os
from google.cloud import bigquery

class BigQueryClient:
    '''A class to handle Google's BigQuery queries and table previews.'''

    KEY_FILE = f'{os.path.dirname(os.path.abspath(__file__))}{os.sep}key.json'

    def __init__(self, project_id, dataset_id):
        '''
        Constructor.
        
        Parameters
        ----------
        project_id : str
            ID of the project to connect to.
        dataset_id : str
            ID of the dataset to connect to.
        '''

        # export google application credentials to environment variable
        # this is needed to authenticate with the Google Cloud Platform
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.KEY_FILE

        self.client = bigquery.Client(project=project_id)
        self.dataset_ref = self.client.dataset(dataset_id)

        # add api key to client
        

        

    def select(self, table_name, columns, limit=10) -> list:
        '''
        Selects rows from a table.
        
        Parameters
        ----------
        table_name : str
            Name of the table to select from.
        columns : list
            List of columns to select.
        limit : int, optional
            Number of rows to select, by default 10
            
        Returns
        -------
        list
            List of rows returned by the query.
        '''
        
        # create query
        query = f'SELECT {", ".join(columns)} FROM `{self.dataset_ref}.{table_name}` LIMIT {limit}'

        # run query
        return self.run_query(query)
    
    def run_query(self, query) -> list:
        '''
        Runs a query.
        
        Parameters
        ----------
        query : str
            Query to run.
            
        Returns
        -------
        list
            List of rows returned by the query.
        '''
        query_job = self.client.query(query)
        rows = query_job.result()
        return [row.values() for row in rows]

    def list_tables(self) -> list:
        '''
        Lists the tables in the dataset.
        
        Returns
        -------
        list
            List of table names.
        '''
        tables = self.client.list_tables(self.dataset_ref)
        return [table.table_id for table in tables]

    def preview_table(self, table_name, num_rows=5) -> list:
        '''
        Previews a table.

        Parameters
        ----------
        table_name : str
            Name of the table to preview.
        num_rows : int, optional
            Number of rows to preview, by default 5

        Returns
        -------
        list
            List of rows in the table.
        '''
        table_ref = self.dataset_ref.table(table_name)
        table = self.client.get_table(table_ref)
        rows = self.client.list_rows(table, max_results=num_rows)
        return [row.values() for row in rows]
    

# Testing the class

bqc = BigQueryClient('bigquery-public-data', 'libraries_io')
print(bqc.list_tables())
print(bqc.preview_table('repositories'))

# Get 10 packages of CRAN and their dependencies
query = """
SELECT
    package_name,
    repository_dependencies.repository_name AS dependency
FROM
    `bigquery-public-data.libraries_io.packages`
WHERE
    package_manager = 'CRAN'
LIMIT
    10
"""

print(bqc.run_query(query))