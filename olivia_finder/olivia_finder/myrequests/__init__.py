"""

The myrequest package is prepared to concurrently make requests to a web server, being able to abuse these requests without denying us the service. 

The package includes different modules that are responsible for carrying out this task transparently, such as obtaining proxies and useragents to disguise the origin of the request, or the concurrent execution of requests.


## Module structure

**Package structure**



```python
!tree ../../olivia_finder/olivia_finder/myrequests
```
    [01;34m../../olivia_finder/olivia_finder/myrequests[0m
    ├── [01;34mdata[0m
    │   └── [00museragents.txt[0m
    ├── [00m__init__.py[0m
    ├── [00mjob.py[0m
    ├── [01;34mproxy_builders[0m
    │   ├── [00m__init__.py[0m
    │   ├── [00mlist_builder.py[0m
    │   ├── [00mproxy_builder.py[0m
    │   └── [00mssl_proxies.py[0m
    ├── [00mproxy_handler.py[0m
    ├── [01;32mrequest_handler.py[0m
    ├── [00mrequest_worker.py[0m
    └── [00museragent_handler.py[0m
    
    2 directories, 11 files


## Subpackage `myrequests.proxy_builders`


The proxy builder subpackage takes care of getting a list of proxies. 

Two implementations are available, one based on an online proxy provider called SSL proxies, and the other based on a proxy list. The proxy list-based implementation is proposed as the best option due to its genericity.

We can focus on two different ways:

- Obtain the data through Web Scraping from some website that provides updated proxys, like SSLProxies

- Obtain the data from a proxies list in format `<IP>:<PORT>` from a web server

This is shown below


**_Web scraping implementation (from sslproxies.org)_**



```python
from olivia_finder.myrequests.proxy_builders.ssl_proxies import SSLProxiesBuilder
```


```python
pb_SSLProxies = SSLProxiesBuilder()
pb_SSLProxies.get_proxies()
```

    ['78.46.190.133:8000',
     '64.225.4.63:9993',
     ...
     '103.129.92.95:9995',
     '40.83.102.86:80',
     '87.237.239.57:3128',
     '86.57.137.63:2222',
     '140.238.245.116:8100',
     '171.244.65.14:4002',
     '35.240.219.50:8080',
     '115.144.1.222:12089',
     '119.8.120.4:80',
     '41.174.96.38:32650']



**_Web list implementation (from lists)_**



```python
from olivia_finder.myrequests.proxy_builders.list_builder import ListProxyBuilder
```


```python
pb_ListBuilder = ListProxyBuilder(
    url="https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt")
pb_ListBuilder.get_proxies()
```

    ['77.247.108.17:33080',
     '195.133.45.149:7788',
     '94.110.148.115:3128',
     '35.240.156.235:8080',
      ...
     '103.157.83.229:8080',
     '36.91.46.26:8080',
     '82.165.184.53:80']



## Module `myrequests.proxy_handler`


```python
from olivia_finder.myrequests.proxy_handler import ProxyHandler
```


```python
ph = ProxyHandler()
```


```python
for i in range(10):
    print(ph.get_next_proxy())
```

    http://170.130.55.153:5001
    http://104.17.16.136:80
    http://104.234.138.40:3128
    http://45.131.5.32:80
    http://203.32.120.18:80
    http://172.67.23.197:80
    http://185.162.229.77:80
    http://203.13.32.148:80
    http://172.67.251.80:80
    http://103.19.130.50:8080


## Module `myrequests.useragent_handler`


```python
from olivia_finder.myrequests.useragent_handler import UserAgentHandler
```

The purpose of this class is to provide a set of useragents to be used by the RequestHandler object with the aim of hiding the original identity of the web request

The class is prepared to load the useragents from a text file contained in the package, and in turn can obtain them from a website dedicated to provide them.

If both options are not available, there will be used the default ones hardcoded in the class


Useragents dataset included on the package MyRequests



```python
!tail ../../olivia_finder/olivia_finder/myrequests/data/useragents.txt
```

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



We can force obtaining the useragents from the Internet with the flag:

```python
use_file=False
```

We can force get useragents from internet 


```python
import gc

# Delete the object and force the garbage collector to free the memory
del ua_handler
UserAgentHandler.destroy()  # Delete the singleton instance
gc.collect()

from olivia_finder.myrequests.useragent_handler import UserAgentHandler
ua_handler = UserAgentHandler(use_file=False)
ua_handler.useragents_list[:5]
```

  ['Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
  'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
  'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)',
  'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
  'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)']


Once the class is initialized, it can provide a random useragent to the object RequestHandler to perform the request



```python
useragents = [ua_handler.get_next_useragent() for _ in range(10)]
useragents
```




    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko',
     'Mozilla/5.0 (X11; Linux x86_64; U; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
     'Mozilla/5.0 (Linux; Android 4.4.2; SM-T530NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0; 1ButtonTaskbar)',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
     'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3']



## Module `myrequests.request_handler`


```python
from olivia_finder.myrequests.job import RequestJob
from olivia_finder.myrequests.request_handler import RequestHandler
```

It is the main class of the MyRequest package and makes use of the ProxyHandler and UserAgentHandler classes to obtain the proxies and user agents that will be used in the web requests that is responsible for performing.


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
    f'Key: {finalized_job.key}\n'
    f'URL: {finalized_job.url}\n'
    f'Response: {finalized_job.response}\n'
)
```

    Key: networkx
    URL: https://www.pypi.org/project/networkx/
    Response: <Response [200]>
    


**Do parallel requests**


We can make parallel requests through the use of Threads, it is safe to do so since the class is prepared for it



```python
# Initialize RequestHandler
from tqdm import tqdm
rh = RequestHandler()

# Initialize RequestJobs
request_jobs = [
    RequestJob(key="networkx", url="https://www.pypi.org/project/networkx/"),
    RequestJob(key="pandas", url="https://www.pypi.org/project/pandas/"),
    RequestJob(key="numpy", url="https://www.pypi.org/project/numpy/"),
    RequestJob(key="matplotlib",
               url="https://www.pypi.org/project/matplotlib/"),
    RequestJob(key="scipy", url="https://www.pypi.org/project/scipy/"),
    RequestJob(key="scikit-learn",
               url="https://www.pypi.org/project/scikit-learn/"),
    RequestJob(key="tensorflow",
               url="https://www.pypi.org/project/tensorflow/"),
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

      0%|          | 0/8 [00:00<?, ?it/s] 88%|████████▊ | 7/8 [00:02<00:00,  3.36it/s]

As a result we get a list of ResponseJob objects



```python
for job in finalized_jobs:
    print(f'Key: {job.key}, URL: {job.url}, Response: {job.response}')
```

    Key: networkx, URL: https://www.pypi.org/project/networkx/, Response: <Response [200]>
    Key: scipy, URL: https://www.pypi.org/project/scipy/, Response: <Response [200]>
    Key: pandas, URL: https://www.pypi.org/project/pandas/, Response: <Response [200]>
    Key: tensorflow, URL: https://www.pypi.org/project/tensorflow/, Response: <Response [200]>
    Key: numpy, URL: https://www.pypi.org/project/numpy/, Response: <Response [200]>
    Key: scikit-learn, URL: https://www.pypi.org/project/scikit-learn/, Response: <Response [200]>
    Key: matplotlib, URL: https://www.pypi.org/project/matplotlib/, Response: <Response [200]>
    Key: keras, URL: https://www.pypi.org/project/keras/, Response: <Response [200]>


The Job object contains the response to request



```python
print(finalized_jobs[0].response.text[10000:20000])
```

     class="split-layout split-layout--middle package-description">
        
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
                    <a id="history-tab" href="#history" data-project-tabs-target="tab" data-action="project-tabs#onTabClick" class="vertical-tabs__tab vertical-tabs__tab--with-icon" aria-label="Release history. Focus will be moved to the history panel.">
                      <i class="fa fa-history" aria-hidden="true"></i>
                      Release history
                    </a>
                  </li>
                  
                  <li role="tab">
                    <a id="files-tab" href="#files" data-project-tabs-target="tab" data-action="project-tabs#onTabClick" class="vertical-tabs__tab vertical-tabs__tab--with-icon" aria-label="Download files. Focus will be moved to the project files.">
                      <i class="fa fa-download" aria-hidden="true"></i>
                      Download files
                    </a>
                  </li>
                  
                </ul>
              </nav>
            </div>
            
...

"""

