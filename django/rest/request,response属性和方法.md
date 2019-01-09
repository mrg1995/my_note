##1 Request 对象的属性和方法

每个 view 函数的第一个参数是一个 HttpRequest 对象，就像下面这个 hello() 函数:

```
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world")
```

HttpRequest对象包含当前请求URL的一些信息：

| **属性**        | **描述**                                   |
| ------------- | ---------------------------------------- |
| path          | 请求页面的全路径,不包括域名—例如, "/hello/"。            |
| method        | 请求中使用的HTTP方法的字符串表示。全大写表示。例如:if request.method == 'GET':     do_something() elif request.method == 'POST':     do_something_else() |
| GET           | 包含所有HTTP GET参数的类字典对象。参见QueryDict 文档。     |
| POST          | 包含所有HTTP POST参数的类字典对象。参见QueryDict 文档。服务器收到空的POST请求的情况也是有可能发生的。也就是说，表单form通过HTTP POST方法提交请求，但是表单中可以没有数据。因此，不能使用语句if request.POST来判断是否使用HTTP POST方法；应该使用if request.method == "POST" (参见本表的method属性)。注意: POST不包括file-upload信息。参见FILES属性。 |
| REQUEST       | 为了方便，该属性是POST和GET属性的集合体，但是有特殊性，先查找POST属性，然后再查找GET属性。借鉴PHP's $_REQUEST。例如，如果GET = {"name": "john"} 和POST = {"age": '34'},则 REQUEST["name"] 的值是"john", REQUEST["age"]的值是"34".强烈建议使用GET and POST,因为这两个属性更加显式化，写出的代码也更易理解。 |
| COOKIES       | 包含所有cookies的标准Python字典对象。Keys和values都是字符串。 |
| FILES         | 包含所有上传文件的类字典对象。FILES中的每个Key都是<input type="file" name="" />标签中name属性的值. FILES中的每个value 同时也是一个标准Python字典对象，包含下面三个Keys:filename: 上传文件名,用Python字符串表示content-type: 上传文件的Content typecontent: 上传文件的原始内容注意：只有在请求方法是POST，并且请求页面中<form>有enctype="multipart/form-data"属性时FILES才拥有数据。否则，FILES 是一个空字典。 |
| META          | CONTENT_LENGTHCONTENT_TYPEQUERY_STRING: 未解析的原始查询字符串,(其余看下文) |
| user          | 是一个django.contrib.auth.models.User 对象，代表当前登录的用户。如果访问用户当前没有登录，user将被初始化为django.contrib.auth.models.AnonymousUser的实例。你可以通过user的is_authenticated()方法来辨别用户是否登录：`if request.user.is_authenticated():     # Do something for logged-in users. else:     # Do something for anonymous users.`只有激活Django中的AuthenticationMiddleware时该属性才可用 |
| session       | 唯一可读写的属性，代表当前会话的字典对象。只有激活Django中的session支持时该属性才可用。 |
| raw_post_data | 原始HTTP POST数据，未解析过。 高级处理时会有用处。           |

META属性:

包含所有可用HTTP头部信息的字典。 例如:

CONTENT_LENGTHCONTENT_TYPEQUERY_STRING: 未解析的原始查询字符串

REMOTE_ADDR: 客户端IP地址

REMOTE_HOST: 客户端主机名

SERVER_NAME: 服务器主机名

SERVER_PORT: 服务器端口

META 中这些头加上前缀HTTP_为Key, 如:

HTTP_ACCEPT_ENCODINGHTTP_ACCEPT_LANGUAGEHTTP_HOST: 客户发送的HTTP主机头信息HTTP_REFERER: referring页

HTTP_USER_AGENT: 客户端的user-agent字符串

HTTP_X_BENDER: X-Bender头信息

| 方法               | 描述                                       |
| ---------------- | ---------------------------------------- |
| __getitem__(key) | 返回GET/POST的键值,先取POST,后取GET。如果键不存在抛出 KeyError。  这是我们可以使用字典语法访问HttpRequest对象。  例如,request["foo"]等同于先request.POST["foo"] 然后 request.GET["foo"]的操作。 |
| has_key()        | 检查request.GET or request.POST中是否包含参数指定的Key。 |
| get_full_path()  | 返回包含查询字符串的请求路径。例如， "/music/bands/the_beatles/?print=true" |
| is_secure()      | 如果请求是安全的，返回True，就是说，发出的是HTTPS请求。         |

##2 QueryDict对象

在HttpRequest对象中, GET和POST属性是django.http.QueryDict类的实例。

QueryDict类似字典的自定义类，用来处理单键对应多值的情况。

QueryDict实现所有标准的词典方法。还包括一些特有的方法：

