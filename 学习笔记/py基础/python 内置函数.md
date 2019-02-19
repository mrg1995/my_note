##python 内置函数

###目前已经知道

>abs()   绝对值
>
>chr()    获得对应的asc码
>
>dict()  转化成字典
>
>float() 转换成浮点数
>
>format()    字符串 赋值
>
>getattr()    获取对象属性
>
>hasattr()   判断对象是否有对应属性
>
>id()   查看对象id
>
>input()  输入值
>
>int()   转换成整型
>
>len()  对象长度
>
>list()  转化成列表
>
>max()   最大值
>
>min()  最小值
>
>open()   打开文件
>
>ord()   获得对应asc码的索引
>
>print()  打印对象
>
>range()    生成可迭代对象
>
>set()    转为集合
>
>setattr()   给对象设置属性
>
>str()    转化为字符串
>
>sum()  求和
>
>tuple()   转为元组
>
>type()   查看类型
>
>bool()  将参数转为布尔类型
>
>delattr()  删除对象属性

###all()

all() 函数用于判断给定的可迭代参数 iterable 中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False。

元素除了是 0、空、FALSE 外都算 TRUE。

>```
>all(iterable)
>```

返回布尔值

###any()

any() 函数用于判断给定的可迭代参数 iterable 是否全部为 False，则返回 False，如果有一个为 True，则返回 True。

元素除了是 0、空、FALSE 外都算 TRUE。

>```
>any(iterable)
>```

返回布尔值

###ascii()

ascii() 函数类似 repr() 函数, 返回一个表示对象的字符串, 但是对于字符串中的非 ASCII 字符则返回通过 repr() 函数使用 \x, \u 或 \U 编码的字符。 生成字符串类似 Python2 版本中 repr() 函数的返回值。

>```
>ascii(object)
>```

返回字符串

###bin()

**bin()** 返回一个整数 int 或者长整数 long int 的二进制表示。

>bin(x)

返回字符串

### bytearray()

**bytearray()** 方法返回一个新字节数组。这个数组里的元素是可变的，并且每个元素的值范围: 0 <= x < 256。

>```
>bytearray([source[, encoding[, errors]]])
>```

### bytes()

bytes 函数返回一个新的 bytes 对象，该对象是一个 0 <= x < 256 区间内的整数不可变序列。它是 bytearray 的不可变版本

>```
>bytes([source[, encoding[, errors]]])
>```

###callable()

**callable()** 函数用于检查一个对象是否是可调用的。如果返回True，object仍然可能调用失败；但如果返回False，调用对象ojbect绝对不会成功。

对于函数, 方法, lambda 函式, 类, 以及实现了 __call__ 方法的类实例, 它都返回 True。

>```
>callable(object)
>```

返回布尔值

### classmethod()   修饰符

**classmethod** 修饰符对应的函数不需要实例化，不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等。

>class A(object):
>​    bar = 1
>​    def func1(self):  
>​        print ('foo') 
>​    @classmethod
>​    def func2(cls):
>​        print ('func2')
>​        print (cls.bar)
>​        cls().func1()   # 调用 foo 方法
>
>A.func2()               # 不需要实例化

输出结果:

>func2
>
>1
>
>foo

###compile()

compile() 函数将一个字符串编译为字节代码。

>```
>compile(source, filename, mode[, flags[, dont_inherit]])
>```

参数

- source -- 字符串或者AST（Abstract Syntax Trees）对象。。
- filename -- 代码文件名称，如果不是从文件读取代码则传递一些可辨认的值。
- mode -- 指定编译代码的种类。可以指定为 exec, eval, single。
- flags -- 变量作用域，局部命名空间，如果被提供，可以是任何映射对象。。
- flags和dont_inherit是用来控制编译源码时的标志

返回值

返回表达式执行结果。

###complex()

**complex()** 函数用于创建一个值为 real + imag * j 的复数或者转化一个字符串或数为复数。如果第一个参数为字符串，则不需要指定第二个参数。。

>```
>complex([real[, imag]])
>```

返回一个复数

###dir()

**dir()** 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。

>```
>dir([object])
>```

返回模块的属性列表

### divmod()

python divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)

>```
>divmod(a, b)
>```

### enumerate()

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

>```
>enumerate(sequence, [start=0])
>```

实例:

>```
>>>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>>>list(enumerate(seasons))
>[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
>______________________________
>seq = ['one', 'two', 'three']
>for i, element in enumerate(seq):
>...    print(i, seq[i])
>... 
>输出
>0 one
>1 two
>2 three
>
>```

