'''
# **Subpackage utilities**

## Module config

Provides the configuration class, which is used to obtain the configuration variables defined in the .ini configuration file

.. warning::

    It is a Singleton instance so only one instance is accessible from any part of the code through the constructor

```python
Configuration().get_key('logger', 'status')
>>> 'ENABLED'
```

## Module logger

The class MyLogger implements a customized logger to register the actions of execution

It is a Singleton instance so only one instance is accessible from any part of the code through the constructor


```python
MyLogger().set_level("DEBUG")

# Log messages
MyLogger().get_logger().debug("Hello World 1")
MyLogger().get_logger().info("Hello World 2")

# disable logger
MyLogger().disable()
MyLogger().get_logger().error("Hello World 3")

# re-enable logger
MyLogger().enable()

MyLogger().get_logger().warning("Hello World 4")
MyLogger().get_logger().error("Hello World 5")
MyLogger().get_logger().critical("Hello World 6")

# reset logger level
MyLogger().set_level(Configuration().get_key('logger', 'level'))
```

```python
>>> [2023-05-15 20:31:29,729 [DEBUG] in 1504849287.<module> (1504849287.py:4)
>>> Hello World 1
>>> [2023-05-15 20:31:29,729 [INFO] in 1504849287.<module> (1504849287.py:5)
>>> Hello World 2
>>> [2023-05-15 20:31:29,730 [WARNING] in 1504849287.<module> (1504849287.py:14)
>>> Hello World 4
>>> [2023-05-15 20:31:29,730 [ERROR] in 1504849287.<module> (1504849287.py:15)
>>> Hello World 5
>>> [2023-05-15 20:31:29,731 [CRITICAL] in 1504849287.<module> (1504849287.py:16)
>>> Hello World 6
```

The **console handler** shows the different levels using indicative colors

The **file handler** has the default format



```bash
>$ cat logs/example_log.log
```

```bash
2023-04-25 18:58:06 [DEBUG] Hello World 1 (1008465612.py:7)
2023-04-25 18:58:06 [INFO] Hello World 2 (1008465612.py:8)
2023-04-25 18:58:06 [WARNING] Hello World 4 (1008465612.py:17)
2023-04-25 18:58:06 [ERROR] Hello World 5 (1008465612.py:18)
2023-04-25 18:58:06 [CRITICAL] Hello World 6 (1008465612.py:19)
2023-04-25 19:00:07 [INFO] RequestHandler: Creating RequestHandler object
Number of jobs: 1
Number of workers: 1
Creating jobs queue (request_handler.py:20)
2023-04-25 19:00:07 [INFO] Jobs queue created (request_handler.py:25)
2023-04-25 19:00:07 [INFO] Jobs queue size: 1 (request_handler.py:26)
2023-04-25 19:00:07 [INFO] Creating workers (request_handler.py:35)
2023-04-25 19:00:07 [DEBUG] Starting new HTTPS connection (1): www.sslproxies.org:443 (connectionpool.py:973)
2023-04-25 19:00:07 [DEBUG] https://www.sslproxies.org:443 "GET / HTTP/1.1" 200 None (connectionpool.py:452)
2023-04-25 19:00:08 [DEBUG] Found 100 proxies from SSLProxiesBuilder (proxy_builder.py:75)
2023-04-25 19:00:08 [DEBUG] Starting new HTTPS connection (1): raw.githubusercontent.com:443 (connectionpool.py:973)
2023-04-25 19:00:08 [DEBUG] https://raw.githubusercontent.com:443 "GET /mertguvencli/http-proxy-list/main/proxy-list/data.txt HTTP/1.1" 200 2034 (connectionpool.py:452)
2023-04-25 19:00:08 [DEBUG] Found 307 proxies from ListProxyBuilder (proxy_builder.py:75)
2023-04-25 19:00:08 [DEBUG] Starting new HTTPS connection (1): raw.githubusercontent.com:443 (connectionpool.py:973)
2023-04-25 19:00:08 [DEBUG] https://raw.githubusercontent.com:443 "GET /TheSpeedX/SOCKS-List/master/http.txt HTTP/1.1" 200 18270 (connectionpool.py:452)
2023-04-25 19:00:08 [DEBUG] Found 2580 proxies from ListProxyBuilder (proxy_builder.py:75)
2023-04-25 19:00:08 [DEBUG] Proxies len: 2661 (proxy_handler.py:160)
2023-04-25 19:00:08 [DEBUG] Proxy Handler initialized with 2661 proxies (proxy_handler.py:82)
2023-04-25 19:00:08 [DEBUG] Useragents loaded from file: /home/dnllns/Documentos/repositorios/olivia-finder/olivia_finder/olivia_finder/myrequests/data/useragents.txt (useragent_handler.py:35)
2023-04-25 19:00:08 [INFO] Workers created (request_handler.py:40)
2023-04-25 19:00:08 [INFO] Number of workers: 1 (request_handler.py:41)
2023-04-25 19:00:08 [DEBUG] Worker 0: Got job from queue
Job key: networkx
url: https://www.pypi.org/project/networkx/ (request_worker.py:67)
...
url: None (request_worker.py:67)
2023-04-25 19:00:13 [INFO] Joining worker 1 (request_handler.py:67)
2023-04-25 19:00:13 [INFO] Joining worker 2 (request_handler.py:67)
2023-04-25 19:00:13 [INFO] Joining worker 3 (request_handler.py:67)
2023-04-25 19:00:13 [INFO] Worker 0 finished (request_handler.py:73)
2023-04-25 19:00:13 [INFO] Worker 1 finished (request_handler.py:73)
2023-04-25 19:00:13 [INFO] Worker 2 finished (request_handler.py:73)
2023-04-25 19:00:13 [INFO] Worker 3 finished (request_handler.py:73)
```


## Module utilities

Includes some utilities to work with the module

## Module exceptions

Includes some exceptions to work with the module

'''