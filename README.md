# **OLIVIA-FINDER**
## Introduction
Olivia Finder is an open source tool that can be used to extract data from software package dependency networks in package managers. It is designed to work in conjunction with Olivia, and uses web-scraping techniques and CSV files as data sources. With Olivia Finder, you can easily extract information on package dependencies, versions, and other relevant data. This information can be used to analyze software packages and their dependencies, identify potential vulnerabilities or issues, and make informed decisions about which packages to use or avoid. Additionally, Olivia Finder is highly customizable and extensible, allowing you to tailor it to your specific needs and requirements.

## Doc pages
Olivia Finder's documentation is found in Github Pages.The documentation includes details about the functionalities implemented in the library, as well as instructions on how to install the previous requirements and configure a virtual environment for use.

[![Olivia-Finder doc](https://img.shields.io/badge/DOC-Olivia--Finder-blue)](https://dab0012.github.io/olivia-finder)


## Quality metrics
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/771e39014ceb48688cb9d341c705ecf9)](https://www.codacy.com/gh/dab0012/olivia-finder/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dab0012/olivia-finder&amp;utm_campaign=Badge_Grade)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia) 
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dab0012_olivia&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dab0012_olivia)
## Intended audience

Olivia Finder is destined to be used by developers, researchers and centralized packages interested in the identification and analysis of vulnerabilities. It is designed to be used jointly with Olivia, suggesting that users must be familiar with this related tool. In general, users are expected to have technical knowledge and experience in handling networks of software packages.

## Open in Deepnote
Run olivia-finder introduction notebook in Deepnote cloud 
<br>

[<img src="https://deepnote.com/buttons/try-in-a-jupyter-notebook-white-small.svg">](https://deepnote.com/workspace/olivia-0732-b407de18-1731-4b54-b602-aa8db84aa932/project/olivia-finder-627b89b5-a14d-43dd-8e37-100bca8981fc/notebook/olivia-finder%2Folivia_finder%2Fnotebooks%2Folivia_finder_implementation_details-5721bfb8509248bdae331a339efef4aa)

## License

Olivia Finder is distributed under the MIT License. See LICENSE file for details.

## Olivia-Finder data

Olivia-Finder has the capacity to obtain data from the following sources

| Repositorio de Software | Olivia-Finder | Libraries.io CSV Data | External Datasets |
|-------------------------|:-------------:|:---------------------:|:------------------:|
| Alcatraz                | :x:             | :white_check_mark:          | :x:                    |
| Bower                   | :x:             | :white_check_mark:          | :x:                    |
| Bioconductor            | :white_check_mark:             | :x:                       | :x:       |
| CRAN                    | :white_check_mark:  | :white_check_mark:          | :x:                    |
| CPAN                    | :x:  | :white_check_mark:                       | :x:                    |
| Cargo                   | :x:  | :white_check_mark:          | :white_check_mark:       |
| Carthage                | :x:             | :white_check_mark:                       | :x:       |
| CocoaPods               | :x:  | :white_check_mark:          | :x:                    |
| Clojars                 | :x:             | :white_check_mark:          | :x:                    |
| Dub                     | :x:             | :white_check_mark:          | :x:                    |
| Elm                     | :x:             | :white_check_mark:                       | :x:       |
| Go                      | :x:  | :white_check_mark:          | :x:       |
| Hackage                 | :x:             | ::                       | :x:       |
| Haxelib                 | :x:             | :white_check_mark:          | :x:                    |
| Hex                     | :x:             | :white_check_mark:          | :x:                    |
| Homebrew                | :x:             | :white_check_mark:          | :x:                    |
| Inqlude                 | :x:             | :white_check_mark:          | :x:                    |
| Julia                   | :x:             | :white_check_mark:          | :x:                    |
| Maven                   | :x:  | :white_check_mark:                       | :x:                    |
| Meteor                  | :x:             | :white_check_mark:          | :x:                    |
| Nimble                  | :x:             | :white_check_mark:          | :x:                    |
| NPM                     | :white_check_mark:          | :white_check_mark:                    | :X:
| NuGet                   | :x:  | :white_check_mark:          | :x:                    |
| Packagist               | :x:  | :white_check_mark:          | :x:                    |
| Pub                     | :x:  | :white_check_mark:          | :x:                    |
| PyPI                    | :white_check_mark:  | :white_check_mark:          | :x:                    |
| Puppet                  | :x:             | :white_check_mark:          | :x:                    |
| Racket                  | :x:             | :white_check_mark:          | :x:                    |
| Rubygems                | :x:  | :white_check_mark:          | :x:                    |
| SwiftPM                 | :x:             | :white_check_mark:                       | :x:       |

## **Previous TFG notebooks (Olivia)**

[![https://github.com/dsr0018/olivia](https://img.shields.io/badge/Github-Olivia-purple)](https://github.com/dsr0018/olivia)

[![Olivia - Model](https://img.shields.io/badge/Jupyter-Olivia%20--%20Model-%23fa0297)](https://github.com/dsr0018/olivia/blob/master/A-Model.ipynb)
[![Olivia - Analysis](https://img.shields.io/badge/Jupyter-Olivia%20--%20Analysis-%23fa0297)](https://github.com/dsr0018/olivia/blob/master/B-Analysis.ipynb)
[![Olivia - Imunization](https://img.shields.io/badge/Jupyter-Olivia%20--%20Imunization-%23fa0297)](https://github.com/dsr0018/olivia/blob/master/C-Immunization.ipynb)

**Try it in Google colab**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dab0012/olivia-finder/blob/master/olivia/Olivia.ipynb)


**Acknowledgements**

Olivia Finder uses data from the Olivia project, which was created by @dsr0018

The Olivia project is distributed under the MIT License.

# **Author:** 

**Daniel Alonso Báscones**, (dab0012\<at>alu.ubu.es)

University of Burgos, 2023

