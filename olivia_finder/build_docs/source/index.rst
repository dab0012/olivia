.. Olivia Finder documentation master file, created by
   sphinx-quickstart on Wed Mar 15 18:05:55 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Olivia Finder's documentation!
==============================

Introduction
------------

Olivia Finder is a Python library that allows users to obtain from package data to be used with the Olivia project, 
an open-source library that indexes vulnerability identification and analysis. 
Olivia is designed to help software developers and centralised package managers understand the risks of using dependencies in their projects. 


Modules
-------

Here are the modules provided by Olivia Finder:

* **olivia_finder.package**

   This module contains the Package class, which is used to represent a package and its metadata.

   :mod:`olivia_finder.package`

* **olivia_finder.package_manager**

   This module contains the PackageManager class, which is used to represent a package manager and itd packages
   The PackageManager class provides a set of methods to obtain package objects from a package manager.

   :mod:`olivia_finder.package_manager`

Subpackages
-----------

* **olivia_finder.data_source**

   This subpackage contains the DataSource class, which is used to represent a data source and its data
   The DataSource class provides a set of methods to obtain package data from a data source.

   .. toctree::
      :maxdepth: 1

      olivia_finder/data_source/data_source_module

* **olivia_finder.myrequests**

   This subpackage contains a set os classes that can be used to make requests to a Web scraping based data_source

   .. toctree::
      :maxdepth: 1

      olivia_finder/myrequests/myrequests_module

* **olivia_finder.utilities**

   This subpackage contains a set of utility Classes and functions to help with the use of Olivia Finder

   .. toctree::
      :maxdepth: 1

      olivia_finder/utilities/utilities_module


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`