# selenium&phantomJS&headless

- IE11的Webdriver下载：

http://dl.pconline.com.cn/download/771640-1.html

链接：https://pan.baidu.com/s/13TTyXGNaG5cpSNdl1k9ksQ 密码：2n9n

- Chrome65.0.3325.146的webdriver驱动下载：

链接：https://pan.baidu.com/s/1gv-ATOv_XdaUEThQd5-QtA 密码：dzh2

多版本：http://chromedriver.storage.googleapis.com/index.html

- Firefox58的webdriver驱动下载

链接：https://pan.baidu.com/s/1RATs8y-9Vige0IxcKdn83w 密码：l41g

- ### get(url)

Open an url

```python
#打开URL
def openURL():
  driver = webdriver.Chrome()
  driver.get("http://www.baidu.com")
  print(driver.page_source)
```



- ### clear()

Clears the text if it’s a text entry element.

- ### page_source获取HTML源码

- ### close() 关闭

- ### click()

Clicks the element.

- ### execute_script(script, *args)

Synchronously Executes JavaScript in the current window/frame.

Args: script: The JavaScript to execute. *args: Any applicable arguments for your JavaScript.

Usage: 

```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# 下拉滚动条，使浏览器加载出动态加载的内容
while True:
    # 可能像这样要拉很多次，中间要适当的延时。
    # 如果说说内容都很长，就增大下拉的长度。
    for i in range(10):
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    break
```



- ### find_element(by='id', value=None)

‘Private’ method used by the find_element_by_* methods.

Usage: Use the corresponding find_element_by_* instead of this.

Return type: WebElement

- ### find_element_by_class_name(name)

Finds element within this element’s children by class name.

Args: name: The class name of the element to find.

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_class_name(‘foo’)

- ### find_element_by_css_selector(css_selector)

Finds element within this element’s children by CSS selector.

