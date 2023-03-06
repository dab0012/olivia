from google.cloud import bigquery

class BigQueryClient:
    '''A class to handle Google's BigQuery queries and table previews.'''

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
        self.client = bigquery.Client(project=project_id)
        self.dataset_ref = self.client.dataset(dataset_id)

    def run_query(self, query) -> list:
        '''
        Runs a query and returns the results.
        
        Parameters
        ----------
        query : str
            Query to run.
            
        Returns
        -------
        list
            List of rows returned by the query.
        '''
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = False
        query_job = self.client.query(query, job_config=job_config, location="US")
        return query_job.result()

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