###eval()

eval() 函数用来执行一个字符串表达式，并返回表达式的值

>```
>eval(expression[, globals[, locals]])
>```

参数

- expression -- 表达式。
- globals -- 变量作用域，全局命名空间，如果被提供，则必须是一个字典对象。
- locals -- 变量作用域，局部命名空间，如果被提供，可以是任何映射对象。

返回表达式计算结果

###exec()

exec 执行储存在字符串或文件中的 Python 语句，相比于 eval，exec可以执行更复杂的 Python 代码。

>```
>exec(object[, globals[, locals]])
>```

参数

- object：必选参数，表示需要被指定的Python代码。它必须是字符串或code对象。如果object是一个字符串，该字符串会先被解析为一组Python语句，然后在执行（除非发生语法错误）。如果object是一个code对象，那么它只是被简单的执行。
- globals：可选参数，表示全局命名空间（存放全局变量），如果被提供，则必须是一个字典对象。
- locals：可选参数，表示当前局部命名空间（存放局部变量），如果被提供，可以是任何映射对象。如果该参数被忽略，那么它将会取与globals相同的值。

返回值为None

###filter()

**filter()** 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。

该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。

>```
>filter(function, iterable)
>```

返回列表

###frozenset()

**frozenset()** 返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。

>```
>frozenset([iterable])
>```

返回一个frozenset对象   如果不提供参数,默认生成空集合

###globals()

**globals()** 函数会以字典类型返回当前位置的全部全局变量。

>```
>globals()
>```

返回全局变量的字典

###hash()

**hash()** 用于获取取一个对象（字符串或者数值等）的哈希值。

>hash(object)

返回对象的hash值

###help()

**help()** 函数用于查看函数或模块用途的详细说明。

>help(object)

返回对象的帮助信息

###hex()

**hex()** 函数用于将10进制整数转换成16进制，以字符串形式表示。

>hex(x)

返回字符串

###isinstance()

isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。

>```
>isinstance(object, classinfo)
>```

参数

- object -- 实例对象。
- classinfo -- 可以是直接或间接类名、基本类型或者由它们组成的元组。

返回布尔值

### issubclass()

**issubclass()** 方法用于判断参数 class 是否是类型参数 classinfo 的子类。

>```
>issubclass(class, classinfo)
>```

返回布尔值

###iter()

**iter()** 函数用来生成迭代器。

>```
>iter(object[, sentinel])
>```

参数

- object -- 支持迭代的集合对象。
- sentinel -- 如果传递了第二个参数，则参数 object 必须是一个可调用的对象（如，函数），此时，iter 创建了一个迭代器对象，每次调用这个迭代器对象的__next__()方法时，都会调用 object。

返回迭代器对象

###locals()

**locals()** 函数会以字典类型返回当前位置的全部局部变量。

对于函数, 方法, lambda 函式, 类, 以及实现了 __call__ 方法的类实例, 它都返回 True。

>locals()

返回  

以字典形式返回所有局部变量

###map()

**map()** 会根据提供的函数对指定序列做映射。

第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。

>```
>map(function, iterable, ...)
>```

参数

- function -- 函数，有两个参数
- iterable -- 一个或多个序列



返回 迭代器

实例:

```python
>>>def square(x) :            # 计算平方数
...     return x ** 2
... 
>>> map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
[1, 4, 9, 16, 25]
>>> map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
[1, 4, 9, 16, 25]
 
# 提供了两个列表，对相同位置的列表数据进行相加
>>> map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
[3, 7, 11, 15, 19]
```

###memoryview()

**memoryview()** 函数返回给定参数的内存查看对象(Momory view)。

所谓内存查看对象，是指对支持缓冲区协议的数据进行包装，在不需要复制对象基础上允许Python代码访问。

>```
>memoryview(obj)
>```

返回元组列表

###oct()

**oct()** 函数将一个整数转换成8进制字符串。

>```
>oct(x)
>```

返回字符串

###pow()

**pow()** 方法返回 （x的y次方） 的值。

>```
>#math 模块的pow方法
>import math
>math.pow( x, y )
>```

>```
># 内置的pow()
>pow(x, y[, z])
>```

函数是计算x的y次方，如果z在存在，则再对结果进行取模，其结果等效于pow(x,y) %z

**注意：**pow() 通过内置的方法直接调用，内置方法会把参数作为整型，而 math 模块则会把参数转换为 float。

返回 xy（x的y次方） 的值。

###property()

