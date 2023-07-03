'''

## Initialize a package manager


**Note:**

Initialization based on a scraper-type datasource involves initializing the data prior to its use.

Initialization based on a CSV-type datasource already contains all the data and can be retrieved directly.

Loading from a persistence file implies that the file contains an object that has already been initialized or already contains data.

A bioconductor scraping based package manager


```python
from olivia_finder.package_manager import PackageManager
```


```python
bioconductor_pm_scraper = PackageManager(
    data_sources=[                  # List of data sources
        BioconductorScraper(),
    ]
)
```

A cran package manager loaded from a csv file


```python
cran_pm_csv = PackageManager(
    data_sources=[                  # List of data sources
        CSVDataSource(
            # Path to the CSV file
            "aux_data/cran_adjlist_test.csv",
            dependent_field="Project Name",
            dependency_field="Dependency Name",
            dependent_version_field="Version Number",
        )
    ]
)

# Is needed to initialize the package manager to fill the package list with the csv data
cran_pm_csv.initialize(show_progress=True)
```

    Loading packages: 100%|[32m██████████[0m| 275/275 [00:00<00:00, 729.91packages/s]


A pypi package manager loaded from persistence file


```python
bioconductor_pm_loaded = PackageManager.load_from_persistence("../results/package_managers/bioconductor_scraper.olvpm")
```

A Maven package manager loaded from librariesio api


```python
maven_pm_libio = PackageManager(
    data_sources=[                  # List of data sources
        LibrariesioDataSource(platform="maven")
    ]
)
```

**For scraping-based datasources: Initialize the structure with the data of the selected sources**


<span style="color:red">Note:</span>

The automatic obtaining of bioconductor packages as mentioned above depends on Selenium, which requires a pre-installed browser in the system, in our case Firefox.

It is possible that if you are running this notebook from a third-party Jupyter server, do not have a browser available

As a solution to this problem it is proposed to use the package_names parameter, in this way we can add a list of packages and the process can be continued


```python
# bioconductor_pm_scraper.initialize(show_progress=True)
```

Note: If we do not provide a list of packages it will be obtained automatically if that functionality is implemented in datasource

Initialization of the bioconductor package manager using package list


```python
# Initialize the package list
bioconductor_package_list = []
with open('../results/package_lists/bioconductor_scraped.txt', 'r') as file:
    bioconductor_package_list = file.read().splitlines()

# Initialize the package manager with the package list
bioconductor_pm_scraper.initialize(show_progress=True, package_names=bioconductor_package_list[:10])
```

    Loading packages: 100%|[32m██████████[0m| 10/10 [00:06<00:00,  1.43packages/s]


Initialization of the Pypi package manager



```python
pypi_pm_scraper = PackageManager(
    data_sources=[                  # List of data sources
        PypiScraper(),
    ]
)

pypi_package_list = []
with open('../results/package_lists/pypi_scraped.txt', 'r') as file:
    pypi_package_list = file.read().splitlines()

# Initialize the package manager
pypi_pm_scraper.initialize(show_progress=True, package_names=pypi_package_list[:10])

# Save the package manager
pypi_pm_scraper.save(path="aux_data/pypi_pm_scraper_test.olvpm")
```

    Loading packages: 100%|[32m██████████[0m| 10/10 [00:01<00:00,  6.75packages/s]


Initialization of the npm package manager


```python
# Initialize the package manager
npm_package_list = []
with open('../results/package_lists/npm_scraped.txt', 'r') as file:
    npm_package_list = file.read().splitlines()

npm_pm_scraper = PackageManager(
    data_sources=[                  # List of data sources
        NpmScraper(),
    ]
)

# Initialize the package manager
npm_pm_scraper.initialize(show_progress=True, package_names=npm_package_list[:10])

# Save the package manager
npm_pm_scraper.save(path="aux_data/npm_pm_scraper_test.olvpm")
```

    Loading packages: 100%|[32m██████████[0m| 10/10 [00:02<00:00,  3.88packages/s]


And using a csv based package manager


```python
cran_pm_csv.initialize(show_progress=True)
```

    Loading packages: 100%|[32m██████████[0m| 275/275 [00:00<00:00, 675.72packages/s]


## Persistence


**Save the package manager**



```python
pypi_pm_scraper.save("aux_data/pypi_scraper_pm_saved.olvpm")
```

**Load package manager from persistence file**



```python
from olivia_finder.package_manager import PackageManager
```


```python
bioconductor_pm_loaded = PackageManager.load_from_persistence("../results/package_managers/bioconductor_scraper.olvpm")
```


```python
cran_pm_loaded = PackageManager.load_from_persistence("../results/package_managers/cran_scraper.olvpm")
```


```python
pypi_pm_loaded = PackageManager.load_from_persistence("../results/package_managers/pypi_scraper.olvpm")
```


```python
npm_pm_loaded = PackageManager.load_from_persistence("../results/package_managers/npm_scraper.olvpm")
```

## Package manager functionalities


**List package names**



```python
bioconductor_pm_loaded.package_names()[300:320]
```


    ['CNVgears',
     'CONSTANd',
     'CTSV',
     'CellNOptR',
     'ChAMP',
     'ChIPseqR',
     'CiteFuse',
     'Clonality',
     'CopyNumberPlots',
     'CytoGLMM',
     'DEFormats',
     'DEScan2',
     'DEsingle',
     'DMRcaller',
     'DOSE',
     'DSS',
     'DelayedMatrixStats',
     'DirichletMultinomial',
     'EBImage',
     'EDASeq']




```python
pypi_pm_loaded.package_names()[300:320]
```




    ['adafruit-circuitpython-bh1750',
     'adafruit-circuitpython-ble-beacon',
     'adafruit-circuitpython-ble-eddystone',
     'adafruit-circuitpython-bluefruitspi',
     'adafruit-circuitpython-bno08x',
     'adafruit-circuitpython-circuitplayground',
     'adafruit-circuitpython-debug-i2c',
     'adafruit-circuitpython-displayio-ssd1306',
     'adafruit-circuitpython-ds18x20',
     'adafruit-circuitpython-ens160',
     'adafruit-circuitpython-fingerprint',
     'adafruit-circuitpython-gc-iot-core',
     'adafruit-circuitpython-hcsr04',
     'adafruit-circuitpython-htu31d',
     'adafruit-circuitpython-imageload',
     'adafruit-circuitpython-itertools',
     'adafruit-circuitpython-lis2mdl',
     'adafruit-circuitpython-lps2x',
     'adafruit-circuitpython-lsm9ds0',
     'adafruit-circuitpython-max31855']



<span style="color: red"> Obtaining package names from libraries io api is not suported</span>


```python
maven_pm_libio.package_names()
```




    []



**Get the data as a dict usung datasource**


```python
maven_pm_libio.fetch_package("org.apache.commons:commons-lang3").to_dict()
```




    {'name': 'org.apache.commons:commons-lang3',
     'version': '3.9',
     'url': 'https://repo1.maven.org/maven2/org/apache/commons/commons-lang3',
     'dependencies': [{'name': 'org.openjdk.jmh:jmh-generator-annprocess',
       'version': '1.25.2',
       'url': None,
       'dependencies': []},
      {'name': 'org.openjdk.jmh:jmh-core',
       'version': '1.25.2',
       'url': None,
       'dependencies': []},
      {'name': 'org.easymock:easymock',
       'version': '5.1.0',
       'url': None,
       'dependencies': []},
      {'name': 'org.hamcrest:hamcrest',
       'version': None,
       'url': None,
       'dependencies': []},
      {'name': 'org.junit-pioneer:junit-pioneer',
       'version': '2.0.1',
       'url': None,
       'dependencies': []},
      {'name': 'org.junit.jupiter:junit-jupiter',
       'version': '5.9.3',
       'url': None,
       'dependencies': []}]}




```python
cran_pm_csv.get_package('nmfem').to_dict()
```




    {'name': 'nmfem',
     'version': '1.0.4',
     'url': None,
     'dependencies': [{'name': 'rmarkdown',
       'version': None,
       'url': None,
       'dependencies': []},
      {'name': 'testthat', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'knitr', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'tidyr', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'mixtools', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'd3heatmap', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'dplyr', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'plyr', 'version': None, 'url': None, 'dependencies': []},
      {'name': 'R', 'version': None, 'url': None, 'dependencies': []}]}



**Get a package from self data**


```python
cran_pm_loaded.get_package('A3')
```




    <olivia_finder.package.Package at 0x7f3c3722fe20>




```python
npm_pm_loaded.get_package("react").to_dict()
```




    {'name': 'react',
     'version': '18.2.0',
     'url': 'https://www.npmjs.com/package/react',
     'dependencies': [{'name': 'loose-envify',
       'version': '^1.1.0',
       'url': None,
       'dependencies': []}]}



**List package objects**



```python
len(npm_pm_loaded.package_names())
```




    1919072




```python
pypi_pm_loaded.get_packages()[300:320]
```




    [<olivia_finder.package.Package at 0x7f3c58ea7ac0>,
     <olivia_finder.package.Package at 0x7f3c58ea7be0>,
     <olivia_finder.package.Package at 0x7f3c58ea7d00>,
     <olivia_finder.package.Package at 0x7f3c58ea7e20>,
     <olivia_finder.package.Package at 0x7f3c58ea7f40>,
     <olivia_finder.package.Package at 0x7f3c590e80a0>,
     <olivia_finder.package.Package at 0x7f3c590e81c0>,
     <olivia_finder.package.Package at 0x7f3c590e82e0>,
     <olivia_finder.package.Package at 0x7f3c590e83a0>,
     <olivia_finder.package.Package at 0x7f3c590e8520>,
     <olivia_finder.package.Package at 0x7f3c590e86a0>,
     <olivia_finder.package.Package at 0x7f3c590e87c0>,
     <olivia_finder.package.Package at 0x7f3c590e88e0>,
     <olivia_finder.package.Package at 0x7f3c590e89a0>,
     <olivia_finder.package.Package at 0x7f3c590e8b20>,
     <olivia_finder.package.Package at 0x7f3c590e8c40>,
     <olivia_finder.package.Package at 0x7f3c590e8d00>,
     <olivia_finder.package.Package at 0x7f3c590e8e80>,
     <olivia_finder.package.Package at 0x7f3c590e8fa0>,
     <olivia_finder.package.Package at 0x7f3c590e90c0>]



**Obtain dependency networks**

Using the data previously obtained and that are already loaded in the structure


```python
a4_network = bioconductor_pm_loaded.fetch_adjlist("a4")
a4_network
```




    {'a4': ['a4Base', 'a4Preproc', 'a4Classif', 'a4Core', 'a4Reporting'],
     'a4Base': ['a4Preproc',
      'a4Core',
      'methods',
      'graphics',
      'grid',
      'Biobase',
      'annaffy',
      'mpm',
      'genefilter',
      'limma',
      'multtest',
      'glmnet',
      'gplots'],
     'a4Preproc': ['BiocGenerics', 'Biobase'],
     'BiocGenerics': ['R', 'methods', 'utils', 'graphics', 'stats'],
     'R': [],
     'methods': [],
     'utils': [],
     'graphics': [],
     'stats': [],
     'Biobase': ['R', 'BiocGenerics', 'utils', 'methods'],
     'a4Core': ['Biobase', 'glmnet', 'methods', 'stats'],
     'glmnet': [],
     'grid': [],
     'annaffy': ['R',
      'methods',
      'Biobase',
      'BiocManager',
      'GO.db',
      'AnnotationDbi',
      'DBI'],
     'BiocManager': [],
     'GO.db': [],
     'AnnotationDbi': ['R',
      'methods',
      'stats4',
      'BiocGenerics',
      'Biobase',
      'IRanges',
      'DBI',
      'RSQLite',
      'S4Vectors',
      'stats',
      'KEGGREST'],
     'stats4': [],
     'IRanges': ['R',
      'methods',
      'utils',
      'stats',
      'BiocGenerics',
      'S4Vectors',
      'stats4'],
     'DBI': [],
     'RSQLite': [],
     'S4Vectors': ['R', 'methods', 'utils', 'stats', 'stats4', 'BiocGenerics'],
     'KEGGREST': ['R', 'methods', 'httr', 'png', 'Biostrings'],
     'mpm': [],
     'genefilter': ['MatrixGenerics',
      'AnnotationDbi',
      'annotate',
      'Biobase',
      'graphics',
      'methods',
      'stats',
      'survival',
      'grDevices'],
     'MatrixGenerics': ['matrixStats', 'methods'],
     'matrixStats': [],
     'annotate': ['R',
      'AnnotationDbi',
      'XML',
      'Biobase',
      'DBI',
      'xtable',
      'graphics',
      'utils',
      'stats',
      'methods',
      'BiocGenerics',
      'httr'],
     'XML': [],
     'xtable': [],
     'httr': [],
     'survival': [],
     'grDevices': [],
     'limma': ['R', 'grDevices', 'graphics', 'stats', 'utils', 'methods'],
     'multtest': ['R',
      'methods',
      'BiocGenerics',
      'Biobase',
      'survival',
      'MASS',
      'stats4'],
     'MASS': [],
     'gplots': [],
     'a4Classif': ['a4Core',
      'a4Preproc',
      'methods',
      'Biobase',
      'ROCR',
      'pamr',
      'glmnet',
      'varSelRF',
      'utils',
      'graphics',
      'stats'],
     'ROCR': [],
     'pamr': [],
     'varSelRF': [],
     'a4Reporting': ['methods', 'xtable']}



Get transitive dependency network graph


```python
commons_lang3_network = maven_pm_libio.get_transitive_network_graph("org.apache.commons:commons-lang3", generate=True)
commons_lang3_network
```




    <networkx.classes.digraph.DiGraph at 0x7f3c67ee3d90>




```python
# Draw the network
from matplotlib import patches
pos = nx.spring_layout(commons_lang3_network)
nx.draw(commons_lang3_network, pos, node_size=50, font_size=8)

nx.draw_networkx_nodes(commons_lang3_network, pos, nodelist=["org.apache.commons:commons-lang3"], node_size=100, node_color="r")
plt.title("org.apache.commons:commons-lang3 transitive network", fontsize=15)
# add legend for red node
red_patch = patches.Patch(color='red', label='org.apache.commons:commons-lang3')
plt.legend(handles=[red_patch])
plt.show()
```


    
![png](Olivia%20Finder%20-%20Implementation_files/Olivia%20Finder%20-%20Implementation_229_0.png)
    


**Obtaining updated data**


```python
a4_network2 = bioconductor_pm_loaded.get_adjlist("a4")
a4_network2
```




    {'a4': ['a4Base', 'a4Preproc', 'a4Classif', 'a4Core', 'a4Reporting'],
     'a4Base': ['a4Preproc',
      'a4Core',
      'methods',
      'graphics',
      'grid',
      'Biobase',
      'annaffy',
      'mpm',
      'genefilter',
      'limma',
      'multtest',
      'glmnet',
      'gplots'],
     'a4Preproc': ['BiocGenerics', 'Biobase'],
     'BiocGenerics': ['R', 'methods', 'utils', 'graphics', 'stats'],
     'Biobase': ['R', 'BiocGenerics', 'utils', 'methods'],
     'a4Core': ['Biobase', 'glmnet', 'methods', 'stats'],
     'annaffy': ['R',
      'methods',
      'Biobase',
      'BiocManager',
      'GO.db',
      'AnnotationDbi',
      'DBI'],
     'AnnotationDbi': ['R',
      'methods',
      'utils',
      'stats4',
      'BiocGenerics',
      'Biobase',
      'IRanges',
      'DBI',
      'RSQLite',
      'S4Vectors',
      'stats',
      'KEGGREST'],
     'IRanges': ['R',
      'methods',
      'utils',
      'stats',
      'BiocGenerics',
      'S4Vectors',
      'stats4'],
     'S4Vectors': ['R', 'methods', 'utils', 'stats', 'stats4', 'BiocGenerics'],
     'KEGGREST': ['R', 'methods', 'httr', 'png', 'Biostrings'],
     'genefilter': ['MatrixGenerics',
      'AnnotationDbi',
      'annotate',
      'Biobase',
      'graphics',
      'methods',
      'stats',
      'survival',
      'grDevices'],
     'MatrixGenerics': ['matrixStats', 'methods'],
     'annotate': ['R',
      'AnnotationDbi',
      'XML',
      'Biobase',
      'DBI',
      'xtable',
      'graphics',
      'utils',
      'stats',
      'methods',
      'BiocGenerics',
      'httr'],
     'limma': ['R', 'grDevices', 'graphics', 'stats', 'utils', 'methods'],
     'multtest': ['R',
      'methods',
      'BiocGenerics',
      'Biobase',
      'survival',
      'MASS',
      'stats4'],
     'a4Classif': ['a4Core',
      'a4Preproc',
      'methods',
      'Biobase',
      'ROCR',
      'pamr',
      'glmnet',
      'varSelRF',
      'utils',
      'graphics',
      'stats'],
     'a4Reporting': ['methods', 'xtable']}



Note that some package managers use dependencies that are not found is their repositories, as is the case of the 'xable' package, which although it is not in bioconductor, is dependence on a bioconductor package


```python
xtable_bioconductor = bioconductor_pm_scraper.fetch_package("xtable")
xtable_bioconductor
```

In concrete this package is in Cran


```python
cran_pm = PackageManager(
    data_sources=[                  # List of data sources
        CranScraper(),
    ]
)

cran_pm.fetch_package("xtable")
```




    <olivia_finder.package.Package at 0x7f3c2a19d090>



To solve this incongruity, we can supply the packet manager the Datasource de Cran, such as auxiliary datasource in which to perform searches if data is not found in the main datasource


```python
bioconductor_cran_pm = PackageManager(
    # Name of the package manager
    data_sources=[                                          # List of data sources
        BioconductorScraper(),
        CranScraper(),
    ]
)

bioconductor_cran_pm.fetch_package("xtable")
```




    <olivia_finder.package.Package at 0x7f3c2a19c910>



In this way we can obtain the network of dependencies for a package recursively, now having access to packages and dependencies that are from CRAN repository


```python
a4_network3 = bioconductor_cran_pm.get_adjlist("a4")
a4_network3
```




    {'a4': []}



As you can see, we can get a more complete network when we combine datasources

It is necessary that there be compatibility as in the case of Bioconductor/CRAN


```python
a4_network.keys() == a4_network2.keys()
```




    False




```python
print(len(a4_network.keys()))
print(len(a4_network2.keys()))
print(len(a4_network3.keys()))
```

    42
    18
    1


## Export the data


```python
bioconductor_df = bioconductor_pm_loaded.export_dataframe(full_data=False)

#Export the dataframe to a csv file
bioconductor_df.to_csv("aux_data/bioconductor_adjlist_scraping.csv", index=False)
bioconductor_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>dependency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ABSSeq</td>
      <td>R</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ABSSeq</td>
      <td>methods</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ABSSeq</td>
      <td>locfit</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ABSSeq</td>
      <td>limma</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AMOUNTAIN</td>
      <td>R</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>28322</th>
      <td>zenith</td>
      <td>reshape2</td>
    </tr>
    <tr>
      <th>28323</th>
      <td>zenith</td>
      <td>progress</td>
    </tr>
    <tr>
      <th>28324</th>
      <td>zenith</td>
      <td>utils</td>
    </tr>
    <tr>
      <th>28325</th>
      <td>zenith</td>
      <td>Rdpack</td>
    </tr>
    <tr>
      <th>28326</th>
      <td>zenith</td>
      <td>stats</td>
    </tr>
  </tbody>
</table>
<p>28327 rows × 2 columns</p>
</div>




```python
pypi_df = pypi_pm_loaded.export_dataframe(full_data=True)
pypi_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>version</th>
      <th>url</th>
      <th>dependency</th>
      <th>dependency_version</th>
      <th>dependency_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0x-sra-client</td>
      <td>4.0.0</td>
      <td>https://pypi.org/project/0x-sra-client/</td>
      <td>urllib3</td>
      <td>2.0.2</td>
      <td>https://pypi.org/project/urllib3/</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0x-sra-client</td>
      <td>4.0.0</td>
      <td>https://pypi.org/project/0x-sra-client/</td>
      <td>six</td>
      <td>1.16.0</td>
      <td>https://pypi.org/project/six/</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0x-sra-client</td>
      <td>4.0.0</td>
      <td>https://pypi.org/project/0x-sra-client/</td>
      <td>certifi</td>
      <td>2022.12.7</td>
      <td>https://pypi.org/project/certifi/</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0x-sra-client</td>
      <td>4.0.0</td>
      <td>https://pypi.org/project/0x-sra-client/</td>
      <td>python</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0x-sra-client</td>
      <td>4.0.0</td>
      <td>https://pypi.org/project/0x-sra-client/</td>
      <td>0x</td>
      <td>0.1</td>
      <td>https://pypi.org/project/0x/</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>933950</th>
      <td>zyfra-check</td>
      <td>0.0.9</td>
      <td>https://pypi.org/project/zyfra-check/</td>
      <td>pytest</td>
      <td>7.3.1</td>
      <td>https://pypi.org/project/pytest/</td>
    </tr>
    <tr>
      <th>933951</th>
      <td>zyfra-check</td>
      <td>0.0.9</td>
      <td>https://pypi.org/project/zyfra-check/</td>
      <td>jira</td>
      <td>3.5.0</td>
      <td>https://pypi.org/project/jira/</td>
    </tr>
    <tr>
      <th>933952</th>
      <td>zyfra-check</td>
      <td>0.0.9</td>
      <td>https://pypi.org/project/zyfra-check/</td>
      <td>testit</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>933953</th>
      <td>zython</td>
      <td>0.4.1</td>
      <td>https://pypi.org/project/zython/</td>
      <td>wheel</td>
      <td>0.40.0</td>
      <td>https://pypi.org/project/wheel/</td>
    </tr>
    <tr>
      <th>933954</th>
      <td>zython</td>
      <td>0.4.1</td>
      <td>https://pypi.org/project/zython/</td>
      <td>minizinc</td>
      <td>0.9.0</td>
      <td>https://pypi.org/project/minizinc/</td>
    </tr>
  </tbody>
</table>
<p>933955 rows × 6 columns</p>
</div>




```python
npm_df = npm_pm_loaded.export_dataframe(full_data=True)
npm_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>version</th>
      <th>url</th>
      <th>dependency</th>
      <th>dependency_version</th>
      <th>dependency_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>--hoodmane-test-pyodide</td>
      <td>0.21.0</td>
      <td>https://www.npmjs.com/package/--hoodmane-test-...</td>
      <td>base-64</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/base-64</td>
    </tr>
    <tr>
      <th>1</th>
      <td>--hoodmane-test-pyodide</td>
      <td>0.21.0</td>
      <td>https://www.npmjs.com/package/--hoodmane-test-...</td>
      <td>node-fetch</td>
      <td>3.3.1</td>
      <td>https://www.npmjs.com/package/node-fetch</td>
    </tr>
    <tr>
      <th>2</th>
      <td>--hoodmane-test-pyodide</td>
      <td>0.21.0</td>
      <td>https://www.npmjs.com/package/--hoodmane-test-...</td>
      <td>ws</td>
      <td>8.13.0</td>
      <td>https://www.npmjs.com/package/ws</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-lidonghui</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/-lidonghui</td>
      <td>axios</td>
      <td>1.4.0</td>
      <td>https://www.npmjs.com/package/axios</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-lidonghui</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/-lidonghui</td>
      <td>commander</td>
      <td>10.0.1</td>
      <td>https://www.npmjs.com/package/commander</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4855089</th>
      <td>zzzzz-first-module</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/zzzzz-first-module</td>
      <td>rxjs</td>
      <td>7.8.1</td>
      <td>https://www.npmjs.com/package/rxjs</td>
    </tr>
    <tr>
      <th>4855090</th>
      <td>zzzzz-first-module</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/zzzzz-first-module</td>
      <td>zone.js</td>
      <td>0.13.0</td>
      <td>https://www.npmjs.com/package/zone.js</td>
    </tr>
    <tr>
      <th>4855091</th>
      <td>zzzzzwszzzz</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/zzzzzwszzzz</td>
      <td>commander</td>
      <td>10.0.1</td>
      <td>https://www.npmjs.com/package/commander</td>
    </tr>
    <tr>
      <th>4855092</th>
      <td>zzzzzwszzzz</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/zzzzzwszzzz</td>
      <td>inquirer</td>
      <td>9.2.2</td>
      <td>https://www.npmjs.com/package/inquirer</td>
    </tr>
    <tr>
      <th>4855093</th>
      <td>zzzzzwszzzz</td>
      <td>1.0.0</td>
      <td>https://www.npmjs.com/package/zzzzzwszzzz</td>
      <td>link</td>
      <td>1.5.1</td>
      <td>https://www.npmjs.com/package/link</td>
    </tr>
  </tbody>
</table>
<p>4855094 rows × 6 columns</p>
</div>



**Get Network graph**


```python
bioconductor_G = bioconductor_pm_loaded.get_network_graph()
bioconductor_G
```




    <networkx.classes.digraph.DiGraph at 0x7f3c229451b0>




```python
# Draw the graph
# ----------------
# Note:
#   - Execution time can take a bit

pos = nx.spring_layout(bioconductor_G)
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(bioconductor_G, pos, node_size=10, node_color="blue")
nx.draw_networkx_edges(bioconductor_G, pos, alpha=0.4, edge_color="black", width=0.1)
plt.title("Bioconductor network graph", fontsize=15)
plt.show()
```
  


## Explore the data 


We can appreciate the difference, as we explained before if we use a combined datasource


```python
bioconductor_cran_pm = PackageManager(
    data_sources=[BioconductorScraper(), CranScraper()]
)

a4_network_2 = bioconductor_cran_pm.fetch_adjlist("a4")
```


```python
import json
print(json.dumps(a4_network_2, indent=4))
```

    {
        "a4": [
            "a4Base",
            "a4Preproc",
            "a4Classif",
            "a4Core",
            "a4Reporting"
        ],
        "a4Base": [
            "a4Preproc",
            "a4Core",
            "methods",
            "graphics",
            "grid",
            "Biobase",
            "annaffy",
            "mpm",
            "genefilter",
            "limma",
            "multtest",
            "glmnet",
            "gplots"
        ],
        "a4Preproc": [
            "BiocGenerics",
            "Biobase"
        ],
        "BiocGenerics": [
            "R",
            "methods",
            "utils",
            "graphics",
            "stats"
        ],
        "R": [],
        "methods": [],
        "utils": [],
        "graphics": [],
        "stats": [],
        "Biobase": [
            "R",
            "BiocGenerics",
            "utils",
            "methods"
        ],
        "a4Core": [
            "Biobase",
            "glmnet",
            "methods",
            "stats"
        ],
        "glmnet": [
            "R",
            "Matrix",
            "methods",
            "utils",
            "foreach",
            "shape",
            "survival",
            "Rcpp"
        ],
        "Matrix": [
            "R",
            "methods",
            "graphics",
            "grid",
            "lattice",
            "stats",
            "utils"
        ],
        "foreach": [
            "R",
            "codetools",
            "utils",
            "iterators"
        ],
        "shape": [
            "R",
            "stats",
            "graphics",
            "grDevices"
        ],
        "survival": [
            "R",
            "graphics",
            "Matrix",
            "methods",
            "splines",
            "stats",
            "utils"
        ],
        "Rcpp": [
            "methods",
            "utils"
        ],
        "grid": [],
        "annaffy": [
            "R",
            "methods",
            "Biobase",
            "BiocManager",
            "GO.db",
            "AnnotationDbi",
            "DBI"
        ],
        "BiocManager": [
            "utils"
        ],
        "GO.db": [],
        "AnnotationDbi": [
            "R",
            "methods",
            "stats4",
            "BiocGenerics",
            "Biobase",
            "IRanges",
            "DBI",
            "RSQLite",
            "S4Vectors",
            "stats",
            "KEGGREST"
        ],
        "stats4": [],
        "IRanges": [
            "R",
            "methods",
            "utils",
            "stats",
            "BiocGenerics",
            "S4Vectors",
            "stats4"
        ],
        "DBI": [
            "methods",
            "R"
        ],
        "RSQLite": [
            "R",
            "bit64",
            "blob",
            "DBI",
            "memoise",
            "methods",
            "pkgconfig"
        ],
        "S4Vectors": [
            "R",
            "methods",
            "utils",
            "stats",
            "stats4",
            "BiocGenerics"
        ],
        "KEGGREST": [
            "R",
            "methods",
            "httr",
            "png",
            "Biostrings"
        ],
        "mpm": [
            "R",
            "MASS",
            "KernSmooth"
        ],
        "MASS": [
            "R",
            "grDevices",
            "graphics",
            "stats",
            "utils",
            "methods"
        ],
        "grDevices": [],
        "KernSmooth": [
            "R",
            "stats"
        ],
        "genefilter": [
            "MatrixGenerics",
            "AnnotationDbi",
            "annotate",
            "Biobase",
            "graphics",
            "methods",
            "stats",
            "survival",
            "grDevices"
        ],
        "MatrixGenerics": [
            "matrixStats",
            "methods"
        ],
        "matrixStats": [
            "R"
        ],
        "annotate": [
            "R",
            "AnnotationDbi",
            "XML",
            "Biobase",
            "DBI",
            "xtable",
            "graphics",
            "utils",
            "stats",
            "methods",
            "BiocGenerics",
            "httr"
        ],
        "XML": [
            "R",
            "methods",
            "utils"
        ],
        "xtable": [
            "R",
            "stats",
            "utils"
        ],
        "httr": [
            "R",
            "curl",
            "jsonlite",
            "mime",
            "openssl",
            "R6"
        ],
        "limma": [
            "R",
            "grDevices",
            "graphics",
            "stats",
            "utils",
            "methods"
        ],
        "multtest": [
            "R",
            "methods",
            "BiocGenerics",
            "Biobase",
            "survival",
            "MASS",
            "stats4"
        ],
        "gplots": [
            "R",
            "gtools",
            "stats",
            "caTools",
            "KernSmooth",
            "methods"
        ],
        "gtools": [
            "methods",
            "stats",
            "utils"
        ],
        "caTools": [
            "R",
            "bitops"
        ],
        "bitops": [],
        "a4Classif": [
            "a4Core",
            "a4Preproc",
            "methods",
            "Biobase",
            "ROCR",
            "pamr",
            "glmnet",
            "varSelRF",
            "utils",
            "graphics",
            "stats"
        ],
        "ROCR": [
            "R",
            "methods",
            "graphics",
            "grDevices",
            "gplots",
            "stats"
        ],
        "pamr": [
            "R",
            "cluster",
            "survival"
        ],
        "cluster": [
            "R",
            "graphics",
            "grDevices",
            "stats",
            "utils"
        ],
        "varSelRF": [
            "R",
            "randomForest",
            "parallel"
        ],
        "randomForest": [
            "R",
            "stats"
        ],
        "parallel": [],
        "a4Reporting": [
            "methods",
            "xtable"
        ]
    }


'''

