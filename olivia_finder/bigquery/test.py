# import os
# from google.cloud import bigquery

# KEY_FILE = f'{os.path.dirname(os.path.abspath(__file__))}{os.sep}key.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_FILE

# client = bigquery.Client()

# # Perform a query.
# QUERY = ('SELECT * FROM `bigquery-public-data.libraries_io.dependencies` WHERE platform="NPM" LIMIT 10')
# query_job = client.query(QUERY)  # API request
# rows = query_job.result()  # Waits for query to finish

# for row in rows:
#     print(row.project_name)


from google.cloud import bigquery
import os
import pandas as pd

class BigQueryClient:
    def __init__(self, key_file_path):
        # Set the environment variable for the service account key file path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file_path

        # Create a BigQuery client object
        self.client = bigquery.Client()

    def run_query(self, query):
        # Run the query and return the result
        query_job = self.client.query(query)
        return query_job.result()

if __name__ == '__main__':
    # Set the path to the service account key file
    KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.json')

    # Create a BigQuery client object using the service account key file
    bq_client = BigQueryClient(KEY_FILE)

    # Define the query
    QUERY = ('SELECT * FROM `bigquery-public-data.libraries_io.dependencies` WHERE platform="NPM"')

    # Run the query and print the result
    rows = bq_client.run_query(QUERY)
    df = rows.to_dataframe()
 
    #save pandas dataframe to csv
    OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out.csv')

    df.to_csv('output.csv', index=False)
