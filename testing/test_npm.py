import os
import pickle

# Add the olivea_finder directory to the path
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from olivia_finder.repo import Repo
from olivia_finder.scrape.requests.proxy_handler import ProxyHandler
from olivia_finder.scrape.npm import NpmScraper
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler
from olivia_finder.scrape.requests.proxy_builder import GeonodeProxy
from olivia_finder.config import LoggerConfiguration

# Configure the logger
LoggerConfiguration('testing/npm.log', 'DEBUG').aply_config()


npm = Repo('NPM', 'https://www.npmjs.com/package/')

# Define the request handler
rh = RequestHandler(
    proxy_handler           = ProxyHandler(GeonodeProxy()), 
    useragents_handler      = UserAgentHandler(),
    request_timeout         = 30
)

# Initialize cran scraper
ns = NpmScraper(rh)

# Get the list of packages
packages = ns.obtain_package_names()

# Get the startkeys for future implementations and save them
startkeys = ns.GET_NAMES_KEYS
with open('testing/npm_startkeys.pkl', 'wb') as f:
    pickle.dump(startkeys, f)


# Save the list of packages
print('Saving package names...')
with open('testing/npm_package_names.pkl', 'wb') as f:
    pickle.dump(packages, f)
print('Done!')

# write the package names to a csv file
print('Writing package names to csv file...')
with open('testing/npm_package_names.csv', 'w') as f:
    f.write('package_name\n')
    for package in packages:
        f.write(package + '\n')
print('Done!')

# # Load the list of packages
# print('Loading package names...')
# start_time = time.time()
# with open('testing/npm_package_names.pkl', 'rb') as f:
#     package_name_list = pickle.load(f)
# print('Done! Ttotal time: %s seconds' % (time.time() - start_time))

# order the packages alphabetically
print('Ordering packages...')
start_time = time.time()
packages.sort()
print('Done! Ttotal time: %s seconds' % (time.time() - start_time))

# Initialize the repository
print("Initializing NPM repo...")
npm = Repo('NPM', 'https://www.npmjs.com/package/')

# Scrape the packages
print("Scraping NPM packages...")
start_time = time.time()
packages = []
packages = npm.obtain_packages(pkg_names=packages, scraper=ns, extend_repo=True)
print("NPM packages scraped")
print("Total time: %s seconds" % (time.time() - start_time))

# Export the repository as raw data to a pickle file
print("Exporting NPM repo...")
start_time = time.time()
with open("testing/npm_repo.pkl", "wb") as f:
    pickle.dump(npm, f)
print("NPM repo exported in %s seconds" % (time.time() - start_time))

# Export the repository as a adjacency list to a csv file
print("Exporting NPM repo as adjacency list...")
start_time = time.time()
npm.to_full_adj_list(packages, "testing/npm_full_adj_list.csv")
print("NPM repo exported as adjacency list in %s seconds" % (time.time() - start_time))


