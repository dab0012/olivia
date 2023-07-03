'''
# Subpackage utilities

The utility package is designed to contain source code that is used in the library on a recurring basis, and whose functionality is to provide a certain utility to the library.

## Module structure

**Package structure**

```bash
../../olivia_finder/olivia_finder/utilities
├── config.py
├── exception.py
├── __init__.py
├── logger.py
├── singleton_decorator.py
└── utilities.py
```


## Module `utilities.config`


Provides the configuration class, which is used to obtain the configuration variables defined in the .ini configuration file

.. warning::

    It is a Singleton instance so only one instance is accessible from any part of the code through the constructor

    



```python
from olivia_finder.utilities.config import Configuration
```

You need to provide a configuration file

The configuration file is located in the root of the olivia_finder package

In this execution we are using a personalized configuration file for demonstration


```python
!cat ./config.ini
```

    [olivia_finder_logger]
    ; Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    name                     = olivia_finder
    level                    = DEBUG
    status                   = ENABLED
    file_handler             = ENABLED
    console_handler          = ENABLED
    
    ; Myrequests configuration
    [logger_myrequests]
    name                 = olivia_finder.myrequests
    level                = DEBUG
    status               = DISABLED
    file_handler         = DISABLED
    console_handler      = DISABLED
    
    ; Package Manager configuration
    [logger_packagemanager]
    name                 = olivia_finder.packagemanager
    level                = DEBUG
    status               = DISABLED
    file_handler         = DISABLED
    console_handler      = DISABLED
    
    ; CSV Datasource configuration
    [logger_datasource]
    name                 = olivia_finder.datasource
    level                = DEBUG
    status               = DISABLED
    file_handler         = DISABLED
    console_handler      = DISABLED
    
    ; Output directory for the results
    [folders]
    logger                      = logs/
    working_dir                 = results/working/
    
    
    ; Libraries.io configuration
    [librariesio]
    api_key                     = 558f419425861e607e78cd4e3a0b129b

Acess the keys using `get_key` method


```python
Configuration().get_key('olivia_finder_logger', 'status')
``
    'ENABLED'


## Module `utilities.logger`



```python
from olivia_finder.utilities.logger import MyLogger
```

The class MyLogger implements an utility loging tools to register the actions of execution. It is based on the default Python logging module


```python

logger = MyLogger.get_logger("olivia_finder_logger")

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')

# Acess the logger using the default logging class
import logging
logging.getLogger(logger.name).debug('Debug message')
```

    [32;20m2023-06-28 19:26:34,316 [olivia_finder(DEBUG)] -> 4423775.py:3[0m
    Debug message
    [34;20m2023-06-28 19:26:34,318 [olivia_finder(INFO)] -> 4423775.py:4[0m
    Info message
    [33;20m2023-06-28 19:26:34,318 [olivia_finder(WARNING)] -> 4423775.py:5[0m
    Warning message
    [38;5;208;20m2023-06-28 19:26:34,319 [olivia_finder(ERROR)] -> 4423775.py:6[0m
    Error message
    [31;20m2023-06-28 19:26:34,319 [olivia_finder(CRITICAL)] -> 4423775.py:7[0m
    Critical message
    [32;20m2023-06-28 19:26:34,320 [olivia_finder(DEBUG)] -> 4423775.py:10[0m
    Debug message
    [32;20m2023-06-28 19:26:34,320 [olivia_finder(DEBUG)] -> 4423775.py:14[0m
    Debug message


Default logger is root


```python
# The default logger is root and it is not configured
MyLogger.get_logger().debug('Debug message')
MyLogger.get_logger().info('Info message')
MyLogger.get_logger().warning('Warning message')
MyLogger.get_logger().error('Error message')
MyLogger.get_logger().critical('Critical message')
```
    Warning message
    Error message
    Critical message

Change log level


```python
MyLogger.configure_level("olivia_finder_logger", 'console', 'warning')
logger = MyLogger.get_logger("olivia_finder_logger")
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
```

    [33;20m2023-06-28 19:26:34,331 [olivia_finder(WARNING)] -> 446635553.py:4[0m
    Warning message
    [38;5;208;20m2023-06-28 19:26:34,332 [olivia_finder(ERROR)] -> 446635553.py:5[0m
    Error message
    [31;20m2023-06-28 19:26:34,333 [olivia_finder(CRITICAL)] -> 446635553.py:6[0m
    Critical message

## Module `utilities.exceptions`

Includes a series of exceptions to be used by the library and provide a more generic context in the case of being rised


```python
from olivia_finder.utilities.exception import OliviaFinderException
```


```python
OliviaFinderException('Test exception')
```
    OliviaFinderException: Test exception



## Module `utilities.singleton_decorator`

This module includes a decorator-based implementation of the Singleton design pattern


```python
from olivia_finder.utilities.singleton_decorator import singleton
```


```python
# Dummy class
@singleton
class Dummy:
    def __init__(self, name):
        self.name = name
```


```python
print(Dummy('test').name)
print(Dummy('test2').name)
```

    test
    test


## Module `utilities.utilities`

A module containing common source code to be reused

'''