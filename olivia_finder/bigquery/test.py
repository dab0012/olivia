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

#

# Fix path
# ----------------------------------------------------------------------------
import os, sys, inspect

import pandas as pd

# Add olivia_finder directory to the path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
# ----------------------------------------------------------------------------

from olivia_finder.bigquery.librariesio_bigquery import LibrariesioBigQuery
from olivia_finder.package_manager import PackageManager


# Testing the class

libio = LibrariesioBigQuery('CRAN')

#Testing the method get_suported_package_managers
# supoorted_platforms = libio.get_suported_package_managers()
# print(supoorted_platforms)

#Testing the method obtain_package_names
# package_names = libio.obtain_package_names(1000)
# print(package_names)

# Testing the method obtain_package
# package_list = libio.obtain_dependency_network()
# for package in package_list:
#     package.print()


pm = PackageManager(
    data_source=libio,
    name = 'CRAN'
)

# # Get package name list
# package_names = libio.obtain_package_names()
pm.obtain_packages(extend_repo=True)

df : pd.DataFrame = pm.to_full_adj_list()

# Save the dataframe
df.to_csv('CRAN.csv', index=False)