'''
File:              test_bioconductor.py
Project:           Olivia-Finder
Created Date:      Sunday March 5th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Sunday March 5th 2023 10:18:12 pm
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

from olivia_finder.scraping.bioconductor import BiocScraper
from olivia_finder.requests.proxy_handler import ProxyHandler
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.requests.useragent_handler import UserAgentHandler

bioconductor = Repo('Bioconductor', 'https://bioconductor.org')

# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh, use_logger=True)

# Initialize bioconductor scraper
bs = BiocScraper(rh)

# get list of packages
# time test
print("Getting list of packages...")
start_time = time.time()
bioconductor_packages = bs.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# get only the first 100 packages
print("Getting first 100 packages...")
bioconductor_packages = bioconductor_packages[:100]

# Scrape Bioconductor packages
print("Scraping data...")
start_time = time.time()
bioconductor.obtain_packages(bioconductor_packages, bs, extend_repo=True)
print("--- %s seconds ---" % (time.time() - start_time))
print("Bioconductor packages obtained")

# Define output file and folder
curr_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = curr_dir + os.sep + "persistence" + os.sep + "test" + os.sep

# Export the repository as raw data to a pickle file
print("Exporting data...")
start_time = time.time()
with open(output_folder + "bioconductor_raw.pickle", 'wb') as f:
    pickle.dump(bioconductor, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("Data exported to {}".format(output_folder + "bioconductor_raw.pickle"))

# Export the dependencies to a CSV file as dependency graph
print("Exporting dependencies...")
start_time = time.time()
bioconductor_df = bioconductor.to_full_adj_list()
with open(output_folder + "bioconductor_df.csv", 'w') as f:
    f.write(bioconductor_df.to_csv())
print("--- %s seconds ---" % (time.time() - start_time))
print("Dependencies exported to {}".format(output_folder + "bioconductor_df.csv"))