Args: css_selector - CSS selector string, ex: ‘a.nav#home’

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_css_selector(‘#foo’)

- ### find_element_by_id(id_)

Finds element within this element’s children by ID.

Args: id_ - ID of child element to locate.

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: foo_element = element.find_element_by_id(‘foo’)

- ### find_element_by_link_text(link_text)

Finds element within this element’s children by visible link text.

Args: link_text - Link text string to search for.

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_link_text(‘Sign In’)

- ### find_element_by_name(name)

Finds element within this element’s children by name.

Args: name - name property of the element to find.

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_name(‘foo’)

- ### find_element_by_tag_name(name)

Finds element within this element’s children by tag name.

Args: name - name of html tag (eg: h1, a, span)

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_tag_name(‘h1’)

- ### find_element_by_xpath(xpath)

Finds element by xpath.

Args: xpath - xpath of element to locate. “//input[@class=’myelement’]”

Note: The base path will be relative to this element’s location.

This will select the first link under this element.

```
myelement.find_element_by_xpath(".//a")
```

However, this will select the first link on the page.

```
myelement.find_element_by_xpath("//a")
```

Returns: WebElement - the element if it was found

Raises: NoSuchElementException - if the element wasn’t found

Usage: element = element.find_element_by_xpath(‘//div/td[1]’)

- ### find_elements(by='id', value=None)

‘Private’ method used by the find_elements_by_* methods.

Usage: Use the corresponding find_elements_by_* instead of this.

Return type: list of WebElement

- ### find_elements_by_class_name(name)

Finds a list of elements within this element’s children by class name.

Args:

name: The class name of the elements to find.

Returns: list of WebElement - a list with elements if any was found. An empty list if not

Usage: elements = element.find_elements_by_class_name(‘foo’)

- ### find_elements_by_css_selector(css_selector)

Finds a list of elements within this element’s children by CSS selector.

Args: css_selector - CSS selector string, ex: ‘a.nav#home’

Returns: list of WebElement - a list with elements if any was found. An empty list if not

Usage: elements = element.find_elements_by_css_selector(‘.foo’)

- ### find_elements_by_id(id_)

Finds a list of elements within this element’s children by ID. Will return a list of webelements if found, or an empty list if not.

Args: id_ - Id of child element to find.

Returns: list of WebElement - a list with elements if any was found. An empty list if not

Usage: elements = element.find_elements_by_id(‘foo’)

- ### find_elements_by_link_text(link_text)

Finds a list of elements within this element’s children by visible link text.

Args: link_text - Link text string to search for.

Returns: list of webelement - a list with elements if any was found. an empty list if not

Usage: elements = element.find_elements_by_link_text(‘Sign In’)

- ### find_elements_by_name(name)

Finds a list of elements within this element’s children by name.

Args: name - name property to search for.

Returns: list of webelement - a list with elements if any was found. an empty list if not

Usage: elements = element.find_elements_by_name(‘foo’)

- ### find_elements_by_tag_name(name)

Finds a list of elements within this element’s children by tag name.

Args: name - name of html tag (eg: h1, a, span)

Returns: list of WebElement - a list with elements if any was found. An empty list if not

Usage: elements = element.find_elements_by_tag_name(‘h1’)

- ### find_elements_by_xpath(xpath)

Finds elements within the element by xpath.

Args: xpath - xpath locator string.

Note: The base path will be relative to this element’s location.

This will select all links under this element.

myelement.find_elements_by_xpath(".//a")

However, this will select all links in the page itself.

myelement.find_elements_by_xpath("//a")

Returns: list of WebElement - a list with elements if any was found. An empty list if not

Usage: elements = element.find_elements_by_xpath(“//div[contains(@class, ‘foo’)]”)

- ### get_attribute(name)

Gets the given attribute or property of the element.

This method will first try to return the value of a property with the given name. If a property with that name doesn’t exist, it returns the value of the attribute with the same name. If there’s no attribute with that name, None is returned.

Values which are considered truthy, that is equals “true” or “false”, are returned as booleans. All other non-None values are returned as strings. For attributes or properties which do not exist, None is returned.

Args: name - Name of the attribute/property to retrieve.

Example:

```python
# Check if the "active" CSS class is applied to an element.
is_active = "active" in target_element.get_attribute("class")
```

- ### save_screenshot(filename)

Saves a screenshot of the current element to a PNG image file. Returns

False if there is any IOError, else returns True. Use full paths in your filename.

Args:

filename: The full path you wish to save your screenshot to. This should end with a .png extension.

Usage: element.screenshot(‘/Screenshots/foo.png’)

- ### send_keys(*value)

Simulates typing into the element.

Args: value - A string for typing, or setting form fields. For setting file inputs, this could be a local file path.

Use this to send simple key events or to fill out form fields:

```python
form_textfield = driver.find_element_by_name('username')
form_textfield.send_keys("admin")

search.send_keys("海贼王", Keys.ARROW_DOWN) # 回车
```

This can also be used to set file inputs.

```python
file_input = driver.find_element_by_name('profilePic')
file_input.send_keys("path/to/profilepic.gif")
# Generally it's better to wrap the file path in one of the methods
# in os.path to return the actual path to support cross OS testing.
# file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))
```

- selenium登陆知乎
- selenium设置代理

```python
#!C:\Python36\python.exe
# -*- coding:utf-8 -*-
'''
@Time    : 2018/6/1 16:44
@Author  : Fate
@File    : 10seleniue设置代理.py
'''
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://10.3.132.6:808")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(chrome_options=chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("https://blog.csdn.net/zwq912318834/article/details/78626739")
print(browser.page_source)

# 退出，清除浏览器缓存
# browser.quit()

```



- selenium登陆QQ空间

```python
from selenium import webdriver
import time

# http://demo.smeoa.com/
def openURL():
  driver = webdriver.Chrome()
  driver.get("https://user.qzone.qq.com")
  time.sleep(6)
  login = driver.find_element_by_id('login_frame')
  driver.switch_to_frame(login)
  time.sleep(3)
  driver.find_element_by_id('switcher_plogin').click()

  username = driver.find_element_by_id('u')
  password = driver.find_element_by_id('p')
  username.send_keys('*****')
  password.send_keys('*****')
  time.sleep(3)
  driver.find_element_by_id('login_button').click()
  print("OK")

if __name__ == '__main__':
	openURL()
```

- selenium抓取会小二http://www.huixiaoer.com/



# PhantomJS 无界面浏览器

以停止研发

#headless 

Headless Chrome是Chrome 浏览器的无界面形态，可以在不打开浏览器的前提下，使用所有 Chrome 支持的特性运行程序。相比于现代浏览器，Headless Chrome 更加方便测试web应用，获得网站的截图，做爬虫抓取信息等，也更加贴近浏览器环境。

Headless Chrome基于PhantomJS（QtWebKit内核）由谷歌Chrome团队开发。团队表示将专注研发这个项目

确保你的 chrome 浏览器版本是 60+

# 配置

```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
```

