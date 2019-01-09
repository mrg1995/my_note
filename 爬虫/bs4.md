# 爬取策略
在爬虫系统中，待抓取URL队列是很重要的一部分。待抓取URL队列中的URL以什么样的顺序排列也是一个很重要的问题，因为这涉及到先抓取那个页面，后抓取哪个页面。而决定这些URL排列顺序的方法，叫做抓取策略。下面重点介绍几种常见的抓取策略：
### 深度优先遍历策略
深度优先遍历策略是指网络爬虫会从起始页开始，一个链接一个链接跟踪下去，处理完这条线路之后再转入下一个起始页，继续跟踪链接。我们以下面的图为例：遍历的路径：A-F-G E-H-I B C D
```python
#!C:\Python36\python.exe
# -*- coding:utf-8 -*-
'''
@Time    : 2018/5/29 17:15
@Author  : Fate
@File    : 01deepSpider.py
'''
import re

import requests

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

hrefre = "<a.*href=\"(https?://.*?)\".*>"


def getPage(url):
    '''
    获取html
    :param url:
    :return: html源码
    '''
    html = requests.get(url, headers=header)
    return html.text


def getUrl(url):
    '''
    获取url
    :param url:
    :return: URLList
    '''
    html = getPage(url)
    urllist = re.findall(hrefre, html)
    return urllist


def deepSpider(url, depth):
    '''
    深度爬虫
    :param url:
    :param depth:深度控制
    :return:
    '''
    print("\t\t\t" * depthDict[url], "爬取了第%d级页面：%s" % (depthDict[url], url))

    if depthDict[url] > depth:
        return  # 超出深度则跳出
    sonlist = getUrl(url)
    for i in sonlist:
        if i not in depthDict:
        	depthDict[i] = depthDict[url] + 1  # 层级+1
        	deepSpider(i, depth)


if __name__ == '__main__':
    depthDict = {}  # 爬虫层级控制
    # 起始url
    startUrl = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=岛国邮箱"
    depthDict[startUrl] = 1
    deepSpider(startUrl, 4)

```

### 宽度优先遍历策略
宽度优先遍历策略的基本思路是，将新下载网页中发现的链接直接**待抓取URL队列的末尾。也就是指网络爬虫会先抓取起始网页中链接的所有网页，然后再选择其中的一个链接网页，继续抓取在此网页中链接的所有网页。还是以上面的图为例：遍历路径：A-B-C-D-E-F-G-H-I
```python
# coding:utf-8
import re

import requests

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

hrefre = "<a.*href=\"(https?://.*?)\".*>"


def getUrl(url):
    '''
    获取网页的全部url
    :param url:
    :return: url列表
    '''
    html = getPage(url)
    '''
    <a data-click="{}" href="http://www.baidu.com/" fasdf>...</a>
    '''
    urlre = "<a.*href=\"(https?://.*?)\".*>"
    urllist = re.findall(urlre, html)
    return urllist


def getPage(url):
    '''
    抓取网页html
    :param url:
    :return: HTML源码
    '''
    html = requests.get(url, headers=header).text
    return html


def vastSpider(depth):
    while len(urlList) > 0:
        url = urlList.pop(0)  # 弹出首个url
        print("\t\t\t" * depthDict[url], "抓取了第%d级页面：%s" % (depthDict[url], url))

        if depthDict[url] < depth:
            sonList = getUrl(url)
            for s in sonList:
                if s not in depthDict: # 去重
                    depthDict[s] = depthDict[url] + 1
                    urlList.append(s)


if __name__ == '__main__':
    # 去重
    urlList = []  # url列表

    depthDict = {}
    starUrl = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=岛国邮箱"
    depthDict[starUrl] = 1
    urlList.append(starUrl)
    vastSpider(4)


```
# 页面解析和数据提取
一般来讲对我们而言，需要抓取的是某个网站或者某个应用的内容，提取有用的价值。内容一般分为两部分，非结构化的数据 和 结构化的数据。

- 非结构化数据：先有数据，再有结构，
- 结构化数据：先有结构、再有数据
###不同类型的数据，我们需要采用不同的方式来处理。
- 非结构化的数据处理
```文本、电话号码、邮箱地址
正则表达式
HTML 文件
正则表达式
XPath
CSS选择器
```