| **方法**      | **描述**                                   |
| ----------- | ---------------------------------------- |
| __getitem__ | 和标准字典的处理有一点不同，就是，如果Key对应多个Value，__getitem__()返回最后一个value。 |
| __setitem__ | 设置参数指定key的value列表(一个Python list)。注意：它只能在一个mutable QueryDict 对象上被调用(就是通过copy()产生的一个QueryDict对象的拷贝). |
| get()       | 如果key对应多个value，get()返回最后一个value。         |
| update()    | 参数可以是QueryDict，也可以是标准字典。和标准字典的update方法不同，该方法添加字典 items，而不是替换它们:`>>> q = QueryDict('a=1')  >>> q = q.copy() # to make it mutable  >>> q.update({'a': '2'})  >>> q.getlist('a')   ['1', '2']  >>> q['a'] # returns the last  ['2']` |
| items()     | 和标准字典的items()方法有一点不同,该方法使用单值逻辑的__getitem__():`>>> q = QueryDict('a=1&a=2&a=3')  >>> q.items()  [('a', '3')]` |
| values()    | 和标准字典的values()方法有一点不同,该方法使用单值逻辑的__getitem__(): |

此外, QueryDict也有一些方法，如下表：

| **方法**                   | **描述**                                   |
| ------------------------ | ---------------------------------------- |
| copy()                   | 返回对象的拷贝，内部实现是用Python标准库的copy.deepcopy()。该拷贝是mutable(可更改的) — 就是说，可以更改该拷贝的值。 |
| getlist(key)             | 返回和参数key对应的所有值，作为一个Python list返回。如果key不存在，则返回空list。 It's guaranteed to return a list of some sort.. |
| setlist(key,list_)       | 设置key的值为list_ (unlike __setitem__()).    |
| appendlist(key,item)     | 添加item到和key关联的内部list.                    |
| setlistdefault(key,list) | 和setdefault有一点不同，它接受list而不是单个value作为参数。  |
| lists()                  | 和items()有一点不同, 它会返回key的所有值，作为一个list, 例如:`>>> q = QueryDict('a=1&a=2&a=3')  >>> q.lists()  [('a', ['1', '2', '3'])]  ` |
| urlencode()              | 返回一个以查询字符串格式进行格式化后的字符串(e.g., "a=2&b=3&b=5"). |

## 3 HttpResponse

类定义：class HttpResponse[source]

HttpResponse类定义在django.http模块中。

HttpRequest对象由Django自动创建，而HttpResponse对象则由程序员手动创建.

我们编写的每个视图都要实例化、填充和返回一个HttpResponse对象。也就是函数的return值。

## 一、使用方法

### 1. 传递一个字符串

最简单的方式是传递一个字符串作为页面的内容到HttpResponse构造函数，并返回给用户:

```
>>> from django.http import HttpResponse
>>> response = HttpResponse("Here's the text of the Web page.")
>>> response = HttpResponse("Text only, please.", content_type="text/plain")
```

可以将response看做一个类文件对象，使用wirte()方法不断地往里面增加内容。

```
>>> response = HttpResponse()
>>> response.write("<p>Here's the text of the Web page.</p>")
>>> response.write("<p>Here's another paragraph.</p>")
```

### 2. 传递可迭代对象

HttpResponse会立即处理这个迭代器，并把它的内容存成字符串，最后废弃这个迭代器。比如文件在读取后，会立刻调用close()方法，关闭文件。

### 3. 设置头部字段

可以把HttpResponse对象当作一个字典一样，在其中增加和删除头部字段。

```
>>> response = HttpResponse()
>>> response['Age'] = 120
>>> del response['Age']
```

注意！与字典不同的是，如果要删除的头部字段如果不存在，del不会抛出KeyError异常。

HTTP的头部字段中不能包含换行。所以如果我们提供的头部字段值包含换行符（CR或者LF），将会抛出BadHeaderError异常。

### 4. 告诉浏览器将响应视为文件附件

让浏览器以文件附件的形式处理响应, 需要声明`content_type`类型和设置`Content-Disposition`头信息。 例如，给浏览器返回一个微软电子表格：

```
>>> response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
>>> response['Content-Disposition'] = 'attachment; filename="foo.xls"'
```

## 二、属性

### 1. HttpResponse.content

响应的内容。bytes类型。

### 2. HttpResponse.charset

编码的字符集。 如果没指定，将会从`content_type`中解析出来。

### 3. HttpResponse.status_code

响应的状态码，比如200。

### 4. HttpResponse.reason_phrase

响应的HTTP原因短语。 使用标准原因短语。

除非明确设置，否则`reason_phrase`由`status_code`的值决定。

### 5. HttpResponse.streaming

这个属性的值总是False。由于这个属性的存在，使得中间件能够区别对待流式响应和常规响应。

### 6. HttpResponse.closed

如果响应已关闭，那么这个属性的值为True。

## 三、 方法

### 1. HttpResponse.**init**(content='', content_type=None, status=200, reason=None, charset=None)[source]

响应的实例化方法。使用content参数和`content-type`实例化一个HttpResponse对象。

content应该是一个迭代器或者字符串。如果是迭代器，这个迭代期返回的应是一串字符串，并且这些字符串连接起来形成response的内容。 如果不是迭代器或者字符串，那么在其被接收的时候将转换成字符串。

`content_type`是可选地，用于填充HTTP的`Content-Type`头部。如果未指定，默认情况下由`DEFAULT_CONTENT_TYPE`和`DEFAULT_CHARSET`设置组成：`text/html; charset=utf-8`。

