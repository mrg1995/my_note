# JQuery

## 1.什么是JQuery

jQuery是一个快速、简洁的JavaScript框架，是继Prototype之后又一个优秀的JavaScript代码库（或JavaScript框架）。jQuery设计的宗旨是“write Less，Do More”，即倡导写更少的代码，做更多的事情。它封装JavaScript常用的功能代码，提供一种简便的JavaScript设计模式，优化HTML文档操作、事件处理、动画设计和Ajax交互。可以到http://www.bootcdn.cn/jquery/下载最新的jQuery。

```
jQuery的核心特性可以总结为：具有独特的链式语法和短小清晰的多功能接口；具有高效灵活的css选择器，并且可对CSS选择器进行扩展；拥有便捷的插件扩展机制和丰富的插件。
```

## 2.引入方式

- 使用远程(cdn)

```js
<script src="//cdn.bootcss.com/jquery/3.1.1/jquery.js"></script>
```

- 使用本地

```js
<script type="text/javascript" src="jquery-3.1.1/jquery.js"></script>
```

- 说明:

  - 远程引入方式,//表示自适应协议

  - min版是代码压缩后的,不带空格换行,是工作版;不压缩的是开发,是研究版

  - 使用JQuery需要注明版本

  - 使用方法

    ```
    jQuery(document) .ready(function(){
    	alert(123);
    });

    //$ = jQuery
    $(document).ready(function(){
    	alert(456);
    });
    $(function(){
    	alert(456);
    });
    ```

    ​

  - $等于jquery,代表jQuery对象

  - jQuery(document)是构造jQuery对象的方法

  - 大部分方法都返回jQuery对象,所以可以串联操作

  - ready方法在DOM加载后执行,不加载资源,可以绑定多个方法

## 核心

#### jQuery对象访问

size()	返回当前匹配的元素个数

```js
<img src="test1.jpg"/> <img src="test2.jpg"/>
  $("img").size();
 //结果:
  2
```

length   返回jQuery对象的长度

selector   返回传给jQuery()的原始选择器

```js
$("ul")
  .append("<li>" + $("ul").selector + "</li>")
  .append("<li>" + $("ul li").selector + "</li>")
  .append("<li>" + $("div#foo ul:not([class])").selector + "</li>");
//结果:
ul
ul li
div#foo ul:not([class])
```

context  返回传给jQuery()的原始的DOM节点内容

index()  搜索匹配的元素,并返回相应元素的索引值,从0开始计数

```js
<ul>
  <li id="foo">foo</li>
  <li id="bar">bar</li>
  <li id="baz">baz</li>
</ul>
$('li').index(document.getElementById('bar')); //1，传递一个DOM对象，返回这个对象在原先集合中的索引位置
$('li').index($('#bar')); //1，传递一个jQuery对象
$('li').index($('li:gt(0)')); //1，传递一组jQuery对象，返回这个对象中第一个元素在原先集合中的索引位置
$('#bar').index('li'); //1，传递一个选择器，返回#bar在所有li中的做引位置
$('#bar').index(); //1，不传递参数，返回这个元素在同辈中的索引位置。  
```

#### 数据缓存    队列控制   插件机制   多库共存等  可在chm文档核心模块查看

## 选择器

- 标签选择器

  ```js
  $('div')		//选择所有div元素   
  ```

- id 选择器

  ```js
  $('#p1')		//选择id为p1 的元素
  ```

- 类选择器

  ```js
  $('.p2')		//选择class为p2的元素
  ```

- 组合选择器

  ```js
  $('div,p')		//选择所有 div 和 p 元素
  ```

- 层级选择器

  - ' '     例如: $('ul li')    即选中ul标签下所有的li标签


  - '>' 	选中父级元素下的子一级节点      子二级  及  更深层的子级元素不包括其中
  -  '+'选中相邻的下一个指定类型的元素
  - '~' 选择后面所有同级的元素

- 基本选择器

  具体内容查找jQuery api文档选择器一栏

- 内容选择器

  - has   包含指定标签

    ```js
    <div><p>Hello</p></div>
    <div>Hello again!</div>
    $("div:has(p)").addClass("test");
    //结果:
    [ <div class="test"><p>Hello</p></div> ]
    ```

  - contains 包含给定文本

    ```js
    <div>John Resig</div>
    <div>George Martin</div>
    <div>Malcom John Sinclair</div>
    <div>J. Ohn
    $("div:contains('John')")
    //结果:
    [ <div>John Resig</div>, <div>Malcom John Sinclair</div> ]
    ```

  - parent  匹配包含子元素或者文本的元素

    ```js
    <table>
      <tr><td>Value 1</td><td></td></tr>
      <tr><td>Value 2</td><td></td></tr>
    </table>
    $("td:parent")
    //结果:
    [ <td>Value 1</td>, <td>Value 2</td> ]
    ```

- 属性选择器

  ```
  attr主要针对标签的自定义属性
  prop主要针对标签的固有属性
  ```

  attr(name|properties|key,value|key,function(index,attr))  

   获取匹配的元素集合中的第一个属性的值  或者 设置每一个匹配元素的一个或多个属性

  | 参数                       | 含义                              |
  | ------------------------ | ------------------------------- |
  | name                     | 匹配元素中的属性名称                      |
  | properties               | 作为属性的“名/值对”对象                   |
  | key,value                | 属性名称 , 属性值                      |
  | key,function(index,attr) | 属性名, 函数 参数1是当前元素的索引值,参数2是原先的属性值 |

  attr(name)

  ```js
  $("img").attr("src");//返回文档中所有图像的src属性值
  ```

  attr(properties)

  ```js
  $("img").attr({ src: "test.jpg", alt: "Test Image" });
  //为所有的img设置src属性  以及alt属性
  ```

  attr(key,value)

  ```js
  $("img").attr("src","test.jpg");//为所有的img设置src属性
  ```

  attr(key,function(index,attr))

  ```js
  $("img").attr("title", function() { return this.src });
  //把src属性的值设置为title属性的值
  ```

  ​