- 结构化的数据处理
```JSON 文件
JSON Path
转化成Python类型进行操作（json类）
XML 文件
转化成Python类型（xmltodict）
XPath
CSS选择器
正则表达式
```
#2.Beautiful Soup 4.2.0 文档
https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

- 爬取智联招聘岗位数量
```python
import urllib
from bs4 import BeautifulSoup
from urllib import request


def download(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers) # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read() # 打开请求，抓取数据
    soup = BeautifulSoup(data, "html5lib", from_encoding="utf-8")
    # findall
    # 获取岗位数量的多种查找方式
    spanlist = soup.find_all("span", class_="search_yx_tj")
    print(spanlist)
    print(spanlist[0].em.string)
    print(soup.select('.search_yx_tj'))
    print(((soup.select('.search_yx_tj')[0]).select("em")[0]).get_text())
    print(((soup.select('span[class="search_yx_tj"]')[0]).select("em")[0]).get_text())


download("http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python&sm=0&p=1")
```
- 爬取股票基金

```python
#!C:\Python36\python.exe
# -*- coding:utf-8 -*-
'''
@Time    : 2018/5/29 17:47
@Author  : Fate
@File    : aaa.py
'''
import urllib
from urllib import request
from bs4 import BeautifulSoup

stockList = []


def download(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers)  # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read()  # 打开请求，抓取数据
    soup = BeautifulSoup(data, "html5lib", from_encoding="gb2312")
    mytable = soup.select("#datalist")
    for line in mytable[0].find_all("tr"):
        print(line.get_text())  # 提取每一个行业

        print(line.select("td:nth-of-type(3)")[0].text) # 提取具体的某一个


if __name__ == '__main__':
    download("http://quote.stockstar.com/fund/stock_3_1_2.html")

```
- 爬取腾讯岗位说明
```python

#encoding:utf-8
import urllib
from urllib import request
from bs4 import BeautifulSoup


def download(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers) # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read() # 打开请求，抓取数据
    soup = BeautifulSoup(data, "html5lib")
    print(soup)
    data = soup.find_all("ul", class_="squareli")
    for dataline in data:
        for linedata in dataline.find_all("li"):
            print(linedata.string)
        
    data = soup.select('ul[class="squareli"]')
    for dataline in data:
        for linedata in dataline.select("li"):
            print(linedata.get_text())


download("https://hr.tencent.com/position_detail.php?id=37446&keywords=&tid=0&lid=0")
```
- 获取腾讯岗位列表
```python
#encoding:utf-8
import urllib
from urllib import request
from bs4 import BeautifulSoup


def download(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib.request.Request(url, headers=headers) # 请求，修改，模拟http.
    data = urllib.request.urlopen(request).read() # 打开请求，抓取数据
    soup = BeautifulSoup(data, "html5lib")
    
    data = soup.find_all("table", class_="tablelist")
    for line in data[0].find_all("tr", class_=["even", "odd"]):
        print(line.find_all("td")[0].a["href"])
        for data in line.find_all("td"):
            print(data.string)


download("http://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start=100#a")
```
### 插入数据库

```python
#!C:\Python36\python.exe
# -*- coding:utf-8 -*-
'''
@Time    : 2018/5/30 12:57
@Author  : Fate
@File    : insertMySQL.py
'''
import pymysql

# 连接数据库
conn = pymysql.connect(host="127.0.0.1", user='root', password="123456",
                       database='fate', port=3306,
                       charset='utf8')

print(conn)

# 游标
cursor = conn.cursor()

with open("tencet.txt", 'r', encoding='utf-8', errors='ignore') as f:
    jobList = f.readlines()
    for job in jobList:
        job = job.split(",")
        # print(job[0][1:])
        # print(job[4][:-2])
        try:
            sql = "insert into Tencent(jobName, jobAddr, jobType, jobNum, jobInfo) VALUES(%s,%s,%s,%s,%s) " % (
                job[0][1:], job[1], job[2], job[3], job[4][:-2])
            print(sql)
            cursor.execute(sql)
            conn.commit()
        except:
            pass

cursor.close()
conn.close()
# print("%s======%r" % ("asdfasdf","asdfasfd"))

```



# 作业

http://www.dataduoduo.com/