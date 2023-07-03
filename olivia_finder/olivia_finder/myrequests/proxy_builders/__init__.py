"""

## **The proxy_builders subpackage**

The `ProxyBuilder` class is an abstract base class that represents a proxy builder. It cannot be instantiated directly, but must be subclassed to create a concrete proxy builder.

### Creating a Subclass

To create a subclass of `ProxyBuilder`, you must implement the `_parse_request` method. This method takes a `requests.Response` object as a parameter and returns a list of proxies.

Here's an example subclass that retrieves proxies from a website that provides SSL proxies:

```python
from proxy_builder import ProxyBuilder

class SSLProxiesBuilder(ProxyBuilder):
    '''
    Class to represent a proxy builder that retrieves SSL proxies from a website
    '''

    def __init__(self, url: str = None, request_timeout: int = None):
        '''
        Constructor
        
        Parameters
        ----------
        url : str
            URL of the proxy list website to get the proxies
        request_timeout : int
            Timeout for the proxy list requests
        '''
        super().__init__(url, request_timeout)

    def _parse_request(self, response: requests.Response) -> List[str]:
        '''
        Parse the response from the SSLProxies website and return a list of proxies

        Parameters
        ----------
        response : requests.Response
            The response from the request

        Returns
        -------
        List[str]
            A list of proxies
        '''
        # Parse the response and return a list of proxies
        # ...
```

### Using a Subclass

To use a subclass of `ProxyBuilder`, you can create an instance of the subclass and call its `get_proxies` method to retrieve a list of proxies.

Here's an example of how to use the `SSLProxiesBuilder` subclass:

```python
from proxy_builders.ssl_proxies import SSLProxiesBuilder

# Create an instance of the SSLProxiesBuilder class
ssl_proxies = SSLProxiesBuilder(url='https://www.sslproxies.org/')

# Get a list of proxies from the website
proxies = ssl_proxies.get_proxies()

# Use the proxies for your application
# ...
```

That's a brief guide on how to use the `ProxyBuilder` class. Let me know if you have any questions!


Submodules of proxy_builders package:
------------------------------------

- :class:`olivia_finder.myrequests.proxy_builders.ssl_proxies.SSLProxiesBuilder`
- :class:`olivia_finder.myrequests.proxy_builders.list_builder.ListProxyBuilder`

"""