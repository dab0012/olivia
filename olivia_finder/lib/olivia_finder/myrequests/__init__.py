"""

## **Description**

The MyRequest subpackage is designed to obtain data repetitively from a web server

It is able to perform requests with thread parallelism

## **Package structure**

```bash
├── data
│   └── useragents.txt
├── __init__.py
├── job.py
├── proxy_builders
│   ├── __init__.py
│   ├── list_builder.py
│   ├── proxy_builder.py
│   └── ssl_proxies.py
├── proxy_handler.py
├── request_handler.py
├── request_worker.py
└── useragent_handler.py
```

## **Package modules**

- **olivia_finder.myrequests.job**

  It represents a web request work, implements Thread

- **olivia_finder.myrequests.proxy_builders.proxy_builder**

  It contains the ProxyBuilder class, used to request proxies from web services

- **olivia_finder.myrequests.proxy_handler**

  It contains the ProxyHandler class, used by the **RequestHandler** object to obtain a fresh proxy (Singleton)

- **olivia_finder.myrequests.useragent_handler**

  It contains the UserAgentHandler class, used by the **RequestHandler** object to obtain a fresh user agent (Singleton)

- **olivia_finder.myrequests.request_handler**

  It contains the **RequestHandler** class, from which we can perform the corresponding works


## **Class ProxyBuilder and subclasses**


You have the functionality of obtaining a list of internet proxys from some more or less stable data source

ProxyBuilder It is an abstract class and should not be used directly, Its use is made through its subclasses


We can focus on two different ways:

- Obtain the data through Web Scraping from some website that provides updated proxys

- Obtain the data from a proxies list in format `<IP>:<PORT>` from a web server

This is shown below


**Web scraping implementation (from sslproxies.org)**


```python
pb_SSLProxies = SSLProxiesBuilder()
pb_SSLProxies.get_proxies()
```
    ['35.247.245.218:3129',
     '164.90.253.93:3128',
     '190.61.88.147:8080',
     '152.67.10.190:8100',
     '113.53.231.133:3129',
     '115.144.101.201:10001',
     '207.38.87.110:30114',
     '43.156.100.152:80',
     ...
     '93.91.112.247:41258',
     '103.180.59.220:8080']



**Web list implementation (from lists)**



```python
pb_ListBuilder = ListProxyBuilder(url="https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt")
pb_ListBuilder.get_proxies()
```

    ['20.241.236.196:3128',
     '3.8.144.154:3128',
     '34.94.3.209:8585',
     '20.99.187.69:8443',
     '35.181.54.72:3128',
     ...
     '103.75.117.21:4443',
     '193.138.178.6:8282',
     '84.255.35.210:9898',
     '160.242.19.126:8080',
     '167.114.19.195:8050',
     '213.233.177.180:3000',
     '188.166.247.215:5000',
     '103.146.222.2:83',
     '188.132.222.198:8080',
     '217.21.214.139:8080',
     '85.173.165.36:46330',
     '179.63.149.2:999',
     '182.253.79.20:8080',
     '200.106.184.97:999']


### **Class ProxyHandler**


```python
ph = ProxyHandler()
```

### **Class UserAgentHandler**


The purpose of this class is to provide a set of useragents to be used by the **RequestHandler** object with the aim of hiding the original identity of the web request

The class is prepared to load the useragents from a text file contained in the package, and in turn can obtain them from a website dedicated to provide them.

.. warning::

    If both options are not available, there will be used the default ones hardcoded in the class

.. note::

    Useragents dataset included on the package **MyRequests**



```bash
>$ tail ../olivia_finder/myrequests/data/useragents.txt

    Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36
    Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3
    Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36
    Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/50.0.125 Chrome/44.0.2403.125 Safari/537.36
    Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36
    Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAARJS; rv:11.0) like Gecko
    Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900T Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
    Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4
```


The default constructor loads the usragents from the file


```python
ua_handler = UserAgentHandler()
ua_handler.useragents_list[:5]
```
    ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9']
     
.. note::
     
    We can force obtaining the useragents from the Internet with the flag: `use_file=False`

```python
ua_handler = UserAgentHandler(use_file=False)
ua_handler.useragents_list[:5]
```


Once the class is initialized, it can provide a random useragent to the object **RequestHandler** to perform the request



```python
useragents = [ua_handler.get_next_useragent() for _ in range(10)]
useragents
```

    ['Mozilla/5.0 (Linux; Android 4.4.2; RCT6773W22 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
     'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']



### Class **RequestHandler**


It is the main class of the **MyRequest** package and makes use of the **ProxyHandler** and **UserAgentHandler** classes to obtain the proxies and user agents that will be used in the web requests that is responsible for performing.


The default constructor does not receive parameters, the class will manage to instantize their units and use the default configuration


**Make a request**



```python
job = RequestJob(
    key="networkx",
    url="https://www.pypi.org/project/networkx/"
)
```


```python
rh = RequestHandler()
finalized_job = rh.do_request(job)
```

As a result we obtain the ResponseJob object but with the data of the response



```python
print(
    f'Key: {finalized_job.key}\\n'+
    f'URL: {finalized_job.url}\\n'+
    f'Response: {finalized_job.response}\\n'+
)
```

    Key: networkx
    URL: https://www.pypi.org/project/networkx/
    Response: <Response [200]>
    


**Do parallel requests**


We can make parallel requests through the use of Threads, it is safe to do so since the class is prepared for it


```python
# MyLogger().disable()
```


```python
# Initialize **RequestHandler**
from tqdm import tqdm
rh = **RequestHandler**()

# Initialize RequestJobs
request_jobs = [
    RequestJob(key="networkx", url="https://www.pypi.org/project/networkx/"),
    RequestJob(key="pandas", url="https://www.pypi.org/project/pandas/"),
    RequestJob(key="numpy", url="https://www.pypi.org/project/numpy/"),
    RequestJob(key="matplotlib", url="https://www.pypi.org/project/matplotlib/"),
    RequestJob(key="scipy", url="https://www.pypi.org/project/scipy/"),
    RequestJob(key="scikit-learn", url="https://www.pypi.org/project/scikit-learn/"),
    RequestJob(key="tensorflow", url="https://www.pypi.org/project/tensorflow/"),
    RequestJob(key="keras", url="https://www.pypi.org/project/keras/")
]

# Set number of workers
num_workers = 4

# Initialize progress bar
progress_bar = tqdm(total=len(request_jobs))

finalized_jobs = rh.do_requests(
    request_jobs=request_jobs,
    num_workers=num_workers,
    progress_bar=progress_bar
)
```

As a result we get a list of ResponseJob objects


```python
for job in finalized_jobs:
    print(f'Key: {job.key}, URL: {job.url}, Response: {job.response}')
```

    Key: networkx, URL: https://www.pypi.org/project/networkx/, Response: <Response [200]>
    Key: tensorflow, URL: https://www.pypi.org/project/tensorflow/, Response: <Response [200]>
    Key: pandas, URL: https://www.pypi.org/project/pandas/, Response: <Response [200]>
    Key: keras, URL: https://www.pypi.org/project/keras/, Response: <Response [200]>
    Key: numpy, URL: https://www.pypi.org/project/numpy/, Response: <Response [200]>
    Key: scikit-learn, URL: https://www.pypi.org/project/scikit-learn/, Response: <Response [200]>
    Key: matplotlib, URL: https://www.pypi.org/project/matplotlib/, Response: <Response [200]>
    Key: scipy, URL: https://www.pypi.org/project/scipy/, Response: <Response [200]>


The Job object contains the response to request



```python
print(finalized_jobs[0].response.text[10000:20000])
```

```html
    ss="split-layout split-layout--middle package-description">
        
          <p class="package-description__summary">Python package for creating and manipulating graphs and networks</p>
        
        <div data-html-include="/_includes/edit-project-button/networkx">
        </div>
        </div>
      </div>
    </div>
    
    <div data-controller="project-tabs">
      <div class="tabs-container">
        <div class="vertical-tabs">
          <div class="vertical-tabs__tabs">
            <div class="sidebar-section">
              <h3 class="sidebar-section__title">Navigation</h3>
              <nav aria-label="Navigation for networkx">
                <ul class="vertical-tabs__list" role="tablist">
                  <li role="tab">
                    <a id="description-tab" href="#description" data-project-tabs-target="tab" data-action="project-tabs#onTabClick" class="vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--is-active" aria-selected="true" aria-label="Project description. Focus will be moved to the description.">
                      <i class="fa fa-align-left" aria-hidden="true"></i>
                      Project description
                    </a>
                  </li>
                  <li role="tab">
```

"""