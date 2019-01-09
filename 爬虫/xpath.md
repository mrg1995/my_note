# XPath
XPath即为XML路径语言，它是一种用来确定XML（标准通用标记语言的子集）文档中某部分位置的语言。XPath基于XML的树状结构，有不同类型的节点，包括元素节点，属性节点和文本节点，提供在数据结构树中找寻节点的能力。

# 什么是 XPath?
- XPath 使用路径表达式在 XML 文档中进行导航
- XPath 包含一个标准函数库
- XPath 是 XSLT 中的主要元素
- XPath 是一个 W3C 标准
# 使用xpath
### pip install lxml

```python
import lxml
from lxml import etree
```
# XPath Helper插件
chrome插件网：http://www.cnplugins.com/

添加插件

Ctrl + Shift + X打开或关闭插件

# XPath 术语
## 节点（Node）
在 XPath 中，有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档（根）节点。XML 文档是被作为节点树来对待的。树的根被称为文档节点或者根节点。

请看下面这个 XML 文档：
```
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>

    <book>
        <title lang="en">Harry Potter</title>
        <author>J K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>

</bookstore>
```
##基本值（或称原子值，Atomic value）
基本值是无父或无子的节点。

基本值的例子：
```
J K. Rowling

"en"
```
## 项目（Item）
项目是基本值或者节点。
## 节点关系
### 父（Parent）
每个元素以及属性都有一个父。
###子（Children）
元素节点可有零个、一个或多个子。
### 同胞（Sibling）
拥有相同的父的节点
###先辈（Ancestor）
某节点的父、父的父，等等。
### 后代（Descendant）
某个节点的子，子的子，等等。

# XPath 语法
```
<?xml version="1.0" encoding="UTF-8"?>

<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```



## 选取节点

XPath 使用路径表达式在 XML 文档中选取节点。节点是通过沿着路径或者 step 来选取的。 下面列出了最有用的路径表达式：

| 表达式  | 描述                            |
| ---- | ----------------------------- |
| /    | 从根节点选取。                       |
| //   | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .    | 选取当前节点。                       |
| ..   | 选取当前节点的父节点。                   |
| @    | 选取属性。                         |

在下面的表格中，我们已列出了一些路径表达式以及表达式的结果：

| 路径表达式           | 结果                                       |
| --------------- | ---------------------------------------- |
| bookstore       | 选取 bookstore 元素的所有子节点。                   |
| /bookstore      | 选取根元素 bookstore。注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！ |
| /bookstore/book | 选取属于 bookstore 的子元素的所有 book 元素。          |
| //book          | 选取所有 book 子元素，而不管它们在文档中的位置。              |
| bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。 |
| //@lang         | 选取名为 lang 的所有属性。                         |

## 谓语（Predicates）

谓语用来查找某个特定的节点或者包含某个指定的值的节点。

谓语被嵌在方括号中。

在下面的表格中，我们列出了带有谓语的一些路径表达式，以及表达式的结果：

| 路径表达式                              | 结果                                       |
| ---------------------------------- | ---------------------------------------- |
| /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。          |
| /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。         |
| /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。        |
| /bookstore/book[position()<3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
| //title[@lang]                     | 选取所有拥有名为 lang 的属性的 title 元素。             |
| //title[@lang='eng']               | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。   |
| /bookstore/book[price>35.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

## 选取未知节点

XPath 通配符可用来选取未知的 XML 元素。

| 通配符    | 描述         |
| ------ | ---------- |
| *      | 匹配任何元素节点。  |
| @*     | 匹配任何属性节点。  |
| node() | 匹配任何类型的节点。 |

在下面的表格中，我们列出了一些路径表达式，以及这些表达式的结果：

| 路径表达式        | 结果                     |
| ------------ | ---------------------- |
| /bookstore/* | 选取 bookstore 元素的所有子元素。 |
| //*          | 选取文档中的所有元素。            |
| //title[@*]  | 选取所有带有属性的 title 元素。    |

------

## 选取若干路径

通过在路径表达式中使用"|"运算符，您可以选取若干个路径。

在下面的表格中，我们列出了一些路径表达式，以及这些表达式的结果：

| 路径表达式                            | 结果                                       |
| -------------------------------- | ---------------------------------------- |
| //book/title \| //book/price     | 选取 book 元素的所有 title 和 price 元素。          |
| //title \| //price               | 选取文档中的所有 title 和 price 元素。               |
| /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |

```python
htmlFile = '''
    <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-inactive"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li> 
    </ul>
    '''

    
html = lxml.etree.parse("filename.html") # 读取文件
html = lxml.etree.HTML(htmltext) # 直接加载
	
print(html.xpath("//li/@class")) # 取出li的所有节点class名称
print(html.xpath("//li/@text")) # 为空，如果包含这个属性，
print(html.xpath("//li/a")) # li下面5个节点，每个节点对应一个元素
print(html.xpath("//li/a/@href")) # 取出li的所有节点 a内部href名称
print(html.xpath("//li/a/@href=\"link3.html\"")) # 判断是有一个节点==link3.html
print(html.xpath("//li//span")) # 取出li下面所有的span
print(html.xpath("//li//span/@class")) # 取出li下面所有的span内部的calss
print(html.xpath("//li/a//@class")) # 取出li的所有节点内部节点a包含的class
print(html.xpath("//li")) # 取出所有节点
print(html.xpath("//li[1]")) # 取出第一个
print(html.xpath("//li[last()]")) # 取出最后一个
print(html.xpath("//li[last()-1]")) # 取出倒数第2个
print(html.xpath("//li[last()-1]/a/@href")) # 取出倒数第2个的a下面的href
print(html.xpath("//*[@text=\"3\"]")) # 选着text=3的元素
print(html.xpath("//*[@text=\"3\"]/@class")) # 选着text=3的元素
print(html.xpath("//*[@class=\"nimei\"]")) # 选着text=3的元素
print(html.xpath("//li/a/text()")) # 取出<>
print(html.xpath("//li[3]/a/span/text()")) # 取出内部<>数据
```

- 抓取招聘网岗位数量

- 抓取51job全国岗位https://jobs.51job.com/

- 抓取上海市高级人民法院

- http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search.jsp?

  ```python
  #!C:\Python36\python.exe
  # -*- coding:utf-8 -*-
  import requests

  url = "http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search_content.jsp?"
  # print(requests.get(url).content.decode("gbk"))

  data = {
  "yzm": " eHep",
  "ft": "",
  "ktrqks": " 2018 - 04 - 26",
  "ktrqjs": " 2018 - 05 - 26",
  "spc": "",
  "yg": "",
  "bg": "",
  "ah": "",
  "pagesnum": "2"}

  header = {
  "Referer": "http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTAxMDEmbG1tYz23qNS6tq/MrAPdcssPdcssz&zd=xwzx",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

  page = requests.post(url=url, headers=header, data=data)

  print(page.content.decode("gbk"))

  ```




- http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTA2MDImbG1tYz2wuMD90dDO9gPdcssPdcssz&zd=spyj
- 爬取链家https://gz.lianjia.com/ershoufang/


```python
   ua_list = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
]
```
