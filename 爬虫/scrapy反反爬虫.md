#反反爬虫相关机制

##### Some websites implement certain measures to prevent bots from crawling them, with varying degrees of sophistication. Getting around those measures can be difficult and tricky, and may sometimes require special infrastructure. Please consider contacting commercial support if in doubt.

#### (有些些网站使用特定的不同程度的复杂性规则防止爬虫访问，绕过这些规则是困难和复杂的，有时可能需要特殊的基础设施，如果有疑问，请联系商业支持。)

> 来自于Scrapy官方文档描述：[http://doc.scrapy.org/en/master/topics/practices.html#avoiding-getting-banned](https://legacy.gitbook.com/book/fategithub/pythonspider/edit#)

### 通常防止爬虫被反主要有以下几个策略：

- 动态设置User-Agent（随机切换User-Agent，模拟不同用户的浏览器信息）

- 添加请求头的多种方式

  - 方法1：

    修改setting.py中的User-Agent

    ```python
    # Crawl responsibly by identifying yourself (and your website) on the user-agent
    USER_AGENT = 'Hello World'
    ```

  - 方法2.

    修改setting中的

    DEFAULT_REQUEST_HEADERS

    ```python
    # Override the default request headers:
     DEFAULT_REQUEST_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent':'Hello World'
     }
    ```

  - 方法3.

    在代码中修改。

    ```python
    class HeadervalidationSpider(scrapy.Spider):
        name = 'headervalidation'
        allowed_domains = ['helloacm.com']
    ```


```python
    def start_requests(self):
        header={'User-Agent':'Hello World'}
        yield scrapy.Request(url='http://helloacm.com/api/user-agent/',headers=header,callback=self.parse)

    def parse(self, response):
        print '*'*20
        print response.body
        print '*'*20
​```
```

- 禁用Cookies（也就是不启用cookies middleware，不向Server发送cookies，有些网站通过cookie的使用发现爬虫行为）

  - 可以通过

    `COOKIES_ENABLED`

    控制 CookiesMiddleware 开启或关闭

- 设置延迟下载（防止访问过于频繁，设置为 2秒 或更高）

- Google Cache 和 Baidu Cache：如果可能的话，使用谷歌/百度等搜索引擎服务器页面缓存获取页面数据。

- 使用IP地址池：VPN和代理IP，现在大部分网站都是根据IP来ban的。

- 使用[Crawlera](https://legacy.gitbook.com/book/fategithub/pythonspider/edit#)（专用于爬虫的代理组件），正确配置和设置下载中间件后，项目所有的request都是通过crawlera发出。

  ```python
    DOWNLOADER_MIDDLEWARES = {
        'scrapy_crawlera.CrawleraMiddleware': 600
    }
  ```


    CRAWLERA_ENABLED = True
    CRAWLERA_USER = '注册/购买的UserKey'
    CRAWLERA_PASS = '注册/购买的Password'
  ```

## 设置下载中间件（Downloader Middlewares）

下载中间件是处于引擎(crawler.engine)和下载器(crawler.engine.download())之间的一层组件，可以有多个下载中间件被加载运行。

1. 当引擎传递请求给下载器的过程中，下载中间件可以对请求进行处理 （例如增加http header信息，增加proxy信息等）；
2. 在下载器完成http请求，传递响应给引擎的过程中， 下载中间件可以对响应进行处理（例如进行gzip的解压等）

要激活下载器中间件组件，将其加入到 DOWNLOADER_MIDDLEWARES 设置中。 该设置是一个字典(dict)，键为中间件类的路径，值为其中间件的顺序(order)。

这里是一个例子:

​```python
DOWNLOADER_MIDDLEWARES = {
    'mySpider.middlewares.MyDownloaderMiddleware': 543,
}
  ```

编写下载器中间件十分简单。每个中间件组件是一个定义了以下一个或多个方法的Python类:

```
class scrapy.contrib.downloadermiddleware.DownloaderMiddleware
```

### process_request(self, request, spider)

- 当每个request通过下载中间件时，该方法被调用。

- process_request() 必须返回以下其中之一：一个 None 、一个 Response 对象、一个 Request 对象或 raise IgnoreRequest:

  - 如果其返回 None ，Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用， 该request被执行(其response被下载)。
  - 如果其返回 Response 对象，Scrapy将不会调用 任何 其他的 process_request() 或 process_exception() 方法，或相应地下载函数； 其将返回该response。 已安装的中间件的 process_response() 方法则会在每个response返回时被调用。
  - 如果其返回 Request 对象，Scrapy则停止调用 process_request方法并重新调度返回的request。当新返回的request被执行后， 相应地中间件链将会根据下载的response被调用。
  - 如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)。