**property()** 函数的作用是在新式类中返回属性值。也可以作为装饰器

>```
>property([fget[, fset[, fdel[, doc]]]])
>```

参数

- fget -- 获取属性值的函数
- fset -- 设置属性值的函数
- fdel -- 删除属性值函数
- doc -- 属性描述信息

返回新式类属性

###reversed()

reversed 函数返回一个反转的迭代器。

>```
>reversed(seq)
>```

参数

- seq -- 要转换的序列，可以是 tuple, string, list 或 range。

返回一个反转的迭代器

###round()

**round()** 方法返回浮点数x的四舍五入值。

>```
>round( x [, n]  )
>```

参数

- x -- 数字表达式。
- n -- 表示从小数点位数，其中 x 需要四舍五入，默认值为 0。

返回浮点数的四舍五入值

###slice()

**slice()** 函数实现切片对象，主要用在切片操作函数里的参数传递。

>```
> slice(stop)
> slice(start, stop[, step])
>```

参数

- start -- 起始位置
- stop -- 结束位置
- step -- 间距



实例:

```python
>>>myslice = slice(5)    # 设置截取5个元素的切片
>>> myslice
slice(None, 5, None)
>>> arr = range(10)
>>> arr
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> arr[myslice]         # 截取 5 个元素
[0, 1, 2, 3, 4]
>>>
```

### sorted()

**sorted()** 函数对所有可迭代的对象进行排序操作。

>**sort 与 sorted 区别：**
>
>sort 是应用在 list 上的方法，sorted 可以对所有可迭代的对象进行排序操作。
>
>list 的 sort 方法返回的是对已经存在的列表进行操作，而内建函数 sorted 方法返回的是一个新的 list，而不是在原来的基础上进行的操作。

>```
>sorted(iterable, key=None, reverse=False)  
>```

参数

- iterable -- 可迭代对象。
- key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
- reverse -- 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。

返回重新排序的列表

实例:

```python
>>>example_list = [5, 0, 6, 1, 2, 7, 3, 4]
>>> result_list = sorted(example_list, key=lambda x: x*-1)
>>> print(result_list)
[7, 6, 5, 4, 3, 2, 1, 0]
```

###staticmethod()

python staticmethod 返回函数的静态方法。 装饰器

该方法不强制要求传递参数，如下声明一个静态方法：

```python
class C(object):
    @staticmethod
    def f(arg1, arg2, ...):
        ...
```

以上实例声明了静态方法 f，类可以不用实例化就可以调用该方法 C.f()，当然也可以实例化后调用 C().f()。

>```
>staticmethod(function)
>```

###super()

**super()** 函数是用于调用父类(超类)的一个方法。

super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。

MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。

>```
>super(type[, object-or-type])
>```

参数

- type -- 类。
- object-or-type -- 类，一般是 self

实例:

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
class FooParent(object):
    def __init__(self):
        self.parent = 'I\'m the parent.'
        print ('Parent')
    
    def bar(self,message):
        print ("%s from Parent" % message)
 
class FooChild(FooParent):
    def __init__(self):
        # super(FooChild,self) 首先找到 FooChild 的父类（就是类 FooParent），然后把类B的对象 FooChild 转换为类 FooParent 的对象
        super(FooChild,self).__init__()    
        print ('Child')
        
    def bar(self,message):
        super(FooChild, self).bar(message)
        print ('Child bar fuction')
        print (self.parent)
 
if __name__ == '__main__':
    fooChild = FooChild()
    fooChild.bar('HelloWorld')
```

执行结果

```python
Parent
Child
HelloWorld from Parent
Child bar fuction
I'm the parent.
```

###var()

**vars()** 函数返回对象object的属性和属性值的字典对象。

>```
>vars([object])
>```

返回

返回对象object的属性和属性值的字典对象，如果没有参数，就打印当前调用位置的属性和属性值 类似 locals()。

###zip()

**zip()** 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。

我们可以使用 list() 转换来输出列表。

如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。

>```
>zip([iterable, ...])
>```



实例:

```
>>>a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 返回一个对象
>>> zipped
<zip object at 0x103abc288>
>>> list(zipped)  # list() 转换为列表
[(1, 4), (2, 5), (3, 6)]
>>> list(zip(a,c))              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
 
>>> a1, a2 = zip(*zip(a,b))          # 与 zip 相反，*zip 可理解为解压，返回二维矩阵式
>>> list(a1)
[1, 2, 3]
>>> list(a2)
[4, 5, 6]
>>>
```