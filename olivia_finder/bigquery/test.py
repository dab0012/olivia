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
# Add olivia_finder directory to the path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
# ----------------------------------------------------------------------------

from olivia_finder.bigquery.librariesio_bigquery import LibrariesioBigQuery

# Testing the class

libio = LibrariesioBigQuery('NPM')

# Testing the method get_suported_package_managers
# supoorted_platforms = libio.get_suported_package_managers()
# print(supoorted_platforms)

#Testing the method obtain_package_names
# package_names = libio.obtain_package_names(1000)
# print(package_names)

# Testing the method obtain_package
package = libio.obtain_package('@specron/sandbox')

if package is not None:
    package.print()
else:
    print('Package not found')