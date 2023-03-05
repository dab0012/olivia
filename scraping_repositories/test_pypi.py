'''
File:              test_pypi.py
Project:           Olivia-Finder
Created Date:      Wednesday March 1st 2023
Author:            Daniel Alonso Báscones
Last Modified:     Wednesday March 1st 2023 8:49:50 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

# Fix path
# ----------------------------------------------------------------------------
import os, sys, inspect
# Add olivia_finder directory to the path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# Imports
# ----------------------------------------------------------------------------
import pickle, time
from olivia_finder.repo import Repo
from olivia_finder.scraping.pypi import PypiScraper
from olivia_finder.requests.proxy_handler import ProxyHandler
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.requests.useragent_handler import UserAgentHandler

pypi = Repo('PyPi', 'https://pypi.org')

# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh, use_logger=True)

# Initialize pypi scraper
ps = PypiScraper(rh)

# get list of packages
# time test
print("Getting list of packages...")
start_time = time.time()
pypi_packages = ps.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# get only the first 100 packages
print("Getting first 100 packages...")
pypi_packages = pypi_packages[:100]

# Scrape PyPi packages
print("Scraping data...")
start_time = time.time()
pypi.obtain_packages(pypi_packages, ps, extend_repo=True)
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPi packages obtained")

# Define output file and folder
# Define output file and folder
curr_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = curr_dir + os.sep + "persistence" + os.sep + "test" + os.sep

# Export the repository as raw data to a pickle file
print("Exporting PyPi repo...")
start_time = time.time()
with open(output_folder + 'pypi_raw.pickle', 'wb') as f:
    pickle.dump(pypi, f)
print("--- %s seconds ---" % (time.time() - start_time))

# Export the dependencies to a CSV file as dependency graph
print("Exporting PyPi dependencies as csv...")
start_time = time.time()
pypi_df = pypi.to_full_adj_list()
with open(output_folder + "pypi_df.csv", "w") as f:
    f.write(pypi_df.to_csv())
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPi dependencies exported")