- 可见性选择器

  - hidden    匹配选择  display为none 或者   type为hidden的元素
  - visible 元素的visibility:hidden  或者 opacity:0 被认为是可见的

- 子元素选择器

  - :first-child	为每个父元素匹配一个子元素   

    ```js
    <ul>
      <p>good</p>
      <li>John</li>
      <li>Karl</li>
      <li>Brandon</li>
    </ul>
    <ul>
      <li>Glen</li>
      <li>Tane</li>
      <li>Ralph</li>
    </ul>
    $("ul li:first-child")
    //结果   
    [ <li>Glen</li> ]   //为每个ul元素匹配 如果第一个是li则选择  不是则不选
    ```

  - :nth-child(index)   指定下标  为每个父元素匹配一个指定下标子元素  该下标从1开始计数

- 表单选择器

  具体内容查找jQuery api文档表单选择器一栏



## 文档处理

### 

#### 内部插入

append(content|fn)    向每个匹配的元素内部追加内容

| 参数                   | 含义                                       |
| -------------------- | ---------------------------------------- |
| content              | 要追加到目标中的内容                               |
| function(index,html) | 返回一个html字符串,用于追加到每个匹配元素的里边,index是对象在这个集合中的索引值,html参数是这个对象原先的html值 |

```js
<p>I would like to say: </p>
$("p").append("<b>Hello</b>");
//结果:
[ <p>I would like to say: <b>Hello</b></p> ]//在所有p标签里追加html标记
```

同理  prepend(content)    向每个匹配元素内部的开始出插入内容

#### 外部插入

after(content|fn)		在每个匹配的元素之后插入内容

```js
//实例1
<p>I would like to say: </p>
$("p").after("<b>Hello</b>");
//结果:
<p>I would like to say: </p><b>Hello</b>    //在所有p标签后面插入html标记代码
```

```js
//实例2
<b id="foo">Hello</b><p>I would like to say: </p>
$("p").after( $("#foo")[0] );
//结果:
<p>I would like to say: </p><b id="foo">Hello</b>  //在所有p标签后插入一个DOM元素    注意  将原来的标签提取操作后,被操作的原标签会被删除
```

同理 before(content|fn)   在每个匹配的元素之前插入内容

#### 替换

replaceWith(content|fn)

```js
//实例1
<p>Hello</p><p>cruel</p><p>World</p>
$("p").replaceWith("<b>Paragraph. </b>");
//结果:
<b>Paragraph. </b><b>Paragraph. </b><b>Paragraph. </b>
```

```js
//实例2
<div class="container">
  <div class="first">Hello</div>
  <div class="second">And</div>
  <div class="third">Goodbye</div>
</div>
$('.third').replaceWith($('.first'));
//结果:
<div class="container">
  <div class="second">And</div>
  <div class="first">Hello</div>
</div>			
//用第一段替换第三段,是移动到目标位置来替换,而不是复制一份来替换
```

#### 删除

empty()        删除匹配的元素集合中所有的子节点

```js
<p>Hello, <span>Person</span> <a href="#">and person</a></p>
$("p").empty();
//结果:
<p></p>
```

remove([expr])     从DOM中删除所有匹配的元素

```js
//实例1
<p>Hello</p> how are <p>you?</p>
 $("p").remove();
//结果:
how are			//从DOM中把所有p标签删除
```

```js
//实例2
<p class="hello">Hello</p> how are <p>you?</p>
$("p").remove(".hello");
//结果:
 how are <p>you?</p>    //从DOM中删除带有 hello类的p标签
```

## 筛选

#### 过滤

eq(index|-index)		获取第n个元素

```js
//实例1
<p> This is just a test.</p> <p> So is this</p>
$("p").eq(1)
//结果:
[ <p> So is this</p> ]		//匹配第二个元素
```

```js
//实例2
<p> This is just a test.</p> <p> So is this</p>
$("p").eq(-2)
//结果:
[ <p> This is just a test.</p> ]
```

hasClass(class)		检查当前的元素是否含有某个特定的类  如果有返回true

```js
<div class="protected"></div><div></div>
 $("div").click(function(){
  if ( $(this).hasClass("protected") )
    $(this)
      .animate({ left: -10 })
      .animate({ left: 10 })
      .animate({ left: -10 })
      .animate({ left: 10 })
      .animate({ left: 0 });
});								//操作包含 protected类的该元素
```



## jQuery和js的转换

```js
//jQuery ==>js对象
$('p')[0].style.color = 'red'

//js对象 ==> jQuery
var obj = document.getElementById('bj')
$(onj).css('font-size','50px')

//jQuery对象不能直接调用js中的属性和方法,只能调用jQuery的方法和属性
$('.nav input:eq(0)').click(function(){
	$('.d1 input').prop('checked',true);
	//在事件函数中,this代表的是js对象，$(this)是jQuery对象
	$(this).siblings().prop('checked',false);
})

```

## 样式添加

-addClass    添加类名
-removeClass 移除类名
-toggleClass 切换类名
-attr        获取属性和设置属性（一般针对自定义的特性）
-prop        获取属性和设置属性(元素固有属性)
-val         获取输入框的值
-text        标签中的内容
-html
-css
-width
-height 
-position
-index
-each 遍历



### 最好可以将jQuery的所有方法、属性、选择器都给出一个实例