# Add the environment variable OLIVIA_FINDER_CONFIG_FILE_PATH
import os
os.environ['OLIVIA_FINDER_CONFIG_FILE_PATH'] = "olivia_finder/config.ini"

import tqdm
from olivia_finder.package_manager import PackageManager
from olivia_finder.data_source.repository_scrapers.cran import CranScraper

# Test cran package manager
cran_pm_scraper = PackageManager(data_sources=[CranScraper()])

# Test fetch package names
test_packages = cran_pm_scraper.fetch_package_names()[300:350]

# Test fetch packages
progress_bar = tqdm.tqdm(total=len(test_packages))
cran_pm_scraper.fetch_packages(test_packages, progress_bar=progress_bar, extend=True)

# Export to csv
df = cran_pm_scraper.export_dataframe(full_data=True)
df.to_csv("test.csv", index=False)

print(df.head(50))


