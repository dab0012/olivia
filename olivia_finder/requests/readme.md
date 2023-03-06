**Custom requests library**
================


**A custom Python library for sending HTTP requests**

This library is composed of four modules:

`request_handler`, `useragents_handler`, `proxy_handler`, and `proxy_builder`.

<br>


# **Modules**

## **request_handler**

This module contains the `RequestHandler` class, which is responsible for sending HTTP requests. It provides a simple interface for making HTTP requests with options for setting a user agent, proxy, and timeout. It also provides a method for getting the HTML of a page.

The `RequestHandler` is a class that handles HTTP requests in a more transparent way in scraping and denial of service environments by the servers from which the data is requested. Basically, it manages the proxies and user agents so that scraping is not detected.

**Methods**

-   `__init__(self, proxy_handler: ProxyHandler, useragents_handler: UserAgentHandler, max_retry: int = REQUEST_MAX_RETRIES, request_timeout: int = REQUEST_TIMEOUT, num_processes: int = NUM_PROCESSES, use_logger: bool = False)`: 

    Constructor that initializes the `RequestHandler`. 

-   `do_request(self, url:str, params:dict = None, retry_count:int=0) -> Union[Tuple[str, requests.Response], None]`: 

    Do a request to the given url. 

-   `do_parallel_requests(self, url_list:List[str], param_list:List[dict], progress_bar:tqdm.tqdm = None)`: 

    Do parallel requests to the given urls.

<br>

## **useragents_handler**

This module contains the `UserAgentsHandler` class, which is responsible for getting a random user agent. It provides a method for getting a random user agent.

**Methods**
-   `__init__(self, useragents_file_path: str = None, logger: logging.Logger = None)`: 

    Constructor that initializes the class by loading user agents from a file or from the web. If no user agents are loaded, a default user agent is used.
-   `_load_from_file(self, file_path:str) -> bool`: 

    Loads user agents from a file and returns True if successful.

-   `_load_from_API(self) -> bool`: 
    
    Gets user agents from the specified website and saves them in the user agent list. Returns True if successful.

-   `get_next_useragent(self) -> str`: 
    
    Returns a random user agent from the list.

<br>

## **proxy_handler**

The `ProxyHandler` class is used to handle proxy rotation and usage. It provides a method `get_next_proxy()` that returns a randomly selected proxy from the list of available proxies. The selected proxy is then rotated to the end of the list to prevent it from being used too frequently.

The `ProxyHandler` class also handles the lifetime of each proxy by keeping track of the number of times it has been used. If a proxy has been used more times than the specified maximum limit, it is removed from the list of available proxies.

**Methods**

The `ProxyHandler` class has the following methods:

-   `__init__(self, builders=None, proxy_max_uses=50, logger=None)`: 

    initializes the `ProxyHandler` object. If `builders` is `None`, the default list of available builders is used. `proxy_max_uses` sets the maximum number of uses for each proxy. `logger` is an optional logger object.

-   `get_next_proxy(self)`: 

    gets the next proxy from the list of available proxies and rotates it to the end of the list. Returns the next proxy or `None` if there are no proxies available.

-   `handle_lifetime(self, proxy)`: 

    handles the lifetime of the given proxy by updating its usage count and removing it from the list of available proxies if it has been used more times than the specified maximum limit.

-   `_get_proxies(self)`: 

    gets a list of unique proxies from the list of `proxy_builders`.

-   `_get_available_builders(self)`: 
    
    gets a list of `ProxyBuilder` objects that are available for use.

<br>

## **proxy_builder**

This module contains the `ProxyBuilder` class. It defines an abstract class ProxyBuilder and four classes SSLProxies, FreeProxyList, GeonodeProxy, and NoProxy. Each of these four classes extends the ProxyBuilder class and implements its abstract method parse which returns a list of proxies obtained from a particular source.

The `ProxyBuilder` interface defines an abstract method `parse` that must be implemented by its subclasses. `ProxyBuilder` also has a concrete method `get_proxies`, which returns a list of proxies obtained from a URL.

The implementations of `ProxyBuilder` each retrieve proxies from a specific website, and their `parse` method is responsible for parsing the HTML of the proxy list page to extract the proxies. The four implementations retrieve proxies from the following websites:

-   `SSLProxies`: <https://www.sslproxies.org/>
-   `FreeProxyList`: <https://free-proxy-list.net/anonymous-proxy.html>
-   `GeonodeProxy`: <https://proxylist.geonode.com/>
-   `NoProxy`: returns an empty list of proxies

Each implementation has a `URL` class variable that specifies the URL from which it retrieves proxies.

<br>

---


    /*
    * File:              readme.md
    * Project:           Olivia-Finder
    * Created Date:      Saturday March 4th 2023
    * Author:            Daniel Alonso Báscones
    * Last Modified:     Saturday March 4th 2023 11:43:48 am
    * Modified By:       The developer formerly known as dab0012 <at> alu.ubu.es
    * -----
    * Copyright (c) 2023 Daniel Alonso Báscones
    * -----
    */