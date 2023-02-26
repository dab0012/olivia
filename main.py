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
from olivia_finder.scrape.cran import CranScraper
from olivia_finder.scrape.bioconductor import BiocScraper
from olivia_finder.scrape.requests.request_handler import RequestHandler
import olivia_finder.load_config as load_config

# Define the request handler
rh = RequestHandler(max_request=20)

# Define the repositories
cran = Repo('CRAN', 'https://cran.r-project.org')
bioconductor = Repo('Bioconductor', 'https://bioconductor.org')

# Scrape Bioconductor packages
bs = BiocScraper(rh)
bioconductor.scrape_packages(bs.get_list_of_packages(), bs)
print("Bioconductor packages scraped")
bioconductor.to_csv("./persistence/bioconductor.csv")

# Scrape CRAN packages
cs = CranScraper(rh)
cran.scrape_packages(cs.get_list_of_packages(), cs)
print("CRAN packages scraped")
cran.to_csv("./persistence/cran.csv")
