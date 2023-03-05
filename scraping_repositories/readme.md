Scraping Repositories
===========

The `test_module.py` module is an example script that demonstrates how to use the `olivia_finder` package to scrape and obtain data from a generic repository.

Usage
=====

This module can be used to obtain data from any generic repository by modifying the `Repo` and `Scraper` classes to match the structure of the desired repository. The script currently demonstrates how to scrape data from a generic repository and export it as raw data to a pickle file, and as a dependency graph to a CSV file.


Example
=======

To run the example script, navigate to the directory containing `test_module.py` and run the following command:

Copy code

`python test_module.py`

This will scrape data from the generic repository and export it as raw data to a pickle file, and as a dependency graph to a CSV file in the `persistence/test` directory.

Current Status
==============

The scripts are currently available:

- **test_cran.py**: 

    Script that allows obtaining the data from the CRAN packages and exporting them to a pickle file.
    
- **test_pypi.py**: 

    Script that allows to obtain the data of the PyPI packages and export them to a pickle file.