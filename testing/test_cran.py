# TEST CRAN packages
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
from olivia_finder.scrape.cran import CranScraper
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler
from olivia_finder.scrape.requests.proxy_builder import GeonodeProxy

cran = Repo('CRAN', 'https://cran.r-project.org')

# Define the request handler
ph = ProxyHandler(GeonodeProxy())
uh = UserAgentHandler()
rh = RequestHandler(ph, uh)

# Initialize cran scraper
cs = CranScraper(rh)

# get list of packages
# time test
print("Getting list of packages...")
start_time = time.time()
cran_packages = cs.obtain_package_names()
print("--- %s seconds ---" % (time.time() - start_time))

# get only the first 100 packages
cran_packages = cran_packages[:100]

# Scrape CRAN packages
print("Scraping CRAN packages...")
start_time = time.time()
cran.obtain_packages(cran_packages, cs, extend_repo=True)

print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN packages scraped")

# Export the repository as raw data to a pickle file
print("Exporting CRAN repo...")
start_time = time.time()
with open("persistence/test/cran_raw.pickle", "wb") as f:
    pickle.dump(cran, f)
print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN packages exported")

# Export the dependencies to a CSV file as dependency graph
print("Exporting CRAN dependencies as csv...")
start_time = time.time()
cran_df = cran.to_full_adj_list()
with open("persistence/test/cran_df.csv", "w") as f:
    f.write(cran_df.to_csv())
print("--- %s seconds ---" % (time.time() - start_time))
print("CRAN dependencies exported")
