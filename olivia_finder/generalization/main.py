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

from repo import Repo
from scrapers.cran import CranScraper
from scrapers.bioconductor import BiocScraper
from scrapers.requests.request_handler import RequestHandler
import load_config

# Define the request handler
rh = RequestHandler(max_request=20)

# Define the repositories
cran = Repo('CRAN', 'https://cran.r-project.org')
bioconductor = Repo('Bioconductor', 'https://bioconductor.org')

bs = BiocScraper(rh)
bioconductor.scrape_packages(bs.get_list_of_packages(), bs)


# p = bioconductor.scrape_package("a4", BiocScraper(rh))
# p.print()

#list = cran.scrape_packages(["MASS", "ggplot2"], CranScraper(rh))

# for p in list:
#     p.print()


# package_list = CranScraper(rh).get_list_of_packages()
# print(package_list)

# bioconductor_list = BiocScraper(rh).get_list_of_packages()
# print(bioconductor_list)