from __future__ import annotations
from typing import Dict, List, Optional, Union
import pickle
import tqdm
import pandas as pd
import networkx as nx

from .utilities.config import Configuration
from .myrequests.request_handler import RequestHandler
from .utilities.logger import MyLogger
from .data_source.data_source import DataSource
from .data_source.scraper_ds import ScraperDataSource
from .data_source.csv_ds import CSVDataSource
from .data_source.librariesio_ds import LibrariesioDataSource
from .data_source.repository_scrapers.github import GithubScraper
from .package import Package


class PackageManager():
    '''
    Class that represents a package manager, which provides a way to obtain packages from a data source and store them
    in a dictionary
    '''

    def __init__(self, data_sources: Optional[List[DataSource]] = None):
        '''
        Constructor of the PackageManager class

        Parameters
        ----------

        data_sources : Optional[List[DataSource]]
            List of data sources to obtain the packages, if None, an empty list will be used

        Raises
        ------
        ValueError
            If the data_sources parameter is None or empty

        Examples
        --------
        >>> package_manager = PackageManager("My package manager", [CSVDataSource("csv_data_source", "path/to/file.csv")])
        '''

        if not data_sources:
            raise ValueError("Data source cannot be empty")

        self.data_sources: List[DataSource] = data_sources
        self.packages: Dict[str, Package] = {}
        # Init the logger for the package manager
        MyLogger.configure("logger_packagemanager")
        self.logger = MyLogger.get_logger('logger_packagemanager')


    def save(self, path: str):
        '''
        Saves the package manager to a file, normally it has the extension .olvpm for easy identification
        as an Olivia package manager file

        Parameters
        ----------
        path : str
            Path of the file to save the package manager
        '''

        # Remove redundant objects
        for data_source in self.data_sources:
            if isinstance(data_source, ScraperDataSource):
                try:
                    del data_source.request_handler
                except AttributeError:
                    pass
        
        try:

            # Use pickle to save the package manager
            with open(path, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

        except Exception as e:
            raise PackageManagerSaveError(f"Error saving package manager: {e}") from e

    @classmethod
    def load_from_persistence(cls, path: str):
        '''_fro
        Load the package manager from a file, the file must have been created with the save method
        Normally, it has the extension .olvpm

        Parameters
        ----------
        path : str
            Path of the file to load the package manager

        Returns
        -------
        Union[PackageManager, None] 
            PackageManager object if the file exists and is valid, None otherwise
        '''

        # Init the logger for the package manager
        logger = MyLogger.configure("logger_packagemanager")

        # Try to load the package manager from the file
        try:
            # Use pickle to load the package manager
            logger.info(f"Loading package manager from {path}")
            with open(path, "rb") as f:
                obj = pickle.load(f)
                logger.info("Package manager loaded")
        except PackageManagerLoadError:
            logger.error(f"Error loading package manager from {path}")
            return None

        if not isinstance(obj, PackageManager):
            return None
        
        # Set the request handler for the scraper data sources
        for data_source in obj.data_sources:
            if isinstance(data_source, ScraperDataSource):
                data_source.request_handler = RequestHandler()
                # Set the logger for the scraper data source
                data_source.logger = MyLogger.configure("logger_datasource")

        obj.logger = logger

        return obj

    @classmethod
    def load_from_csv(
        cls,
        csv_path: str,
        dependent_field: Optional[str] = None,
        dependency_field: Optional[str] = None, 
        version_field: Optional[str] = None,
        dependency_version_field: Optional[str] = None,
        url_field: Optional[str] = None,
        default_format: Optional[bool] = False,
    ) -> PackageManager:
        '''
        Load a csv file into a PackageManager object

        Parameters
        ----------
        csv_path : str
            Path of the csv file to load
        dependent_field : str = None, optional
            Name of the dependent field, by default None
        dependency_field : str = None, optional
            Name of the dependency field, by default None
        version_field : str = None, optional
            Name of the version field, by default None
        dependency_version_field : str = None, optional
            Name of the dependency version field, by default None
        url_field : str = None, optional
            Name of the url field, by default None
        default_format : bool, optional
            If True, the csv has the structure of full_adjlist.csv, by default False

        Examples
        --------
        >>> pm = PackageManager.load_csv_adjlist(
            "full_adjlist.csv",
            dependent_field="dependent",
            dependency_field="dependency",
            version_field="version",
            dependency_version_field="dependency_version",
            url_field="url"
        )
        >>> pm = PackageManager.load_csv_adjlist("full_adjlist.csv", default_format=True)

        '''

        # Init the logger for the package manager
        MyLogger.configure("logger_packagemanager")
        logger = MyLogger.get_logger(
            logger_name=Configuration().get_key('logger_packagemanager', 'name')
        )

        try:
            logger.info(f"Loading csv file from {csv_path}")
            data = pd.read_csv(csv_path)
        except Exception as e:
            logger.error(f"Error loading csv file: {e}")
            raise PackageManagerLoadError(f"Error loading csv file: {e}") from e

        csv_fields = []

        if default_format:
            # If the csv has the structure of full_adjlist.csv, we use the default fields
            dependent_field = 'name'
            dependency_field = 'dependency'
            version_field = 'version'
            dependency_version_field = 'dependency_version'
            url_field = 'url'
            csv_fields = [dependent_field, dependency_field,
                        version_field, dependency_version_field, url_field]
        else:
            if dependent_field is None or dependency_field is None:
                raise PackageManagerLoadError(
                    "Dependent and dependency fields must be specified")

            csv_fields = [dependent_field, dependency_field]
            # If the optional fields are specified, we add them to the list
            if version_field is not None:
                csv_fields.append(version_field)
            if dependency_version_field is not None:
                csv_fields.append(dependency_version_field)
            if url_field is not None:
                csv_fields.append(url_field)

        # If the csv does not have the specified fields, we raise an error
        if any(col not in data.columns for col in csv_fields):
            logger.error("Invalid csv format")
            raise PackageManagerLoadError("Invalid csv format")

        # We create the data source
        data_source = CSVDataSource(
            file_path=csv_path,
            dependent_field=dependent_field,
            dependency_field=dependency_field,
            dependent_version_field=version_field,
            dependency_version_field=dependency_version_field,
            dependent_url_field=url_field
        )

        obj = cls([data_source])

        # Add the logger to the package manager
        obj.logger = logger
        
        # return the package manager
        return obj

    def initialize(
        self, 
        package_names: Optional[List[str]] = None, 
        show_progress: Optional[bool] = False, 
        chunk_size: Optional[int] = 10000):
        '''
        Initializes the package manager by loading the packages from the data source

        Parameters
        ----------
        package_list : List[str]
            List of package names to load, if None, all the packages will be loaded
        show_progress : bool
            If True, a progress bar will be shown
        chunk_size : int
            Size of the chunks to load the packages, this is done to avoid memory errors

        .. warning:: for large package lists, this method can take a long time to complete

        '''

        # Get package names from the data sources if needed
        if package_names is None:
            for data_source in self.data_sources:
                try:
                    package_names = data_source.obtain_package_names()
                    break
                except NotImplementedError as e:
                    self.logger.debug(f"Data source {data_source} does not implement obtain_package_names method: {e}")
                    continue
                except Exception as e:
                    self.logger.error(f"Error while obtaining package names from data source: {e}")
                    continue

        # Check if the package names are valid
        if package_names is None or not isinstance(package_names, list):
            raise ValueError("No valid package names found")

        # Instantiate the progress bar if needed
        progress_bar = tqdm.tqdm(
            total=len(package_names),
            colour="green",
            desc="Loading packages",
            unit="packages",
        ) if show_progress else None

        # Create a chunked list of package names
        # This is done to avoid memory errors
        package_names_chunked = [package_names[i:i + chunk_size] for i in range(0, len(package_names), chunk_size)]

        for package_names in package_names_chunked:
            # Obtain the packages data from the data source and store them
            self.fetch_packages(
                package_names=package_names, 
                progress_bar=progress_bar,
                extend=True
            )

        # Close the progress bar if needed
        if progress_bar is not None:
            progress_bar.close()

    def fetch_package(self, package_name: str) -> Union[Package, None]:
        '''
        Builds a Package object using the data sources in order until one of them returns a valid package

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        Union[Package, None]
            Package object if the package exists, None otherwise

        Examples
        --------
        >>> package = package_manager.obtain_package("package_name")
        >>> package
        <Package: package_name>
        '''
        # Obtain the package data from the data sources in order
        package_data = None
        for data_source in self.data_sources:
            
            if isinstance(data_source, (GithubScraper, CSVDataSource, ScraperDataSource, LibrariesioDataSource)):
                package_data = data_source.obtain_package_data(package_name)
            else:
                package_data = self.get_package(package_name).to_dict()

            if package_data is not None:
                self.logger.debug(f"Package {package_name} found using {data_source.__class__.__name__}")
                break
            else:
                self.logger.debug(f"Package {package_name} not found using {data_source.__class__.__name__}")


        # Return the package if it exists
        return None if package_data is None else Package.load(package_data)

    def fetch_packages(
        self,
        package_names: List[str],
        progress_bar: Optional[tqdm.tqdm],
        extend: bool = False
    ) -> List[Package]:
        '''
        Builds a list of Package objects using the data sources in order until one of them returns a valid package

        Parameters
        ----------
        package_names : List[str]
            List of package names
        progress_bar : tqdm.tqdm
            Progress bar to show the progress of the operation
        extend : bool
            If True, the packages will be added to the existing ones, otherwise, the existing ones will be replaced

        Returns
        -------
        List[Package]
            List of Package objects
            
        Examples
        --------
        >>> packages = package_manager.obtain_packages(["package_name_1", "package_name_2"])
        >>> packages
        [<Package: package_name_1>, <Package: package_name_2>]
        '''

        # Check if the package names are valid
        if not isinstance(package_names, list):
            raise ValueError("Package names must be a list")

        preferred_data_source = self.data_sources[0]

        # Return list
        packages = []

        # if datasource is instance of ScraperDataSource use the obtain_packages_data method for parallelization
        if isinstance(preferred_data_source, ScraperDataSource):
            
            packages_data = []
            data_found, not_found = preferred_data_source.obtain_packages_data(
                package_names=package_names, 
                progress_bar=progress_bar # type: ignore
            )
            packages_data.extend(data_found)
            # pending_packages = not_found
            self.logger.info(f"Packages found: {len(data_found)}, Packages not found: {len(not_found)}")
            packages = [Package.load(package_data) for package_data in packages_data]
            
        # if not use the obtain_package_data method for sequential processing using the data_sources of the list
        else:

            while len(package_names) > 0:
                
                package_name = package_names[0]
                package_data = self.fetch_package(package_name)
                if package_data is not None:
                    packages.append(package_data)

                # Remove the package from the pending packages
                del package_names[0]

                if progress_bar is not None:
                    progress_bar.update(1)
        
        self.logger.info(f"Total packages found: {len(packages)}")
        
        # update the self.packages attribute overwriting the packages with the same name
        # but conserving the other packages
        if extend:
            self.logger.info("Extending data source with obtained packages")
            for package in packages:
                self.packages[package.name] = package

        return packages
            
    def get_package(self, package_name: str) -> Union[Package, None]:
        '''
        Obtain a package from the package manager

        Parameters
        ----------
        package_name : str
            Name of the package

        Returns
        -------
        Union[Package, None]
            Package object if the package exists, None otherwise

        Examples
        --------
        >>> package = package_manager.get_package("package_name")
        >>> print(package.name)
        '''
        return self.packages.get(package_name, None)

    def get_packages(self) -> List[Package]:
        '''
        Obtain the list of packages of the package manager

        Returns
        -------
        List[Package]
            List of packages of the package manager

        Examples
        --------
        >>> package_list = package_manager.get_package_list()
        '''
        return list(self.packages.values())

    def package_names(self) -> List[str]:
        '''
        Obtain the list of package names of the package manager

        Returns
        -------
        List[str]
            List of package names of the package manager

        Examples
        --------
        >>> package_names = package_manager.get_package_names()
        '''
        return list(self.packages.keys())

    def fetch_package_names(self) -> List[str]:
        '''
        Obtain the list of package names of the package manager

        Returns
        -------
        List[str]
            List of package names of the package manager

        Examples
        --------
        >>> package_names = package_manager.obtain_package_names()
        '''

        return self.data_sources[0].obtain_package_names()

    def export_dataframe(self, full_data = False) -> pd.DataFrame:
        '''
        Convert the object to a adjacency list, where each row represents a dependency
        If a package has'nt dependencies, it will appear in the list with dependency field empty

        Parameters
        ----------
        full_data : bool, optional
            If True, the adjacency list will contain the version and url of the packages, by default False

        Returns
        -------
        pd.DataFrame
            Dependency network as an adjacency list

        Examples    
        --------
        >>> adj_list = package_manager.export_adjlist()
        >>> print(adj_list)
            [name, dependency]
        '''

        if not self.packages:
            self.logger.debug("The package manager is empty")
            return pd.DataFrame()
                    

        rows = []

        if full_data:
            for package_name in self.packages.keys():
                package = self.get_package(package_name)


                for dependency in package.dependencies:
                    
                    try:
                        dependency_full = self.get_package(dependency.name)
                        rows.append(
                            [package.name, package.version, package.url, dependency_full.name, dependency_full.version, dependency_full.url]
                        )
                    except Exception:
                        if dependency.name is not None:
                            rows.append(
                                [package.name, package.version, package.url, dependency.name, None, None]
                            )


            return pd.DataFrame(rows, columns=['name', 'version', 'url', 'dependency', 'dependency_version', 'dependency_url'])
        else:
            for package_name in self.packages.keys():
                package = self.get_package(package_name)
                rows.extend(
                    [package.name, dependency.name]
                    for dependency in package.dependencies
                )
            return pd.DataFrame(rows, columns=['name', 'dependency'])

    def get_adjlist(self, package_name: str, adjlist: Optional[Dict] = None, deep_level: int = 5) -> Dict[str, List[str]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        adjlist : Optional[Dict], optional
            The dependency network of the package, by default None
        deep_level : int, optional
            The deep level of the dependency network, by default 5

        Returns
        -------
        Dict[str, List[str]]
            The dependency network of the package
        """

        # If the deep level is 0, we return the dependency network (Stop condition)
        if deep_level == 0:
            return adjlist

        # If the dependency network is not specified, we create it (Initial case)
        if adjlist is None:
            adjlist = {}

        # If the package is already in the dependency network, we return it (Stop condition)
        if package_name in adjlist:
            return adjlist

        # Use the data of the package manager
        current_package = self.get_package(package_name)
        dependencies =  current_package.get_dependencies_names() if current_package is not None else []

        # Get the dependencies of the package and add it to the dependency network if it is not already in it
        adjlist[package_name] = dependencies

        # Append the dependencies of the package to the dependency network
        for dependency_name in dependencies:

            if (dependency_name not in adjlist) and  (self.get_package(dependency_name) is not None):

                adjlist = self.get_adjlist(
                    package_name = dependency_name, 
                    adjlist = adjlist, 
                    deep_level = deep_level - 1,
                )

        return adjlist

    def fetch_adjlist(self, package_name: str, deep_level: int = 5, adjlist: dict = None) -> Dict[str, List[str]]:
        """
        Generates the dependency network of a package from the data source.

        Parameters
        ----------
        package_name : str
            The name of the package to generate the dependency network
        deep_level : int, optional
            The deep level of the dependency network, by default 5
        dependency_network : dict, optional
            The dependency network of the package

        Returns
        -------
        Dict[str, List[str]]
            The dependency network of the package
        """

        if adjlist is None:
            adjlist = {}

        # If the deep level is 0, we return the adjacency list (Stop condition) 
        if deep_level == 0 or package_name in adjlist:
            return adjlist

        dependencies = []
        try:
            current_package = self.fetch_package(package_name)
            dependencies = current_package.get_dependencies_names()

        except Exception as e:
            self.logger.debug(f"Package {package_name} not found: {e}")

        # Add the package to the adjacency list if it is not already in it
        adjlist[package_name] = dependencies

        # Append the dependencies of the package to the adjacency list if they are not already in it
        for dependency_name in dependencies:
            if dependency_name not in adjlist:
                try:     
                    adjlist = self.fetch_adjlist(
                        package_name=dependency_name,                # The name of the dependency
                        deep_level=deep_level - 1,                   # The deep level is reduced by 1
                        adjlist=adjlist                              # The global adjacency list
                    )
                except Exception:
                    self.logger.debug(
                        f"The package {dependency_name}, as dependency of {package_name} does not exist in the data source"
                    )

        return adjlist

    def __add_chunk(self,
        df, G,
        filter_field=None,
        filter_value=None
    ):
        
        filtered = df[df[filter_field] == filter_value] if filter_field else df
        links = list(zip(filtered["name"], filtered["dependency"]))
        G.add_edges_from(links)
        return G

    def get_network_graph(
            self, chunk_size = int(1e6), 
            source_field = "dependency", target_field = "name",
            filter_field=None, filter_value=None) -> nx.DiGraph:
        """
        Builds a dependency network graph from a dataframe of dependencies.
        The dataframe must have two columns: dependent and dependency.

        Parameters
        ----------
        chunk_size : int
            Number of rows to process at a time
        source_field : str
            Name of the column containing the source node
        target_field : str
            Name of the column containing the target node
        filter_field : str, optional
            Name of the column to filter on, by default None
        filter_value : str, optional
            Value to filter on, by default None

        Returns
        -------
        nx.DiGraph
            Directed graph of dependencies
        """


        # If the default dtasource is a CSV_Datasource, we use custom implementation
        defaul_datasource = self.__get_default_datasource()
        if isinstance(defaul_datasource, CSVDataSource):
            return nx.from_pandas_edgelist(
                defaul_datasource.data, source=source_field, 
                target=target_field, create_using=nx.DiGraph()
            )

        # If the default datasource is not a CSV_Datasource, we use the default implementation
        df = self.export_dataframe()
        try:
            # New NetworkX directed Graph
            G = nx.DiGraph()
            
            for i in range(0, len(df), chunk_size):
                chunk = df.iloc[i:i+chunk_size]
                # Add dependencies from chunk to G
                G = self.__add_chunk(
                    chunk,
                    G,
                    filter_field=filter_field,
                    filter_value=filter_value
                )
        
            return G
        
        except Exception as e:
            print('\n', e)

    def get_transitive_network_graph(self, package_name: str, deep_level: int = 5, generate = False) -> nx.DiGraph:
        """
        Gets the transitive dependency network of a package as a NetworkX graph.

        Parameters
        ----------
        package_name : str
            The name of the package to get the dependency network
        deep_level : int, optional
            The deep level of the dependency network, by default 5
        generate : bool, optional
            If True, the dependency network is generated from the data source, by default False

        Returns
        -------
        nx.DiGraph
            The dependency network of the package
        """

        if generate:
            # Get the dependency network from the data source
            dependency_network = self.fetch_adjlist(package_name=package_name, deep_level=deep_level, adjlist={})

        else:
            # Get the dependency network from in-memory data
            dependency_network = self.get_adjlist(package_name=package_name, deep_level=deep_level)

        # Create a NetworkX graph of the dependency network as (DEPENDENCY ---> PACKAGE)
        G = nx.DiGraph()
        for package_name, dependencies in dependency_network.items():
            for dependency_name in dependencies:
                G.add_edge(dependency_name, package_name)

        return G
    
    def __get_default_datasource(self):
        """
        Gets the default data source

        Returns
        -------
        DataSource
            The default data source
        """

        return self.data_sources[0] if len(self.data_sources) > 0 else None

class PackageManagerLoadError(Exception):
    """
    Exception raised when an error occurs while loading a package manager

    Attributes
    ----------
    message : str
        Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PackageManagerSaveError(Exception):
    """
    Exception raised when an error occurs while saving a package manager

    Attributes
    ----------
    message : str
        Error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