- 参数:

  - `request (Request 对象)`

    – 处理的request

  - `spider (Spider 对象)`

    – 该request对应的spider

### process_response(self, request, response, spider)

当下载器完成http请求，传递响应给引擎的时候调用

- process_request() 必须返回以下其中之一: 返回一个 Response 对象、 返回一个 Request 对象或raise一个 IgnoreRequest 异常。

  - 如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理。
  - 如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样。
  - 如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。

- 参数:

  - `request (Request 对象)`

    – response所对应的request

  - `response (Response 对象)`

    – 被处理的response

  - `spider (Spider 对象)`

    – response所对应的spider

## 使用案例：

#### 1. 创建`middlewares.py`文件。

Scrapy代理IP、Uesr-Agent的切换都是通过`DOWNLOADER_MIDDLEWARES`进行控制，我们在`settings.py`同级目录下创建`middlewares.py`文件，包装所有请求。

```python
# middlewares.py


#!/usr/bin/env python
# -*- coding:utf-8 -*-


import random

from settings import USER_AGENTS
from settings import PROXIES


# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)

# 随机代理IP
class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)

        request.meta['proxy'] = "http://" + proxy['ip_port']
   
```



#### 2. 修改settings.py配置USER_AGENTS和PROXIES

- 添加USER_AGENTS：

```python
　USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
```

- 添加代理IP设置PROXIES：

  免费代理IP可以网上搜索，或者付费购买一批可用的私密代理IP：

```python
PROXIES = [
    {'ip_port': '111.8.60.9:8123'},
    {'ip_port': '101.71.27.120:80'},
    {'ip_port': '122.96.59.104:80'},
    {'ip_port': '122.224.249.122:8088'},
]
```

- 除非特殊需要，禁用cookies，防止某些网站根据Cookie来封锁爬虫。

```
COOKIES_ENABLED = False
```

- 设置下载延迟

```
DOWNLOAD_DELAY = 3
```

- 最后设置setting.py里的DOWNLOADER_MIDDLEWARES，添加自己编写的下载中间件类。

```python
DOWNLOADER_MIDDLEWARES = {
    #'mySpider.middlewares.MyCustomDownloaderMiddleware': 543,
    'mySpider.middlewares.RandomUserAgent': 81,
    'mySpider.middlewares.ProxyMiddleware': 100
}
```

# Settings

Scrapy设置(settings)提供了定制Scrapy组件的方法。可以控制包括核心(core)，插件(extension)，pipeline及spider组件。比如 设置Json Pipeliine、LOG_LEVEL等。

