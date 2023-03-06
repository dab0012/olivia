'''
File:              test_cran.py
Project:           Olivia-Finder
Created Date:      Wednesday March 1st 2023
Author:            Daniel Alonso Báscones
Last Modified:     Wednesday March 1st 2023 9:12:14 pm
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
from olivia_finder.package_manager import PackageManager
from olivia_finder.scraping.cran import CranScraper
from olivia_finder.requests.proxy_handler import ProxyHandler
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.requests.useragent_handler import UserAgentHandler

cran = PackageManager('CRAN', 'https://cran.r-project.org')

# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh, use_logger=True)

# Initialize cran scraper
cs = CranScraper(rh)

# get list of packages
# time test
print("Getting list of packages...")
start_time = time.time()
cran_packages = cs.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# get only the first 100 packages
print("Getting first 100 packages...")
cran_packages = cran_packages[:100]

# Scrape CRAN packages
print("Scraping data...")
start_time = time.time()
cran.obtain_packages(cran_packages, cs, extend_repo=True)

print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN packages obtained")

# Define output file and folder
curr_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = curr_dir + os.sep + "persistence" + os.sep + "test" + os.sep

# Export the repository as raw data to a pickle file
print("Exporting CRAN repo...")
start_time = time.time()
with open(output_folder + "cran_raw.pickle", "wb") as f:
    pickle.dump(cran, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN packages exported")

# Export the dependencies to a CSV file as dependency graph
print("Exporting CRAN dependencies as csv...")
start_time = time.time()
cran_df = cran.to_full_adj_list()
with open(output_folder + "cran_df.csv", "w") as f:
    f.write(cran_df.to_csv())
print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN dependencies exported")
