'''
File:              test_npm.py
Project:           Olivia-Finder
Created Date:      Sunday March 5th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Sunday March 5th 2023 10:30:16 pm
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
from olivia_finder.repo import Repository
from olivia_finder.scraping.npm import NpmScraper
from olivia_finder.requests.proxy_handler import ProxyHandler
from olivia_finder.requests.request_handler import RequestHandler
from olivia_finder.requests.useragent_handler import UserAgentHandler

npm = Repository('NPM', 'https://www.npmjs.com')

# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh, use_logger=True)

# Initialize npm scraper
ns = NpmScraper(rh)

# get list of packages
# time test
print("Getting list of packages...")
start_time = time.time()
npm_packages = ns.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# Define output file and folder
curr_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = curr_dir + os.sep + "persistence" + os.sep + "test" + os.sep

# store list of packages
with open(output_folder + "npm_packages.pickle", "wb") as f:
    pickle.dump(npm_packages, f)

# get only the first 100 packages
print("Getting first 100 packages...")
npm_packages = npm_packages[:100]

# Scrape NPM packages
print("Scraping data...")
start_time = time.time()
npm.obtain_packages(npm_packages, ns, extend_repo=True)
print("--- %s seconds ---" % (time.time() - start_time))
print("NPM packages obtained")

# store repo
print("Storing repo...")
start_time = time.time()
with open(output_folder + "npm_raw.pickle", "wb") as f:
    pickle.dump(npm, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("Repo stored")

# Export the dependencies to a CSV file as dependency graph
print("Exporting dependencies...")
start_time = time.time()
with open(output_folder + "npm_df.csv", "w") as f:
    npm.to_full_adj_list(f)
print("--- %s seconds ---" % (time.time() - start_time))
print("Dependencies exported")





