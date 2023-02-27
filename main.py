'''
File:              main.py
Project:           Olivia-Finder
Created Date:      Friday February 24th 2023
Author:            Daniel Alonso Báscones
Last Modified:     Friday February 24th 2023 7:52:51 pm
Modified By:       The developer formerly known as dab0012 at dab0012@alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''

from olivia_finder.repo import Repo
# from olivia_finder.scrape.cran import CranScraper
# from olivia_finder.scrape.bioconductor import BiocScraper
from olivia_finder.scrape.pypi import PypiScraper
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.requests.proxy_handler import NoProxy, ProxyHandler
from olivia_finder.scrape.requests.useragent_handler import UserAgentHandler

import olivia_finder.load_config as load_config
import pickle

# Define the request handler
ph = ProxyHandler()
uh = UserAgentHandler()
rh = RequestHandler(ph, uh)


# Scrape Bioconductor packages
# ----------------------------------------------------------------------------

# # Define the repositories
# bioconductor = Repo('Bioconductor', 'https://bioconductor.org')

# # Initialize bioconductor scraper
# bs = BiocScraper(rh)

# # get list of packages
# bioconductor_packages = bs.get_list_of_packages()

# # Scrape Bioconductor packages
# bioconductor.scrape_packages(bioconductor_packages, bs)
# print("Bioconductor packages scraped")

# # Export the repository as raw data to a pickle file
# with open("persistence/bioconductor_raw.pickle", "wb") as f:
#     pickle.dump(bioconductor, f)

# # Export the dependencies to a CSV file as dependency graph
# bioconductor_df = bioconductor.to_package_graph_with_dependencies()
# bioconductor_df.to_csv("persistence/bioconductor_dependencies.csv")

# # Export the dependencies to a dictionary and save it to a pickle file
# bioconductor_dict = bioconductor.to_dict()
# with open("persistence/bioconductor_dict.pickle", "wb") as f:
#     pickle.dump(bioconductor_dict, f)


# Scrape CRAN packages
# ----------------------------------------------------------------------------

# # Define the repositories
# cran = Repo('CRAN', 'https://cran.r-project.org')

# # Initialize cran scraper
# cs = CranScraper(rh)

# # get list of packages
# cran_packages = cs.get_list_of_packages()

# # Scrape CRAN packages
# cran.scrape_packages(cran_packages, cs)
# print("CRAN packages scraped")

# # Export the repository as raw data to a pickle file
# with open("persistence/cran_raw.pickle", "wb") as f:
#     pickle.dump(cran, f)

# # Export the dependencies to a CSV file as dependency graph
# cran_df = cran.to_package_graph_with_dependencies()
# cran_df.to_csv("persistence/cran_dependencies.csv")

# # Export the dependencies to a dictionary and save it to a pickle file
# cran_dict = cran.to_dict()
# with open("persistence/cran_dict.pickle", "wb") as f:
#     pickle.dump(cran_dict, f)


# Scrape PyPI packages
# ----------------------------------------------------------------------------
# Define the repositories
pypi = Repo('PyPI', 'https://pypi.org')

# Initialize pypi scraper
ps = PypiScraper(rh)

# get list of packages
pypi_packages = ps.get_list_of_packages()

# Scrape PyPI packages
pypi.scrape_packages(pypi_packages, ps)
print("PyPI packages scraped")

# Export the repository as raw data to a pickle file
with open("persistence/pypi_raw.pickle", "wb") as f:
    pickle.dump(pypi, f)

# Export the dependencies to a CSV file as dependency graph
pypi_df = pypi.to_package_graph_with_dependencies()
pypi_df.to_csv("persistence/pypi_dependencies.csv")

# Export the dependencies to a dictionary and save it to a pickle file
pypi_dict = pypi.to_dict()
with open("persistence/pypi_dict.pickle", "wb") as f:
    pickle.dump(pypi_dict, f)

