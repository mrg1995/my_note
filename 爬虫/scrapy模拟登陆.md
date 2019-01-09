# scrapy模拟登陆

###注意：模拟登陆时，必须保证settings.py里的COOKIES_ENABLED(Cookies中间件) 处于开启状态

> `COOKIES_ENABLED = True`或`# COOKIES_ENABLED = False`

#### 策略一：直接POST数据（比如需要登陆的账户信息)

> 只要是需要提供post数据的，就可以用这种方法。下面示例里post的数据是账户密码：

- 可以使用yield scrapy.FormRequest(url, formdata, callback)方法发送POST请求。
- 如果希望程序执行一开始就发送POST请求，可以重写Spider类的start_requests(self)方法，并且不再调用start_urls里的url。

```python
class mySpider(scrapy.Spider):
    # start_urls = ["http://www.example.com/"]


    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'


        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "mr_mao_hacker@163.com", "password" : "axxxxxxxe"},
            callback = self.parse_page
        )
    def parse_page(self, response):
        # do something
```

#### 策略二：标准的模拟登陆步骤

> 正统模拟登录方法：
>
> 1. 首先发送登录页面的get请求，获取到页面里的登录必须的参数（比如说zhihu登陆界面的 _xsrf）
> 2. 然后和账户密码一起post到服务器，登录成功
> 3. 使用FormRequest.from_response()方法[模拟用户登录]

```python
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
        response,
        formdata={'username': 'john', 'password': 'secret'},
        callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

# continue scraping with authenticated session...
```



**模拟浏览器登录**

**start_requests()方法，可以返回一个请求给爬虫的起始网站，这个返回的请求相当于start_urls，start_requests()返回的请求会替代start_urls里的请求**

**Request()get请求，可以设置，url、cookie、回调函数**

**FormRequest.from_response()表单post提交，第一个必须参数，上一次响应cookie的response对象，其他参数，cookie、url、表单内容等**

**yield Request()可以将一个新的请求返回给爬虫执行**

**在发送请求时cookie的操作，** **meta={'cookiejar':1}表示开启cookie记录，首次请求时写在Request()里** **meta={'cookiejar':response.meta['cookiejar']}表示使用上一次response的cookie，写在FormRequest.from_response()里post授权** **meta={'cookiejar':True}表示使用授权后的cookie访问需要登录查看的页面**

### 正统模拟登录方法

```python
import scrapy

# 正统模拟登录方法：
# 首先发送登录页面的get请求，获取到页面里的登录必须的参数，比如说zhihu的 _xsrf
# 然后和账户密码一起post到服务器，登录成功

    # 第二种标准
    def parse(self, response):
        print(response.body.decode('utf-8'), "@@" * 40)

        yield scrapy.FormRequest.from_response(response,
                                               formdata={
                                                   "email": "18588403840",
                                                   # "icode": icode,
                                                   "origURL": "http://www.renren.com/422167102/profile",
                                               # 个人主页，http://www.renren.com/home 首页
                                                   "domain": "renren.com",
                                                   "key_id": "1",
                                                   "captcha_type": "web_login",
                                                   "password": "97bfc03b0eec4df7c76eaec10cd08ea57b01eefd0c0ffd4c0e5061ebd66460d9",
                                                   "rkey": "26615a8e93fee56fc1fb3d679afa3cc4",
                                                   "f": ""
                                               },
                                               dont_filter=True,
                                               headers=self.headers,
                                               callback=self.get_page)

    def get_page(self, response):
        print("===================", response.url)
        print(response.body.decode('utf-8'))

        url = "http://www.renren.com/353111356/profile"

        yield scrapy.Request(url, callback=self.get_info)

    def get_info(self, response):
        print('*******' * 30)
        print(response.body.decode('utf-8'))
```

```python
# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MyrenSpider(CrawlSpider):
    name = 'myren'
    allowed_domains = ['renren.com']
    start_urls = ["http://www.renren.com/353111356/profile"]

    rules = [Rule(LinkExtractor(allow=('(\d+)/profile')), callback='get_info', follow=True)]

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }

    def start_requests(self):
        yield scrapy.Request(url="http://www.renren.com/", meta={'cookiejar': 1}, callback=self.post_login)

    # 第二种标准
    def post_login(self, response):
        yield scrapy.FormRequest.from_response(response,
                                               url="http://www.renren.com/PLogin.do",
                                               meta={'cookiejar': response.meta['cookiejar']},
                                               # 在之前需要打开 meta = {'cookiejar' : 1}
                                               headers=self.headers,
                                               formdata={
                                                   "email": "18588403840",
                                                   "password": "Changeme_123"
                                               },
                                               dont_filter=True,

                                               callback=self.after_login)

    def after_login(self, response):
        for url in self.start_urls:
            # yield self.make_requests_from_url(url)
            yield scrapy.Request(url, meta={'cookiejar': response.meta['cookiejar']})

    def get_info(self, response):
        print('*******' * 30)
        print(response.body.decode('utf-8'))
        
    def _requests_to_follow(self, response):  
    """重写加入cookiejar的更新"""  
    if not isinstance(response, HtmlResponse):  
        return  
    seen = set()  
    for n, rule in enumerate(self._rules):  
        links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]  
        if links and rule.process_links:  
            links = rule.process_links(links)  
        for link in links:  
            seen.add(link)  
            r = Request(url=link.url, callback=self._response_downloaded)  
            # 下面这句是我重写的  
            r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])  
            yield rule.process_request(r)  




```



