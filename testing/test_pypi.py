# TEST PyPI packages
# ----------------------------------------------------------------------------
# Define the repositories
import os
import pickle
import time
from urllib.request import ProxyHandler

# Add the olivea_finder directory to the path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from olivia_finder.repo import Repo
from olivia_finder.scrape.pypi import PypiScraper
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler
from olivia_finder.scrape.requests.proxy_builder import NoProxy


pypi = Repo('PyPI', 'https://pypi.org')

# Define the request handler
ph = ProxyHandler(NoProxy())
uh = UserAgentHandler()
rh = RequestHandler(ph, uh)

# Initialize pypi scraper
ps = PypiScraper(rh)

# get list of packages
# time test 
print("Getting list of packages...")
start_time = time.time()
pypi_packages = ps.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# get only the first 100 packages
pypi_packages = pypi_packages[:100]

# Scrape PyPI packages
print("Scraping PyPI packages...")
start_time = time.time()
pypi.obtain_packages(pypi_packages, ps, extend_repo=True)
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPI packages scraped")

# Export the repository as raw data to a pickle file
print("Exporting PyPI repo...")
start_time = time.time()
with open("persistence/test/pypi_raw.pickle", "wb") as f:
    pickle.dump(pypi, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPI packages exported")

# Export the dependencies to a CSV file as dependency graph
print("Exporting PyPI dependencies as csv...")
start_time = time.time()
pypi_df = pypi.to_full_adj_list()
pypi_df.to_csv("persistence/test/pypi_dependencies.csv")
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPI dependencies exported")

# Export the dependencies to a dictionary and save it to a pickle file
print("Exporting PyPI dependencies as dict...")
start_time = time.time()
pypi_dict = pypi.to_dict()
with open("persistence/test/pypi_dict.pickle", "wb") as f:
    pickle.dump(pypi_dict, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("PyPI dependencies exported")