参考文档：[http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/settings.html#topics-settings-ref](https://legacy.gitbook.com/book/fategithub/pythonspider/edit#)

## 内置设置参考手册

- `REACTOR_THREADPOOL_MAXSIZE = 20`

  - ##### 增加线程池数量，默认10条

- `IMAGES_STORE = '/path'`：下载图片，图片存储在文件中（一个图片一个文件），并使用它们URL的[SHA1 hash](https://legacy.gitbook.com/book/fategithub/pythonspider/edit#)作为文件名

- `IMAGES_EXPIRES = 30`：图片失效时间（天）,避免下载最近已经下载的图片

- ```python
  # 图片缩略图
  IMAGES_THUMBS = {
      'samll' : (50, 50),
      'big' : (270, 270)
  }
  MEDIA_ALLOW_REDIRECTS = True # 重定向
  ```

```python
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item




class MzituScrapyPipeline(ImagesPipeline):


    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['name']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename


    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for img_url in item['image_urls']:
            referer = item['url']
            yield Request(img_url, meta={'item': item})




    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
```
### BOT_NAME

默认: `'scrapybot'`

Scrapy项目实现的bot的名字(也未项目名称)。 这将用来构造默认 User-Agent，同时也用来log。

当您使用 [`startproject`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#std:command-startproject) 命令创建项目时其也被自动赋值。

### CONCURRENT_ITEMS

默认: `100`

Item Processor(即 [Item Pipeline](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/item-pipeline.html#topics-item-pipeline)) 同时处理(每个response的)item的最大值。

### CONCURRENT_REQUESTS

默认: `16`

Scrapy downloader 并发请求(concurrent requests)的最大值。

### CONCURRENT_REQUESTS_PER_DOMAIN

默认: `8`

对单个网站进行并发请求的最大值。

### CONCURRENT_REQUESTS_PER_IP

默认: `0`

对单个IP进行并发请求的最大值。如果非0，则忽略 [`CONCURRENT_REQUESTS_PER_DOMAIN`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-CONCURRENT_REQUESTS_PER_DOMAIN) 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站。

该设定也影响 [`DOWNLOAD_DELAY`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOAD_DELAY): 如果 [`CONCURRENT_REQUESTS_PER_IP`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-CONCURRENT_REQUESTS_PER_IP) 非0，下载延迟应用在IP而不是网站上。

### DEFAULT_ITEM_CLASS

默认: `'scrapy.item.Item'`

[the Scrapy shell](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/shell.html#topics-shell) 中实例化item使用的默认类。

### DEFAULT_REQUEST_HEADERS

默认:

```
{
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

```

Scrapy HTTP Request使用的默认header。由 [`DefaultHeadersMiddleware`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/downloader-middleware.html#scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware) 产生。

### DEPTH_LIMIT

默认: `0`

爬取网站最大允许的深度(depth)值。如果为0，则没有限制。

### DEPTH_PRIORITY

默认: `0`

整数值。用于根据深度调整request优先级。

如果为0，则不根据深度进行优先级调整。

### DEPTH_STATS

默认: `True`

是否收集最大深度数据。

### DEPTH_STATS_VERBOSE

默认: `False`

是否收集详细的深度数据。如果启用，每个深度的请求数将会被收集在数据中。

### DNSCACHE_ENABLED

默认: `True`

是否启用DNS内存缓存(DNS in-memory cache)。

### DOWNLOADER

默认: `'scrapy.core.downloader.Downloader'`

用于crawl的downloader.

### DOWNLOADER_MIDDLEWARES

默认:: `{}`

保存项目中启用的下载中间件及其顺序的字典。 更多内容请查看 [激活下载器中间件](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/downloader-middleware.html#topics-downloader-middleware-setting) 。

### DOWNLOADER_MIDDLEWARES_BASE

默认:

```
{
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
    'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
}

```

包含Scrapy默认启用的下载中间件的字典。 永远不要在项目中修改该设定，而是修改[`DOWNLOADER_MIDDLEWARES`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOADER_MIDDLEWARES) 。更多内容请参考 [激活下载器中间件](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/downloader-middleware.html#topics-downloader-middleware-setting).

### DOWNLOADER_STATS

默认: `True`

是否收集下载器数据。

### DOWNLOAD_DELAY

默认: `0`

下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度， 减轻服务器压力。同时也支持小数:

```
DOWNLOAD_DELAY = 0.25    # 250 ms of delay

```

该设定影响(默认启用的) [`RANDOMIZE_DOWNLOAD_DELAY`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-RANDOMIZE_DOWNLOAD_DELAY) 设定。 默认情况下，Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值 * [`DOWNLOAD_DELAY`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOAD_DELAY) 的结果作为等待间隔。

当 [`CONCURRENT_REQUESTS_PER_IP`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-CONCURRENT_REQUESTS_PER_IP) 非0时，延迟针对的是每个ip而不是网站。

另外您可以通过spider的 `download_delay` 属性为每个spider设置该设定。

### DOWNLOAD_HANDLERS

默认: `{}`

保存项目中启用的下载处理器(request downloader handler)的字典。 例子请查看 DOWNLOAD_HANDLERS_BASE 。

### DOWNLOAD_HANDLERS_BASE

默认:

```
{
    'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
}

```

保存项目中默认启用的下载处理器(request downloader handler)的字典。 永远不要在项目中修改该设定，而是修改 `DOWNLOADER_HANDLERS` 。

如果需要关闭上面的下载处理器，您必须在项目中的 [`DOWNLOAD_HANDLERS`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOAD_HANDLERS) 设定中设置该处理器，并为其赋值为 None 。 例如，关闭文件下载处理器:

```
DOWNLOAD_HANDLERS = {
    'file': None,
}

```

### DOWNLOAD_TIMEOUT

默认: `180`

下载器超时时间(单位: 秒)。

### DUPEFILTER_CLASS

默认: `'scrapy.dupefilter.RFPDupeFilter'`

用于检测过滤重复请求的类。

默认的 (`RFPDupeFilter`) 过滤器基于 `scrapy.utils.request.request_fingerprint` 函数生成的请求fingerprint(指纹)。 如果您需要修改检测的方式，您可以继承 `RFPDupeFilter` 并覆盖其 `request_fingerprint` 方法。 该方法接收 [`Request`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/request-response.html#scrapy.http.Request) 对象并返回其fingerprint(一个字符串)。

### DUPEFILTER_DEBUG

默认: `False`

默认情况下， `RFPDupeFilter` 只记录第一次重复的请求。 设置 [`DUPEFILTER_DEBUG`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DUPEFILTER_DEBUG) 为 `True` 将会使其记录所有重复的requests。

### EDITOR

默认: depends on the environment

执行 [`edit`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#std:command-edit) 命令编辑spider时使用的编辑器。 其默认为 `EDITOR` 环境变量。如果该变量未设置，其默认为 `vi` (Unix系统) 或者 IDLE编辑器(Windows)。

### EXTENSIONS

默认:: `{}`

保存项目中启用的插件及其顺序的字典。

### EXTENSIONS_BASE

默认:

```
{
    'scrapy.contrib.corestats.CoreStats': 0,
    'scrapy.webservice.WebService': 0,
    'scrapy.telnet.TelnetConsole': 0,
    'scrapy.contrib.memusage.MemoryUsage': 0,
    'scrapy.contrib.memdebug.MemoryDebugger': 0,
    'scrapy.contrib.closespider.CloseSpider': 0,
    'scrapy.contrib.feedexport.FeedExporter': 0,
    'scrapy.contrib.logstats.LogStats': 0,
    'scrapy.contrib.spiderstate.SpiderState': 0,
    'scrapy.contrib.throttle.AutoThrottle': 0,
}

```

可用的插件列表。需要注意，有些插件需要通过设定来启用。默认情况下， 该设定包含所有稳定(stable)的内置插件。

更多内容请参考 [extensions用户手册](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions) 及 [所有可用的插件](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions-ref) 。

### ITEM_PIPELINES

默认: `{}`

保存项目中启用的pipeline及其顺序的字典。该字典默认为空，值(value)任意。 不过值(value)习惯设定在0-1000范围内。

为了兼容性，[`ITEM_PIPELINES`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-ITEM_PIPELINES) 支持列表，不过已经被废弃了。

样例:

```
ITEM_PIPELINES = {
    'mybot.pipelines.validate.ValidateMyItem': 300,
    'mybot.pipelines.validate.StoreMyItem': 800,
}

```

### ITEM_PIPELINES_BASE

默认: `{}`

保存项目中默认启用的pipeline的字典。 永远不要在项目中修改该设定，而是修改 [`ITEM_PIPELINES`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-ITEM_PIPELINES)。

### LOG_ENABLED

默认: `True`

是否启用logging。

### LOG_ENCODING

默认: `'utf-8'`

logging使用的编码。

### LOG_FILE

默认: `None`

logging输出的文件名。如果为None，则使用标准错误输出(standard error)。

### LOG_LEVEL

默认: `'DEBUG'`

log的最低级别。可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG。更多内容请查看 [Logging](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/logging.html#topics-logging) 。

### LOG_STDOUT

默认: `False`

如果为 `True` ，进程所有的标准输出(及错误)将会被重定向到log中。例如， 执行 `print 'hello'` ，其将会在Scrapy log中显示。

### MEMDEBUG_ENABLED

默认: `False`

是否启用内存调试(memory debugging)。

### MEMDEBUG_NOTIFY

默认: `[]`

如果该设置不为空，当启用内存调试时将会发送一份内存报告到指定的地址；否则该报告将写到log中。

样例:

```
MEMDEBUG_NOTIFY = ['user@example.com']

```

### MEMUSAGE_ENABLED

默认: `False`

Scope: `scrapy.contrib.memusage`

是否启用内存使用插件。当Scrapy进程占用的内存超出限制时，该插件将会关闭Scrapy进程， 同时发送email进行通知。

See [内存使用扩展(Memory usage extension)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions-ref-memusage).

### MEMUSAGE_LIMIT_MB

默认: `0`

Scope: `scrapy.contrib.memusage`

在关闭Scrapy之前所允许的最大内存数(单位: MB)(如果 MEMUSAGE_ENABLED为True)。 如果为0，将不做限制。

See [内存使用扩展(Memory usage extension)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions-ref-memusage).

### MEMUSAGE_NOTIFY_MAIL

默认: `False`

Scope: `scrapy.contrib.memusage`

达到内存限制时通知的email列表。

Example:

```
MEMUSAGE_NOTIFY_MAIL = ['user@example.com']

```

See [内存使用扩展(Memory usage extension)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions-ref-memusage).

### MEMUSAGE_REPORT

默认: `False`

Scope: `scrapy.contrib.memusage`

每个spider被关闭时是否发送内存使用报告。

查看 [内存使用扩展(Memory usage extension)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/extensions.html#topics-extensions-ref-memusage).

### MEMUSAGE_WARNING_MB

默认: `0`

Scope: `scrapy.contrib.memusage`

在发送警告email前所允许的最大内存数(单位: MB)(如果 MEMUSAGE_ENABLED为True)。 如果为0，将不发送警告。

### NEWSPIDER_MODULE

默认: `''`

使用 [`genspider`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#std:command-genspider) 命令创建新spider的模块。

样例:

```
NEWSPIDER_MODULE = 'mybot.spiders_dev'

```

### RANDOMIZE_DOWNLOAD_DELAY

默认: `True`

如果启用，当从相同的网站获取数据时，Scrapy将会等待一个随机的值 (0.5到1.5之间的一个随机值 * [`DOWNLOAD_DELAY`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOAD_DELAY))。

该随机值降低了crawler被检测到(接着被block)的机会。某些网站会分析请求， 查找请求之间时间的相似性。

随机的策略与 [wget](http://www.gnu.org/software/wget/manual/wget.html) `--random-wait` 选项的策略相同。

若 [`DOWNLOAD_DELAY`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-DOWNLOAD_DELAY) 为0(默认值)，该选项将不起作用。

### REDIRECT_MAX_TIMES

默认: `20`

定义request允许重定向的最大次数。超过该限制后该request直接返回获取到的结果。 对某些任务我们使用Firefox默认值。

### REDIRECT_MAX_METAREFRESH_DELAY

默认: `100`

有些网站使用 meta-refresh 重定向到session超时页面， 因此我们限制自动重定向到最大延迟(秒)。 =>有点不肯定:

### REDIRECT_PRIORITY_ADJUST

默认: `+2`

修改重定向请求相对于原始请求的优先级。 负数意味着更多优先级。

### ROBOTSTXT_OBEY

默认: `False`

Scope: `scrapy.contrib.downloadermiddleware.robotstxt`

如果启用，Scrapy将会尊重 robots.txt策略。更多内容请查看 [RobotsTxtMiddleware](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/downloader-middleware.html#topics-dlmw-robots) 。

### SCHEDULER

默认: `'scrapy.core.scheduler.Scheduler'`

用于爬取的调度器。

### SPIDER_CONTRACTS

默认:: `{}`

保存项目中启用用于测试spider的scrapy contract及其顺序的字典。 更多内容请参考 [Spiders Contracts](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/contracts.html#topics-contracts) 。

### SPIDER_CONTRACTS_BASE

默认:

```
{
    'scrapy.contracts.default.UrlContract' : 1,
    'scrapy.contracts.default.ReturnsContract': 2,
    'scrapy.contracts.default.ScrapesContract': 3,
}

```

保存项目中默认启用的scrapy contract的字典。 永远不要在项目中修改该设定，而是修改[`SPIDER_CONTRACTS`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-SPIDER_CONTRACTS) 。更多内容请参考 [Spiders Contracts](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/contracts.html#topics-contracts) 。

### SPIDER_MIDDLEWARES

默认:: `{}`

保存项目中启用的下载中间件及其顺序的字典。 更多内容请参考 [激活spider中间件](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spider-middleware.html#topics-spider-middleware-setting) 。

### SPIDER_MIDDLEWARES_BASE

默认:

```
{
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 700,
    'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': 900,
}

```

保存项目中默认启用的spider中间件的字典。 永远不要在项目中修改该设定，而是修改[`SPIDER_MIDDLEWARES`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/settings.html#std:setting-SPIDER_MIDDLEWARES) 。更多内容请参考 [激活spider中间件](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spider-middleware.html#topics-spider-middleware-setting).

### SPIDER_MODULES

默认: `[]`

Scrapy搜索spider的模块列表。

样例:

```
SPIDER_MODULES = ['mybot.spiders_prod', 'mybot.spiders_dev']

```

### STATS_CLASS

默认: `'scrapy.statscol.MemoryStatsCollector'`

收集数据的类。该类必须实现 [状态收集器(Stats Collector) API](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/api.html#topics-api-stats).

### STATS_DUMP

默认: `True`

当spider结束时dump [Scrapy状态数据](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/stats.html#topics-stats) (到Scrapy log中)。

更多内容请查看 [数据收集(Stats Collection)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/stats.html#topics-stats) 。

### STATSMAILER_RCPTS

默认: `[]` (空list)

spider完成爬取后发送Scrapy数据。更多内容请查看 `StatsMailer` 。

### TELNETCONSOLE_ENABLED

默认: `True`

表明 [telnet 终端](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/telnetconsole.html#topics-telnetconsole) (及其插件)是否启用的布尔值。

### TELNETCONSOLE_PORT

默认: `[6023, 6073]`

telnet终端使用的端口范围。如果设置为 `None` 或 `0` ， 则使用动态分配的端口。更多内容请查看[Telnet终端(Telnet Console)](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/telnetconsole.html#topics-telnetconsole) 。

### TEMPLATES_DIR

默认: scrapy模块内部的 `templates`

使用 [`startproject`](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#std:command-startproject) 命令创建项目时查找模板的目录。

### URLLENGTH_LIMIT

默认: `2083`

Scope: `contrib.spidermiddleware.urllength`

爬取URL的最大长度。更多关于该设定的默认值信息请查看:<http://www.boutell.com/newfaq/misc/urllength.html>

### USER_AGENT

默认: `"Scrapy/VERSION (+http://scrapy.org)"`

爬取的默认User-Agent，除非被覆盖。

## Logging

Scrapy提供了log功能，可以通过 logging 模块使用。

> 可以修改配置文件settings.py，任意位置添加下面两行，效果会清爽很多。

```python
LOG_ENABLED = True  # 开启
LOG_FILE = "TencentSpider.log" #日志文件名
LOG_LEVEL = "INFO" #日志级别
```

#### Log levels

- Scrapy提供5层logging级别:
- CRITICAL - 严重错误(critical)
- ERROR - 一般错误(regular errors)
- WARNING - 警告信息(warning messages)
- INFO - 一般信息(informational messages)
- DEBUG - 调试信息(debugging messages)

#### logging设置

通过在setting.py中进行以下设置可以被用来配置logging:

1. `LOG_ENABLED`

   默认: True，启用logging

2. `LOG_ENCODING`

   默认: 'utf-8'，logging使用的编码

3. `LOG_FILE`

   默认: None，在当前目录里创建logging输出文件的文件名

4. `LOG_LEVEL`

   默认: 'DEBUG'，log的最低级别

5. `LOG_STDOUT`

   默认: False 如果为 True，进程所有的标准输出(及错误)将会被重定向到log中。例如，执行 print "hello" ，其将会在Scrapy log中显示。

6. 日志模块已经被scrapy弃用，改用python自带日志模块

```python
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 设置输出格式
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"  # 设置时间格式
logging.basicConfig(filename='tianya.log', filemode='a+', format=LOG_FORMAT, datefmt=DATE_FORMAT)

logging.warning('错误')
```



## 爬取笔趣阁按层级存储

