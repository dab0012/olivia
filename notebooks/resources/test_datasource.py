# Add the environment variable OLIVIA_FINDER_CONFIG_FILE_PATH
import os
os.environ['OLIVIA_FINDER_CONFIG_FILE_PATH'] = "config.ini"


from olivia_finder.package_manager import PackageManager
from olivia_finder.data_source.repository_scrapers.cran import CranScraper


cran_pm_scraper = PackageManager(
    data_sources=[CranScraper()]
)

print("Cran packages:")
print(cran_pm_scraper.fetch_package_names()[300:320])

print("Cran package jacobi:")
print(cran_pm_scraper.fetch_package("jacobi"))

