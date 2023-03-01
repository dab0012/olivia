'''
File:              maven.py
Project:           Olivia-Finder
Created Date:      Wednesday March 1st 2023
Author:            Daniel Alonso Báscones
Last Modified:     Wednesday March 1st 2023 9:24:30 pm
Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
-----
Copyright (c) 2023 Daniel Alonso Báscones
-----
'''


import logging, requests
from typing import Dict, Union
from bs4 import BeautifulSoup
from olivia_finder.scrape.requests.request_handler import RequestHandler
from olivia_finder.scrape.scraper import Scraper
from olivia_finder.package import Package

class MvnScraper(Scraper):
    ''' 
    Class that scrapes the Maven website to obtain information about Java packages
    '''

    pass