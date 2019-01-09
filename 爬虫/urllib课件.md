

接下来，让我们真正迈向我们的爬虫之路吧！

# urllib2库的基本使用
所谓网页抓取，就是把URL地址中指定的网络资源从网络流中读取出来，保存到本地。 在Python中有很多库可以用来抓取网页，我们先学习urllib2。

urllib2 是 Python2.7 自带的模块(不需要下载，导入即可使用)

urllib2 官方文档：https://docs.python.org/2/library/urllib2.html

urllib2 源码：https://hg.python.org/cpython/file/2.7/Lib/urllib2.py

urllib2 在 python3.x 中被改为urllib.request

## urllib
- 01读取网页的三种方式
##urlopen
```angular2html
# 向指定的url发送请求，返回一个类文件对象，支持python文件操作
read()
readlines()
readline()
```

## User-Agent
有一些网站不喜欢被爬虫程序访问，所以会检测连接对象，如果是爬虫程序，也就是非人点击访问，它就会不让你继续访问，所以为了要让程序可以正常运行，需要隐藏自己的爬虫程序的身份。此时，我们就可以通过设置User Agent的来达到隐藏身份的目的，User Agent的中文名为用户代理，简称UA。

User Agent存放于Headers中，服务器就是通过查看Headers中的User Agent来判断是谁在访问。在Python中，如果不设置User Agent，程序将使用默认的参数，那么这个User Agent就会有Python的字样，如果服务器检查User Agent，那么没有设置User Agent的Python程序将无法正常访问网站。

常用消息头(详解http请求消息头)

-    Accept:text/html,image/*(告诉服务器，浏览器可以接受文本，网页图片)
-    Accept-Charaset:ISO-8859-1 [接受字符编码：iso-8859-1]
-    Accept-Encoding:gzip,compress[可以接受  gzip,compress压缩后数据]
-    Accept-Language:zh-cn[浏览器支持的语言]   
-    Host:localhost:8080[浏览器要找的主机]
-    Referer:http://localhost:8080/test/abc.html[告诉服务器我来自哪里,常用于防止下载，盗链]
-    User-Agent:Mozilla/4.0(Com...)[告诉服务器我的浏览器内核]
-    Cookie：[会话]
-    Connection:close/Keep-Alive [保持链接，发完数据后，我不关闭链接]
-    Date:[浏览器发送数据的请求时间]

-    02大灰狼冒充大白兔
```angular2html
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
request = urllib2.Request(url, headers=header) # 构造一个请求对象发送请求，伪装浏览器访问
```

## 添加更多的Header信息
在 HTTP Request 中加入特定的 Header，来构造一个完整的HTTP请求消息。

可以通过调用Request.add_header() 添加/修改一个特定的header 也可以通过调用Request.get_header()来查看已有的header。

添加一个特定的header
```
request.add_header("Connection", "keep-alive") # 一直活着
```
```python
request.add_header("Connection", "keep-alive") # 一直活着
print request.get_full_url() # 访问的网页链接
print request.get_host() # 服务器域名
print request.get_method() # get或post
print request.get_type() # http/https/ftp

response = urllib2.urlopen(request)
print response.code # 状态码200, 404，500
print response.info # 网页详细信息

data = response.read().decode("gb2312")
print response.code # 响应状态码
return data
```

我们都知道Http协议中参数的传输是"key=value"这种简直对形式的，如果要传多个参数就需要用“&”符号对键值对进行分割。如"?name1=value1&name2=value2"，这样在服务端在收到这种字符串的时候，会用“&”分割出每一个参数，然后再用“=”来分割出参数值。

- 03模拟百度搜索
  urllib.urlencode()

urllib 和 urllib2 都是接受URL请求的相关模块，但是提供了不同的功能。两个最显著的不同如下：
urllib 仅可以接受URL，不能创建 设置了headers 的Request 类实例；

但是 urllib 提供 urlencode 方法用来GET查询字符串的产生，而 urllib2 则没有。（这是 urllib 和 urllib2 经常一起使用的主要原因）

编码工作使用urllib的urlencode()函数，帮我们将key:value这样的键值对转换成"key=value"这样的字符串，解码工作可以使用urllib的unquote()函数。(注意，不是urllib2.urlencode())
```
urllib.urlencode(keyWord) # url编码
urllib.unquote(kw) # 解码
```

- 04模拟搜索爬取智联招聘抓取岗位数量
  http://sou.zhaopin.com/jobs/searchresult.ashx?jl=深圳&kw=python
```python
import re

mystr = """<span class=\"search_yx_tj\">
共<em>7287</em>个职位满足条件
</span>"""

myre = "<em>(\d+)</em>"
regex = re.compile(myre, re.I)

mylist = regex.findall(mystr)

print mylist[0]
```

## 抓取ajax数据
- 05抓取豆瓣电影排行
  https://movie.douban.com/tag/#/

## GET和POST请求
- 05POST爬取网易云音乐评论
```python
json_dict = json.loads(list)
print list
hot_comments = json_dict['hotComments'] # 热门评论

hot_comments_list = []
print("共有%d条热门评论!" % len(hot_comments))

for item in hot_comments:

    comment = item['content'] # 评论内容

    likedCount = item['likedCount'] # 点赞总数

    comment_time = item['time'] # 评论时间(时间戳)

    userID = item['user']['userId'] # 评论者id

    nickname = item['user']['nickname'] # 昵称

    avatarUrl = item['user']['avatarUrl'] # 头像地址
    comment_info = (comment, likedCount, comment_time, userID, nickname, avatarUrl)
    hot_comments_list.append(comment_info)
```
## 处理HTTPS请求 SSL证书验证
现在随处可见 https 开头的网站，urllib2可以为 HTTPS 请求验证SSL证书，就像web浏览器一样，如果网站的SSL证书是经过CA认证的，则能够正常访问，如：https://www.baidu.com/等...

如果SSL证书验证不通过，或者操作系统不信任服务器的安全证书，比如浏览器在访问12306网站如：https://www.12306.cn/mormhweb/的时候，会警告用户证书不受信任。（据说 12306 网站证书是自己做的，没有通过CA认证）
```python
import urllib
import urllib2
# 1. 导入Python SSL处理模块
import ssl

# 2. 表示忽略未经核实的SSL证书认证
context = ssl._create_unverified_context()

url = "https://www.12306.cn/mormhweb/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

request = urllib2.Request(url, headers = headers)

# 3. 在urlopen()方法里 指明添加 context 参数
response = urllib2.urlopen(request, context = context)

print response.read()
```

## 作业
模拟有道翻译
