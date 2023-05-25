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

# Import the necessary modules
from olivia_finder.utilities.config import Configuration
from olivia_finder.utilities.logger import MyLogger

# Custom logger for the module
logger_name = Configuration().get_key('logger', 'scraping_name')
MyLogger.get_logger(
    logger_name=logger_name,
    level=Configuration().get_key('logger', 'global_level'),
    enable_console=Configuration().get_key('logger', 'scraping_console'),
    console_level=Configuration().get_key('logger', 'scraping_console_level'),
    filename=f"{Configuration().get_key('folders', 'logger')}/{Configuration().get_key('logger', 'scraping_filename')}",
    file_level=Configuration().get_key('logger', 'scraping_file_level')
)

# Deactivate the logger if configured
if Configuration().get_key('logger', 'scraping_status').lower() == "disabled":
    MyLogger.disable_console(logger_name=logger_name)
    MyLogger.disable_file(logger_name=logger_name)