#### 策略三：直接使用保存登陆状态的Cookie模拟登陆

> 如果实在没办法了，可以用这种方法模拟登录，虽然麻烦一点，但是成功率100%

ChangeCookies

```python
#!C:\Python36\python.exe
# -*- coding:utf-8 -*-
'''
@Time    : 2018/6/7 19:37
@Author  : Fate
@File    : ChangeCookies.py
'''
class transCookie:

    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].strip()
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = "你的cookie"
    trans = transCookie(cookie)
    print(trans.stringToDict())

```



```python
# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = "renren"
    allowed_domains = ["renren.com"]
    start_urls = [
        'http://www.renren.com/111111',
        'http://www.renren.com/222222',
        'http://www.renren.com/333333',
        ]


    cookies = {
    "anonymid" : "ixrna3fysufnwv",
    "_r01_" : "1",
    "ap" : "327550029",
    "JSESSIONID" : "abciwg61A_RvtaRS3GjOv",
    "depovince" : "GW",
    "springskin" : "set",
    "jebe_key" : "f6fb270b-d06d-42e6-8b53-e67c3156aa7e%7Cc13c37f53bca9e1e7132d4b58ce00fa3%7C1484060607478%7C1%7C1486198628950",
    "t" : "691808127750a83d33704a565d8340ae9",
    "societyguester" : "691808127750a83d33704a565d8340ae9",
    "id" : "327550029",
    "xnsid" : "f42b25cf",
    "loginfrom" : "syshome"
    }


    # 可以重写Spider类的start_requests方法，附带Cookie值，发送POST请求
    def start_requests(self):
        return [scrapy.FormRequest(url, cookies = self.cookies, callback = self.parse)]


    # 处理响应内容
    def parse(self, response):
        print "===========" + response.url
        with open("deng.html", "w") as filename:
            filename.write(response.body)
```

# 使用selenium插件

```python
class TaobaoSpider(scrapy.Spider):
    name = 'mytaobao'

    allowed_domains = ['taobao.com']
    start_urls = ['https://login.m.taobao.com/login.htm',
                  "http://h5.m.taobao.com/mlapp/olist.html?spm=a2141.7756461.2.6"]

    def __init__(self):  # 初始化
        self.browser = None
        self.cookies = None
        super(JjSpider, self).__init__()  # 传递给父类
        
    def parse(self, response):
        # 打印链接，打印网页源代码

        print(response.url)
        print(response.body.decode("utf-8", "ignore"))
```

```python
class LoginMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == "mytaobao":  # 指定仅仅处理这个名称的爬虫
            if request.url.find("login") != -1:  # 判断是否登陆页面
                mobilesetting = {"deviceName": "iPhone 6 Plus"}
                options = webdriver.ChromeOptions()  # 浏览器选项
                options.add_experimental_option("mobileEmulation", mobilesetting)  # 模拟手机
                spider.browser = webdriver.Chrome(chrome_options=options)  # 创建一个浏览器
                spider.browser.set_window_size(400, 800)  # 配置手机大小

                spider.browser.get(request.url)  # 爬虫访问链接
                time.sleep(3)
                print("login访问", request.url)
                username = spider.browser.find_element_by_id("username")
                password = spider.browser.find_element_by_id("password")
                time.sleep(1)
                username.send_keys("2403239393@qq.com")  # 账户
                time.sleep(2)
                password.send_keys("bama100")  # 密码
                time.sleep(2)
                click = spider.browser.find_element_by_id("btn-submit")
                click.click()
                time.sleep(18)
                spider.cookies = spider.browser.get_cookies()  # 抓取全部的cookie
                # spider.browser.close()

                return HtmlResponse(url=spider.browser.current_url,  # 当前连接
                                    body=spider.browser.page_source,  # 源代码
                                    encoding="utf-8")  # 返回页面信息
            else:
                # spider.browser.get(request.url)
                # request.访问，调用selenium cookie
                # request模拟访问。统一selenium，慢，request,不能执行js
                print("request  访问")
                req = requests.session()  # 会话
                for cookie in spider.cookies:
                    req.cookies.set(cookie['name'], cookie["value"])
                req.headers.clear()  # 清空头
                newpage = req.get(request.url)
                print("---------------------")
                print(request.url)
                print("---------------------")
                print(newpage.text)
                print("---------------------")
                # 页面
                time.sleep(3)
                return HtmlResponse(url=request.url,  # 当前连接
                                    body=newpage.text,  # 源代码
                                    encoding="utf-8")  # 返回页面信息
```

