'''

## Description


This package is responsible for providing a base data structure for all the derivated classes whose purpose is the obtaining data from a specific source.

It is composed of several modules:

##### Package structure:

```data_source
├── csv_ds.py
├── data_source.py
├── librariesio_ds.py
├── repository_scrapers
│   ├── bioconductor.py
│   ├── cran.py
│   ├── npm.py
│   ├── pypi.py
│   └── r.py
└── scraper_ds.py
```

##### Package modules:

- **data_source.py**

  Implements the abstract class Datasource, which is the base class of the rest of the implementations

- **csv_ds.py**

  Implement datasource for \*.csv files

- **librariesio_ds.py**

  Implements datasource for the API of Libraries.io

- **scraper_ds.py**

  Implements the abstract class ScraperDataSource, which is the base class of customized implementations for each repository

- **repository_scraper/**

  Inside there are several implementations based on Datasource web Scraping for Cran, Bioconductor, NPM and PyPI

##### Doc pages

For more info see [data_source package docs](https://dab0012.github.io/olivia-finder/olivia_finder/data_source/data_source_module.html)



## Web Scraping-Based implementations


### Constructor


- The default constructor does not receive parameters

- The number of optional parameters depends on the implementation, but as a rule we can define a name and a description (With the purpose of offering information)

- The most relevant parameter is the RequestHandler object, which will use by the webscraping based DataSource to make requests to the website to which it refers


Implementation for CRAN



```python
from olivia_finder.data_source.repository_scrapers.cran import CranScraper
cran_ds = CranScraper()
```

Implementation for Bioconductor



```python
from olivia_finder.data_source.repository_scrapers.bioconductor import BioconductorScraper
bioconductor_scraper = BioconductorScraper()
```

Implementation for PyPi



```python
from olivia_finder.data_source.repository_scrapers.pypi import PypiScraper
pypi_scraper = PypiScraper()
```

Implementation for NPM



```python
from olivia_finder.data_source.repository_scrapers.npm import NpmScraper
npm_scraper = NpmScraper()
```

Github repository implementation


```python
from olivia_finder.data_source.repository_scrapers.github import GithubScraper
github_scraper = GithubScraper()
```

### Obtain package names


CRAN package names



```python
cran_ds.obtain_package_names()[:10]
```




    ['A3',
     'AalenJohansen',
     'AATtools',
     'ABACUS',
     'abbreviate',
     'abbyyR',
     'abc',
     'abc.data',
     'ABC.RAP',
     'ABCanalysis']



Bioconductor package names



```python
bioconductor_scraper.obtain_package_names()[:10]
```




    ['ABSSeq',
     'ABarray',
     'ACE',
     'ACME',
     'ADAM',
     'ADAMgui',
     'ADImpute',
     'ADaCGH2',
     'AGDEX',
     'AHMassBank']



PyPi package names



```python
pypi_scraper.obtain_package_names()[:10]
```




    ['0',
     '0-._.-._.-._.-._.-._.-._.-0',
     '000',
     '0.0.1',
     '00101s',
     '00print_lol',
     '00SMALINUX',
     '0101',
     '01changer',
     '01d61084-d29e-11e9-96d1-7c5cf84ffe8e']



NPM package names

<span style="color: red">Note:</span>

- This process is very expensive, the implementation is functional but its use is not recommended unless it is necessary
- It is recommended to import the list of npm packets properctioned as a txt file

Output folder can be configured in `config.ini` file `working_dir`



```python
# npm_scraper.obtain_package_names(
#     page_size=100,                          # Number of packages to obtain per request
#     save_chunks=True,                       # Save packages in a chunk file
#     show_progress_bar=True                  # Show progress bar
# )[:10]
```

The file with the NPM package list is the following



```python
!wc -l ../results/package_lists/npm_packages.txt
```

    wc: ../results/package_lists/npm_packages.txt: No existe el archivo o el directorio



```python
!tail -n 20 results/package_lists/npm_packages.txt
```

    tail: no se puede abrir 'results/package_lists/npm_packages.txt' para lectura: No existe el archivo o el directorio


### Obtain package data


CRAN data of A3 package



```python
cran_ds.obtain_package_data('A3')
```




    {'name': 'A3',
     'version': '1.0.0',
     'dependencies': [{'name': 'R', 'version': '≥ 2.15.0'},
      {'name': 'xtable', 'version': ''},
      {'name': 'pbapply', 'version': ''}],
     'url': 'https://cran.r-project.org/package=A3'}



If the petition fails we will obtain None



```python
non_existent_package = cran_ds.obtain_package_data('NON_EXISTENT_PACKAGE')
print(non_existent_package)
```

    None


Bioconductor data of a4 package



```python
bioconductor_scraper.obtain_package_data('a4')
```




    {'name': 'a4',
     'version': '1.48.0',
     'dependencies': [{'name': 'a4Base', 'version': ''},
      {'name': 'a4Preproc', 'version': ''},
      {'name': 'a4Classif', 'version': ''},
      {'name': 'a4Core', 'version': ''},
      {'name': 'a4Reporting', 'version': ''}],
     'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4.html'}



PyPi data od networkx package



```python
pypi_scraper.obtain_package_data('networkx')
```




    {'name': 'networkx',
     'version': '3.1',
     'url': 'https://pypi.org/project/networkx/',
     'dependencies': [{'name': 'numpy', 'version': None},
      {'name': 'scipy', 'version': None},
      {'name': 'matplotlib', 'version': None},
      {'name': 'pandas', 'version': None},
      {'name': 'pre', 'version': None},
      {'name': 'mypy', 'version': None},
      {'name': 'sphinx', 'version': None},
      {'name': 'pydata', 'version': None},
      {'name': 'numpydoc', 'version': None},
      {'name': 'pillow', 'version': None},
      {'name': 'nb2plots', 'version': None},
      {'name': 'texext', 'version': None},
      {'name': 'lxml', 'version': None},
      {'name': 'pygraphviz', 'version': None},
      {'name': 'pydot', 'version': None},
      {'name': 'sympy', 'version': None},
      {'name': 'pytest', 'version': None},
      {'name': 'codecov', 'version': None}]}



NPM data of aws-sdk package



```python
npm_scraper.obtain_package_data('aws-sdk')
```




    {'name': 'aws-sdk',
     'version': '2.1406.0',
     'dependencies': [{'name': 'buffer', 'version': '4.9.2'},
      {'name': 'events', 'version': '1.1.1'},
      {'name': 'ieee754', 'version': '1.1.13'},
      {'name': 'jmespath', 'version': '0.16.0'},
      {'name': 'querystring', 'version': '0.2.0'},
      {'name': 'sax', 'version': '1.2.1'},
      {'name': 'url', 'version': '0.10.3'},
      {'name': 'util', 'version': '^0.12.4'},
      {'name': 'uuid', 'version': '8.0.0'},
      {'name': 'xml2js', 'version': '0.5.0'},
      {'name': '@types/node', 'version': '6.0.92'},
      {'name': 'browserify', 'version': '13.1.0'},
      {'name': 'chai', 'version': '^3.0'},
      {'name': 'codecov', 'version': '^3.8.2'},
      {'name': 'coffeeify', 'version': '*'},
      {'name': 'coffeescript', 'version': '^1.12.7'},
      {'name': 'cucumber', 'version': '0.5.x'},
      {'name': 'eslint', 'version': '^5.8.0'},
      {'name': 'hash-test-vectors', 'version': '^1.3.2'},
      {'name': 'insert-module-globals', 'version': '^7.0.0'},
      {'name': 'istanbul', 'version': '*'},
      {'name': 'jasmine', 'version': '^2.5.3'},
      {'name': 'jasmine-core', 'version': '^2.5.2'},
      {'name': 'json-loader', 'version': '^0.5.4'},
      {'name': 'karma', 'version': '^4.1.0'},
      {'name': 'karma-chrome-launcher', 'version': '2.2.0'},
      {'name': 'karma-jasmine', 'version': '^1.1.0'},
      {'name': 'mocha', 'version': '^3.0.0'},
      {'name': 'repl.history', 'version': '*'},
      {'name': 'semver', 'version': '*'},
      {'name': 'typescript', 'version': '2.0.8'},
      {'name': 'uglify-js', 'version': '2.x'},
      {'name': 'webpack', 'version': '^1.15.0'}],
     'url': 'https://www.npmjs.com/package/aws-sdk'}



### Obtain a list of packages data


CRAN data for the packages A3, AER y a non existent package



```python
cran_ds.obtain_packages_data(['A3', 'AER', "NON_EXISTING_PACKAGE"])
```




    ([{'name': 'A3',
       'version': '1.0.0',
       'dependencies': [{'name': 'R', 'version': '≥ 2.15.0'},
        {'name': 'xtable', 'version': ''},
        {'name': 'pbapply', 'version': ''}],
       'url': 'https://cran.r-project.org/package=A3'},
      {'name': 'AER',
       'version': '1.2-10',
       'dependencies': [{'name': 'R', 'version': '≥ 3.0.0'},
        {'name': 'car', 'version': '≥ 2.0-19'},
        {'name': 'lmtest', 'version': ''},
        {'name': 'sandwich', 'version': '≥ 2.4-0'},
        {'name': 'survival', 'version': '≥ 2.37-5'},
        {'name': 'zoo', 'version': ''},
        {'name': 'stats', 'version': ''},
        {'name': 'Formula', 'version': '≥ 0.2-0'}],
       'url': 'https://cran.r-project.org/package=AER'}],
     ['NON_EXISTING_PACKAGE'])



Bioconductor data for the packages TDARACNE, ASICS and a non existent package



```python
from tqdm import tqdm

bioconductor_scraper.obtain_packages_data(
    package_names=['a4', 'a4Preproc', 'a4Classif', 'a4Core', 'a4Base'],
    progress_bar=tqdm(total=5)
)
```

    100%|██████████| 5/5 [00:00<00:00,  5.79it/s]





    ([{'name': 'a4',
       'version': '1.48.0',
       'dependencies': [{'name': 'a4Base', 'version': ''},
        {'name': 'a4Preproc', 'version': ''},
        {'name': 'a4Classif', 'version': ''},
        {'name': 'a4Core', 'version': ''},
        {'name': 'a4Reporting', 'version': ''}],
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4.html'},
      {'name': 'a4Preproc',
       'version': '1.48.0',
       'dependencies': [{'name': 'BiocGenerics', 'version': ''},
        {'name': 'Biobase', 'version': ''}],
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4Preproc.html'},
      {'name': 'a4Classif',
       'version': '1.48.0',
       'dependencies': [{'name': 'a4Core', 'version': ''},
        {'name': 'a4Preproc', 'version': ''},
        {'name': 'methods', 'version': ''},
        {'name': 'Biobase', 'version': ''},
        {'name': 'ROCR', 'version': ''},
        {'name': 'pamr', 'version': ''},
        {'name': 'glmnet', 'version': ''},
        {'name': 'varSelRF', 'version': ''},
        {'name': 'utils', 'version': ''},
        {'name': 'graphics', 'version': ''},
        {'name': 'stats', 'version': ''}],
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4Classif.html'},
      {'name': 'a4Core',
       'version': '1.48.0',
       'dependencies': [{'name': 'Biobase', 'version': ''},
        {'name': 'glmnet', 'version': ''},
        {'name': 'methods', 'version': ''},
        {'name': 'stats', 'version': ''}],
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4Core.html'},
      {'name': 'a4Base',
       'version': '1.48.0',
       'dependencies': [{'name': 'a4Preproc', 'version': ''},
        {'name': 'a4Core', 'version': ''},
        {'name': 'methods', 'version': ''},
        {'name': 'graphics', 'version': ''},
        {'name': 'grid', 'version': ''},
        {'name': 'Biobase', 'version': ''},
        {'name': 'annaffy', 'version': ''},
        {'name': 'mpm', 'version': ''},
        {'name': 'genefilter', 'version': ''},
        {'name': 'limma', 'version': ''},
        {'name': 'multtest', 'version': ''},
        {'name': 'glmnet', 'version': ''},
        {'name': 'gplots', 'version': ''}],
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/a4Base.html'}],
     [])




```python
pypi_scraper.obtain_packages_data(
    ['networkx', 'requests', "tqdm", "NON_EXISTING_PACKAGE"])
```




    ([{'name': 'networkx',
       'version': '3.1',
       'url': 'https://pypi.org/project/networkx/',
       'dependencies': [{'name': 'numpy', 'version': None},
        {'name': 'scipy', 'version': None},
        {'name': 'matplotlib', 'version': None},
        {'name': 'pandas', 'version': None},
        {'name': 'pre', 'version': None},
        {'name': 'mypy', 'version': None},
        {'name': 'sphinx', 'version': None},
        {'name': 'pydata', 'version': None},
        {'name': 'numpydoc', 'version': None},
        {'name': 'pillow', 'version': None},
        {'name': 'nb2plots', 'version': None},
        {'name': 'texext', 'version': None},
        {'name': 'lxml', 'version': None},
        {'name': 'pygraphviz', 'version': None},
        {'name': 'pydot', 'version': None},
        {'name': 'sympy', 'version': None},
        {'name': 'pytest', 'version': None},
        {'name': 'codecov', 'version': None}]},
      {'name': 'requests',
       'version': '2.31.0',
       'url': 'https://pypi.org/project/requests/',
       'dependencies': [{'name': 'charset', 'version': None},
        {'name': 'idna', 'version': None},
        {'name': 'urllib3', 'version': None},
        {'name': 'certifi', 'version': None},
        {'name': 'PySocks', 'version': None},
        {'name': 'chardet', 'version': None}]},
      {'name': 'tqdm',
       'version': '4.65.0',
       'url': 'https://pypi.org/project/tqdm/',
       'dependencies': [{'name': 'colorama', 'version': None},
        {'name': 'py', 'version': None},
        {'name': 'twine', 'version': None},
        {'name': 'wheel', 'version': None},
        {'name': 'ipywidgets', 'version': None},
        {'name': 'slack', 'version': None},
        {'name': 'requests', 'version': None}]}],
     ['NON_EXISTING_PACKAGE'])




```python
npm_scraper.obtain_packages_data(
    ['aws-sdk', 'request', "NON_EXISTING_PACKAGE"])
```




    ([{'name': 'aws-sdk',
       'version': '2.1406.0',
       'dependencies': [{'name': 'buffer', 'version': '4.9.2'},
        {'name': 'events', 'version': '1.1.1'},
        {'name': 'ieee754', 'version': '1.1.13'},
        {'name': 'jmespath', 'version': '0.16.0'},
        {'name': 'querystring', 'version': '0.2.0'},
        {'name': 'sax', 'version': '1.2.1'},
        {'name': 'url', 'version': '0.10.3'},
        {'name': 'util', 'version': '^0.12.4'},
        {'name': 'uuid', 'version': '8.0.0'},
        {'name': 'xml2js', 'version': '0.5.0'},
        {'name': '@types/node', 'version': '6.0.92'},
        {'name': 'browserify', 'version': '13.1.0'},
        {'name': 'chai', 'version': '^3.0'},
        {'name': 'codecov', 'version': '^3.8.2'},
        {'name': 'coffeeify', 'version': '*'},
        {'name': 'coffeescript', 'version': '^1.12.7'},
        {'name': 'cucumber', 'version': '0.5.x'},
        {'name': 'eslint', 'version': '^5.8.0'},
        {'name': 'hash-test-vectors', 'version': '^1.3.2'},
        {'name': 'insert-module-globals', 'version': '^7.0.0'},
        {'name': 'istanbul', 'version': '*'},
        {'name': 'jasmine', 'version': '^2.5.3'},
        {'name': 'jasmine-core', 'version': '^2.5.2'},
        {'name': 'json-loader', 'version': '^0.5.4'},
        {'name': 'karma', 'version': '^4.1.0'},
        {'name': 'karma-chrome-launcher', 'version': '2.2.0'},
        {'name': 'karma-jasmine', 'version': '^1.1.0'},
        {'name': 'mocha', 'version': '^3.0.0'},
        {'name': 'repl.history', 'version': '*'},
        {'name': 'semver', 'version': '*'},
        {'name': 'typescript', 'version': '2.0.8'},
        {'name': 'uglify-js', 'version': '2.x'},
        {'name': 'webpack', 'version': '^1.15.0'}],
       'url': 'https://www.npmjs.com/package/aws-sdk'},
      {'name': 'request',
       'version': '2.88.2',
       'dependencies': [{'name': 'aws-sign2', 'version': '~0.7.0'},
        {'name': 'aws4', 'version': '^1.8.0'},
        {'name': 'caseless', 'version': '~0.12.0'},
        {'name': 'combined-stream', 'version': '~1.0.6'},
        {'name': 'extend', 'version': '~3.0.2'},
        {'name': 'forever-agent', 'version': '~0.6.1'},
        {'name': 'form-data', 'version': '~2.3.2'},
        {'name': 'har-validator', 'version': '~5.1.3'},
        {'name': 'http-signature', 'version': '~1.2.0'},
        {'name': 'is-typedarray', 'version': '~1.0.0'},
        {'name': 'isstream', 'version': '~0.1.2'},
        {'name': 'json-stringify-safe', 'version': '~5.0.1'},
        {'name': 'mime-types', 'version': '~2.1.19'},
        {'name': 'oauth-sign', 'version': '~0.9.0'},
        {'name': 'performance-now', 'version': '^2.1.0'},
        {'name': 'qs', 'version': '~6.5.2'},
        {'name': 'safe-buffer', 'version': '^5.1.2'},
        {'name': 'tough-cookie', 'version': '~2.5.0'},
        {'name': 'tunnel-agent', 'version': '^0.6.0'},
        {'name': 'uuid', 'version': '^3.3.2'},
        {'name': 'bluebird', 'version': '^3.2.1'},
        {'name': 'browserify', 'version': '^13.0.1'},
        {'name': 'browserify-istanbul', 'version': '^2.0.0'},
        {'name': 'buffer-equal', 'version': '^1.0.0'},
        {'name': 'codecov', 'version': '^3.0.4'},
        {'name': 'coveralls', 'version': '^3.0.2'},
        {'name': 'function-bind', 'version': '^1.0.2'},
        {'name': 'karma', 'version': '^3.0.0'},
        {'name': 'karma-browserify', 'version': '^5.0.1'},
        {'name': 'karma-cli', 'version': '^1.0.0'},
        {'name': 'karma-coverage', 'version': '^1.0.0'},
        {'name': 'karma-phantomjs-launcher', 'version': '^1.0.0'},
        {'name': 'karma-tap', 'version': '^3.0.1'},
        {'name': 'nyc', 'version': '^14.1.1'},
        {'name': 'phantomjs-prebuilt', 'version': '^2.1.3'},
        {'name': 'rimraf', 'version': '^2.2.8'},
        {'name': 'server-destroy', 'version': '^1.0.1'},
        {'name': 'standard', 'version': '^9.0.0'},
        {'name': 'tape', 'version': '^4.6.0'},
        {'name': 'taper', 'version': '^0.5.0'}],
       'url': 'https://www.npmjs.com/package/request'}],
     ['NON_EXISTING_PACKAGE'])



## CSV-Based implementation


### Constructor



```python
from olivia_finder.data_source.csv_ds import CSVDataSource
bioconductor_csv = CSVDataSource(
    "aux_data/bioconductor_adjlist_test.csv",   # Path to the CSV file
    # Name of the field that contains the dependencies
    dependent_field="name",
    # Name of the field that contains the name of the package
    dependency_field="dependency",
    # Name of the field that contains the version of the package
    dependent_version_field="version",
    # Name of the field that contains the version of the dependency
    dependency_version_field="dependency_version",
    # Name of the field that contains the URL of the package
    dependent_url_field="url",
)
```

### Obtain package data



```python
bioconductor_csv.obtain_package_data('BANDITS')
```




    {'name': 'BANDITS',
     'version': '1.16.0',
     'url': 'https://www.bioconductor.org/packages/release/bioc/html/BANDITS.html',
     'dependencies': [{'name': 'R', 'version': nan},
      {'name': 'Rcpp', 'version': nan},
      {'name': 'doRNG', 'version': nan},
      {'name': 'MASS', 'version': nan},
      {'name': 'data.table', 'version': nan},
      {'name': 'R.utils', 'version': nan},
      {'name': 'doParallel', 'version': nan},
      {'name': 'parallel', 'version': nan},
      {'name': 'foreach', 'version': nan},
      {'name': 'methods', 'version': nan},
      {'name': 'stats', 'version': nan},
      {'name': 'graphics', 'version': nan},
      {'name': 'ggplot2', 'version': nan},
      {'name': 'DRIMSeq', 'version': '1.28.0'},
      {'name': 'BiocParallel', 'version': '1.34.0'}]}



### Obtain a list of packages data



```python
bioconductor_csv.obtain_packages_data(
    ['BANDITS', 'ASICS', "NON_EXISTING_PACKAGE"])
```




    ([{'name': 'BANDITS',
       'version': '1.16.0',
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/BANDITS.html',
       'dependencies': [{'name': 'R', 'version': nan},
        {'name': 'Rcpp', 'version': nan},
        {'name': 'doRNG', 'version': nan},
        {'name': 'MASS', 'version': nan},
        {'name': 'data.table', 'version': nan},
        {'name': 'R.utils', 'version': nan},
        {'name': 'doParallel', 'version': nan},
        {'name': 'parallel', 'version': nan},
        {'name': 'foreach', 'version': nan},
        {'name': 'methods', 'version': nan},
        {'name': 'stats', 'version': nan},
        {'name': 'graphics', 'version': nan},
        {'name': 'ggplot2', 'version': nan},
        {'name': 'DRIMSeq', 'version': '1.28.0'},
        {'name': 'BiocParallel', 'version': '1.34.0'}]},
      {'name': 'ASICS',
       'version': '2.16.0',
       'url': 'https://www.bioconductor.org/packages/release/bioc/html/ASICS.html',
       'dependencies': [{'name': 'R', 'version': nan},
        {'name': 'BiocParallel', 'version': '1.34.0'},
        {'name': 'ggplot2', 'version': nan},
        {'name': 'glmnet', 'version': nan},
        {'name': 'grDevices', 'version': nan},
        {'name': 'gridExtra', 'version': nan},
        {'name': 'methods', 'version': nan},
        {'name': 'mvtnorm', 'version': nan},
        {'name': 'PepsNMR', 'version': '1.18.0'},
        {'name': 'plyr', 'version': nan},
        {'name': 'quadprog', 'version': nan},
        {'name': 'ropls', 'version': '1.32.0'},
        {'name': 'stats', 'version': nan},
        {'name': 'SummarizedExperiment', 'version': '1.30.0'},
        {'name': 'utils', 'version': nan},
        {'name': 'Matrix', 'version': nan},
        {'name': 'zoo', 'version': nan}]}],
     ['NON_EXISTING_PACKAGE'])



## Web API-Based implementation (Libraries.io API)


Based on the Web API of Libraries.io we can obtain data from this source.

It is important to note that the data is not updated as a mandatory point to care about


### Constructor


In this case, it is necessary to define the API Key of Libraries.io in the _config.ini_ file



```python
from olivia_finder.data_source.librariesio_ds import LibrariesioDataSource

pypi_libio  = LibrariesioDataSource(platform="pypi")
nuget_libio = LibrariesioDataSource(platform="nuget")
cran_libio  = LibrariesioDataSource(platform="cran")
```

### Obtain package names


<p style="color:red">
This functionality has not been implemented because there is no way to get this data through the API
</p>


The library used to access API from Python has a search functionality but unfortunately it cannot be used efficiently for this task



```python
# Set the apikey as an environment variable
from pybraries.search import Search

search = Search()
info = search.project_search(platform='pypi')

for project in info:
    print(project['name'])
```

    A string of keywords must be passed as a keyword argument
    typescript
    @types/node
    eslint
    webpack
    prettier
    @types/jest
    @types/react
    @babel/preset-typescript
    @babel/runtime
    jest
    rxjs
    postcss
    vue-template-compiler
    vue
    axios
    requests
    moment
    @types/react-dom
    @types/mocha
    babel-runtime
    babel-preset-react
    @babel/core
    babel-core
    @babel/preset-env
    @babel/plugin-proposal-class-properties
    @babel/plugin-transform-runtime
    @babel/preset-react
    babel-jest
    commander
    rollup


### Obtain package data



```python
pypi_libio.obtain_package_data('networkx')
```




    {'name': 'networkx',
     'version': '3.1rc0',
     'dependencies': [{'name': 'codecov', 'version': '2.1.13'},
      {'name': 'pytest-cov', 'version': '4.0.0'},
      {'name': 'pytest', 'version': '7.4.0'},
      {'name': 'sympy', 'version': '1.11.1'},
      {'name': 'pydot', 'version': '0.9.10'},
      {'name': 'pygraphviz', 'version': '1.3.1'},
      {'name': 'lxml', 'version': '4.9.2'},
      {'name': 'texext', 'version': '0.6.7'},
      {'name': 'nb2plots', 'version': '0.6.1'},
      {'name': 'pillow', 'version': '9.5.0'},
      {'name': 'numpydoc', 'version': '1.5.0'},
      {'name': 'sphinx-gallery', 'version': '0.13.0'},
      {'name': 'pydata-sphinx-theme', 'version': '0.13.3'},
      {'name': 'sphinx', 'version': '7.0.1'},
      {'name': 'mypy', 'version': '1.4.1'},
      {'name': 'pre-commit', 'version': '3.3.3'},
      {'name': 'pandas', 'version': '2.0.1'},
      {'name': 'matplotlib', 'version': '3.7.1'},
      {'name': 'scipy', 'version': '1.11.0'},
      {'name': 'numpy', 'version': '1.25.0'}],
     'url': 'https://pypi.org/project/networkx/'}




```python
nuget_libio.obtain_package_data('Microsoft.Extensions.DependencyInjection')
```




    {'name': 'Microsoft.Extensions.DependencyInjection',
     'version': '8.0.0-preview.5.23280.8',
     'dependencies': [{'name': 'System.Threading.Tasks.Extensions',
       'version': '4.5.4'},
      {'name': 'Microsoft.Extensions.DependencyInjection.Abstractions',
       'version': '3.1.32'},
      {'name': 'Microsoft.Bcl.AsyncInterfaces', 'version': '7.0.0'}],
     'url': 'https://www.nuget.org/packages/Microsoft.Extensions.DependencyInjection/'}



### Obtain a list of packages data



```python
cran_libio.obtain_packages_data(['A3', 'AER', "NON_EXISTING_PACKAGE"])
```




    [{'name': 'A3',
      'version': '1.0.0',
      'dependencies': [{'name': 'R', 'version': None},
       {'name': 'randomForest', 'version': None}],
      'url': 'https://cran.r-project.org/package=A3'},
     {'name': 'AER',
      'version': '1.2-9',
      'dependencies': [{'name': 'vars', 'version': '0.5.3'},
       {'name': 'urca', 'version': None},
       {'name': 'tseries', 'version': None},
       {'name': 'truncreg', 'version': None},
       {'name': 'systemfit', 'version': None},
       {'name': 'strucchange', 'version': None},
       {'name': 'scatterplot3d', 'version': '0.3.4'},
       {'name': 'sampleSelection', 'version': None},
       {'name': 'rugarch', 'version': None},
       {'name': 'ROCR', 'version': None},
       {'name': 'rgl', 'version': '0.109.2'},
       {'name': 'quantreg', 'version': '5.42.1'},
       {'name': 'pscl', 'version': '1.5.5'},
       {'name': 'plm', 'version': None},
       {'name': 'np', 'version': None},
       {'name': 'nnet', 'version': None},
       {'name': 'nlme', 'version': None},
       {'name': 'mlogit', 'version': None},
       {'name': 'MASS', 'version': None},
       {'name': 'longmemo', 'version': None},
       {'name': 'lattice', 'version': None},
       {'name': 'KernSmooth', 'version': None},
       {'name': 'ineq', 'version': None},
       {'name': 'foreign', 'version': None},
       {'name': 'forecast', 'version': '8.17.0'},
       {'name': 'fGarch', 'version': '3042.83.2'},
       {'name': 'effects', 'version': None},
       {'name': 'dynlm', 'version': None},
       {'name': 'boot', 'version': None},
       {'name': 'Formula', 'version': None},
       {'name': 'stats', 'version': None},
       {'name': 'zoo', 'version': None},
       {'name': 'survival', 'version': None},
       {'name': 'sandwich', 'version': None},
       {'name': 'lmtest', 'version': None},
       {'name': 'car', 'version': None},
       {'name': 'R', 'version': None}],
      'url': 'https://cran.r-project.org/package=AER'}]

'''