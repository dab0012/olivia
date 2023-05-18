'''

Module that contains the custom implementation of the Scraper class for a set of package managers

The included package managers are:

## **NPM**
(Node Package Manager from https://www.npmjs.com/)
`olivia_finder.data_source.repository_scrapers.npm.NpmScraper`

## **PyPI**
(Python Package Index from https://pypi.org/)
`olivia_finder.data_source.repository_scrapers.pypi.PypiScraper`

## **CRAN** 
(Comprehensive R Archive Network from https://cran.r-project.org/)
`olivia_finder.data_source.repository_scrapers.cran.CranScraper`

## **Bioconductor**
(Bioconductor from https://www.bioconductor.org/)
`olivia_finder.data_source.repository_scrapers.bioconductor.BioconductorScraper`

'''

from olivia_finder.utilities.logger import MyLogger
from olivia_finder.utilities.config import Configuration

# Custom logger for the module
MyLogger.get_logger(
    logger_name="scraper",
    enable_console=False,
    log_file=Configuration().get_key('folders', 'log_dir') + "/scraper.log",
    log_level=Configuration().get_key('logger', 'level')
)