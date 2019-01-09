# flask-restful  请求解析

## 基本参数

这里是请求解析一个简单的例子。它寻找在 `flask.Request.values` 字典里的两个参数。一个类型为 `int`，另一个的类型是 `str`

```
from flask.ext.restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name', type=str)
args = parser.parse_args()
```

如果你指定了 help 参数的值，在解析的时候当类型错误被触发的时候，它将会被作为错误信息给呈现出来。如果你没有指定 help 信息的话，默认行为是返回类型错误本身的信息。

默认下，arguments **不是** 必须的。另外，在请求中提供的参数不属于 RequestParser 的一部分的话将会被忽略。

另请注意：在请求解析中声明的参数如果没有在请求本身设置的话将默认为 `None`。

## 必需的参数

#### *required=True*****

```
parser.add_argument('name', type=str, required=True,
help="Name cannot be blank!")
```

## 多个值&列表

####  action='append'

```
parser.add_argument('name', type=str, action='append')

```

这将让你做出这样的查询

```
curl http://api.example.com -d "Name=bob" -d "Name=sue" -d "Name=joe"
```

你的参数将会像这样

```
args = parser.parse_args()
args['name']    # ['bob', 'sue', 'joe']
```

## 其它目标（Destinations）

####  dest = kwarg。

```
parser.add_argument('name', type=str, dest='public_name')

args = parser.parse_args()
args['public_name']

```

## 参数位置

#### location

默认下，`RequestParser` 试着从 `flask.Request.values`，以及 `flask.Request.json` 解析值。

在 `add_argument()` 中使用 `location` 参数可以指定解析参数的位置。`flask.Request` 中任何变量都能被使用。例如：

```
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', type=str, location='headers')

# From http cookies
parser.add_argument('session_id', type=str, location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

```

## 多个位置

#### location

通过传入一个列表到 `location` 中可以指定 **多个** 参数位置:

```
parser.add_argument('text', location=['headers', 'values'])
```

列表中最后一个优先出现在结果集中。（例如：location=[‘headers’, ‘values’]，解析后 ‘values’ 的结果会在 ‘headers’ 前面）

## 继承解析

#### copy(),replace_argument(),remove_argument()

往往你会为你编写的每个资源编写不同的解析器。这样做的问题就是如果解析器具有共同的参数。不是重写，你可以编写一个包含所有共享参数的父解析器接着使用 `copy()` 扩充它。你也可以使用 `replace_argument()` 覆盖父级的任何参数，或者使用 `remove_argument()` 完全删除参数。 例如：

```
from flask.ext.restful import RequestParser

parser = RequestParser()
parser.add_argument('foo', type=int)

parser_copy = parser.copy()
parser_copy.add_argument('bar', type=int)

# parser_copy has both 'foo' and 'bar'

parser_copy.replace_argument('foo', type=str, required=True, location='json')
# 'foo' is now a required str located in json, not an int as defined
#  by original parser

parser_copy.remove_argument('foo')
# parser_copy no longer has 'foo' argument
```
## 自定义输入

对于解析参数，你可能要执行自定义验证。创建你自己的输入类型让你轻松地扩展请求解析。

```
def odd_number(value):
    if value % 2 == 0:
        raise ValueError("Value is not odd")

    return value

```

请求解析器在你想要在错误消息中引用名称的情况下将也会允许你访问参数的名称。

```
def odd_number(value, name):
    if value % 2 == 0:
        raise ValueError("The parameter '{}' is not odd. You gave us the value: {}".format(name, value))

    return value

```

你还可以将公开的参数转换为内部表示：

```
# maps the strings to their internal integer representation
# 'init' => 0
# 'in-progress' => 1
# 'completed' => 2

def task_status(value):
    statuses = [u"init", u"in-progress", u"completed"]
    return statuses.index(value)

```

然后你可以在你的 RequestParser 中使用这些自定义输入类型：

```
parser = reqparse.RequestParser()
parser.add_argument('OddNumber', type=odd_number)
parser.add_argument('Status', type=task_status)
args = parser.parse_args()
```