status是响应的状态码。reason是HTTP响应短语。charset是编码方式。

### 2. HttpResponse.has_header(header)

检查头部中是否有给定的名称（不区分大小写），返回True或 False。

### 3. HttpResponse.setdefault(header, value)

设置一个头部，除非该头部已经设置过了。

### 4. HttpResponse.set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)

设置一个Cookie。 参数与Python标准库中的Morsel.Cookie对象相同。

max_age: 生存周期，以秒为单位。

expires：到期时间。

domain: 用于设置跨域的Cookie。例如`domain=".lawrence.com"`将设置一个`www.lawrence.com`、`blogs.lawrence.com`和`calendars.lawrence.com`都可读的Cookie。 否则，Cookie将只能被设置它的域读取。

如果你想阻止客服端的JavaScript访问Cookie，可以设置httponly=True。

### 5. HttpResponse.set_signed_cookie(key, value, salt='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=True)

与`set_cookie()`类似，但是在设置之前将对cookie进行加密签名。通常与`HttpRequest.get_signed_cookie()`一起使用。

### 6. HttpResponse.delete_cookie(key, path='/', domain=None)

删除Cookie中指定的key。

由于Cookie的工作方式，path和domain应该与`set_cookie()`中使用的值相同，否则Cookie不会删掉。

### 7. HttpResponse.write(content)[source]

将HttpResponse实例看作类似文件的对象，往里面添加内容。

### 8. HttpResponse.flush()

清空HttpResponse实例的内容。

### 9. HttpResponse.tell()[source]

将HttpResponse实例看作类似文件的对象，移动位置指针。

### 10. HttpResponse.getvalue()[source]

返回HttpResponse.content的值。 此方法将HttpResponse实例看作是一个类似流的对象。

### 11. HttpResponse.readable()

Django1.10中的新功能，值始终为False。

### 12. HttpResponse.seekable()

Django1.10中的新功能，值始终为False。

### 13. HttpResponse.writable()[source]

Django1.10中的新功能，值始终为True。

### 14. HttpResponse.writelines(lines)[source]

将一个包含行的列表写入响应对象中。 不添加分行符。

## 四、HttpResponse的子类

Django包含了一系列的HttpResponse衍生类（子类），用来处理不同类型的HTTP响应。与HttpResponse相同, 这些衍生类存在于django.http之中。

- class HttpResponseRedirect[source]：重定向，返回302状态码。已经被redirect()替代。
- class HttpResponsePermanentRedirect[source]:永久重定向，返回301状态码。
- class HttpResponseNotModified[source]：未修改页面，返回304状态码。
- class HttpResponseBadRequest[source]：错误的请求，返回400状态码。
- class HttpResponseNotFound[source]：页面不存在，返回404状态码。
- class HttpResponseForbidden[source]：禁止访问，返回403状态码。
- class HttpResponseNotAllowed[source]：禁止访问，返回405状态码。
- class HttpResponseGone[source]：过期，返回405状态码。
- class HttpResponseServerError[source]：服务器错误，返回500状态码。

## 五、JsonResponse类

class JsonResponse（data，encoder = DjangoJSONEncoder，safe = True，json_dumps_params = None ，** kwargs）[source]

JsonResponse是HttpResponse的一个子类，是Django提供的用于创建JSON编码类型响应的快捷类。

它从父类继承大部分行为，并具有以下不同点：

它的默认Content-Type头部设置为application/json。

它的第一个参数data，通常应该为一个字典数据类型。 如果safe参数设置为False，则可以是任何可JSON 序列化的对象。

encoder默认为`django.core.serializers.json.DjangoJSONEncoder`，用于序列化数据。

布尔类型参数safe默认为True。 如果设置为False，可以传递任何对象进行序列化（否则，只允许dict 实例）。

典型的用法如下：

```
>>> from django.http import JsonResponse
>>> response = JsonResponse({'foo': 'bar'})
>>> response.content
b'{"foo": "bar"}'
```

若要序列化非dict对象，必须设置safe参数为False：

```
>>> response = JsonResponse([1, 2, 3], safe=False)
```

如果不传递safe=False，将抛出一个TypeError。

如果你需要使用不同的JSON 编码器类，可以传递encoder参数给构造函数：

```
>>> response = JsonResponse(data, encoder=MyJSONEncoder)
```

## 六、StreamingHttpResponse类

StreamingHttpResponse类被用来从Django响应一个流式对象到浏览器。如果生成的响应太长或者是占用的内存较大，这么做可能更有效率。 例如，它对于生成大型的CSV文件非常有用。

StreamingHttpResponse不是HttpResponse的衍生类（子类），因为它实现了完全不同的应用程序接口。但是，除了几个明显不同的地方，两者几乎完全相同。

## 七、FileResponse

文件类型响应。通常用于给浏览器返回一个文件附件。

FileResponse是StreamingHttpResponse的衍生类，为二进制文件专门做了优化。

FileResponse需要通过二进制模式打开文件，如下:

```
>>> from django.http import FileResponse
>>> response = FileResponse(open('myfile.png', 'rb'))
```