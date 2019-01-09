## 1、数组

- 数组定义方式

  ~~~
  var a = [1,2,3];
  var b = [];
  var c = new Array();
  ~~~

  - 注意：
    - 数组元素不必是同一种类型
    - 数组元素下标从0开始
    - 数组长度使用length获取

- 数组的访问

  - 下标访问

  - for-in遍历

    ~~~
    var aGrade = [100,30,40,80];
    console.log(aGrade[0]); //访问第一个元素
    aGrade[1] = 70;//修改第二个元素
    delete aGrade[2]; 删除第三个元素的值，但位置保留，值变成了undefined

    //for-in遍历，访问每一个数组元素
    for(index in aGrade) {
      console.log(aGrade[index]);
    }

    //使用for循环访问
    for (var i = 0; i < aGrade.length;i++) {
      console.log(aGrade[i]);
    }
    ~~~

    ​

- 数组函数

  ~~~
  var a = [90,10,30,40];
  var b = [80,68];
  //1 数组合并(concat)
  //参数：数组
  //返回值：返回一个新数组
  var aRes = a.concat(b);
  console.log(aRes);

  //2 数组转字符串(join)
  //功能：把数组元素以指定分隔符连接为一个字符串返回
  //参数：指定的分隔符，是一个字符串
  //返回值：返回以分隔符连接形成的字符串
  console.log(a.join());//默认是以逗号分隔
  consolle.log(a.join('--'));

  //3末尾删除pop
  //功能：删除末尾一个元素，修改数组本身
  //参数：无
  //返回值：返回删除的最后一个元素
  var value = a.pop();
  console.log(value,a);
  //4 末尾添加push
  a.push(80,90);
  console.log(a);

  ~~~

  ​

## 2、基础类库

- Date类
- String类
- Math类
- Array类

------

## 3.Dom

DOM（Document Object Model） 文档对象模型，**定义了访问和操作 HTML 文档的标准。**

 HTML DOM 定义了所有 HTML 元素的对象和属性，以及访问它们的*方法*。通过 HTML DOM，树中的所有节点均可通过 JavaScript 进行访问。所有 HTML 元素（节点）均可被修改，也可以创建或删除节点。

 ![ct_htmltree](image/ct_htmltree.gif)

**在 HTML DOM 中，所有事物都是节点。DOM 是被视为节点树的 HTML。**

- 整个文档是一个文档节点
- 每个 HTML 元素是元素节点
- HTML 元素内的文本是文本节点
- 每个 HTML 属性是属性节点
- 注释是注释节点

## 3.1 获取html节点

1. getElementById	

   - 通过标签的id属性获取单个元素，返回一个对象

   - 只能通过document获取

     ~~~
     var oDiv = document.getElementById('标签的id名');
     ~~~

2. getElementsByTagName

   - 通过标签名获取一组元素，返回一个元素数组

   - 它的父级可以不是document

     ~~~
     var oDiv = 父级.getElementsByTagName('标签名');
     ~~~

3. getElementsByClassName  

   - 通过标签的class属性获取多个元素，返回数组

   - 它的父级可以不是document

     ~~~
     var oDiv = 父级.getElementsByClassName  ('标签的类名');
     ~~~

4. getElementsByName  

   - 通过name获取，返回数组


## 3.2 事件

1. 常用事件

   | 事件          | 触发时机      |
   | ----------- | --------- |
   | onclick     | 点击的时候触发   |
   | ondbclick   | 双击        |
   | onmouseover | 鼠标移到某元素之上 |
   | onmouseout  | 鼠标从某元素移出  |
   | onmouseup   | 鼠标按键被松开   |
   | onmousedown | 鼠标按钮被按下   |
   | onmousemove | 鼠标被移动     |
   | onfocus     | 元素获得焦点    |
   | onblur      | 元素失去焦点    |


## 3.3  修改元素
- 获取到标签元素后可以修改标签的行内样式：

```
var oDiv = document.getElementById('div1');
oDiv.style.backgroundColor = 'red';
```
- 获取到标签后，可读取或修改标签的固有属性
- innerHTML  获取或设置标签中间html代码
- innerText 获取或设置标签中间的文本
- value 获取input的值
- display 控制对象是否显示和消失
- 修改className值，实现换肤（className就是class属性）
  注意：
  - css中所有的属性在js中必须转换为小驼峰

| css中属性           | js中属性           |
| ---------------- | --------------- |
| background-color | backgroundColor |
| margin-left      | marginLeft      |
| padding-left     | paddingLeft     |
| font-size        | fontSize        |
| ....             | ......          |

##4.属性（property)和特性(attribute)

- 在标签里添加的自定义属性称之为特性，不能通过标签.属性名获取或设置

- 获取特性可以使用getAttribute,设置可以使用setAttribute

- 使用js代码给标签动态添加的属性称之为属性，可以通过标签.属性名存取

- 只有标准属性(标签固有属性)才可同时使用标准方法和点号方法

- 对于自定义属性

  - 特性使用getAttribute,设置可以使用setAttribute
  - 代码内添加的属性用点号

  ​


##5. 获取非行内样式

- 在标签里使用style设置的属性称之行间样式或行内样式
- 对于使用<style></style>设置的属性称之为非行内样式或非行间样式
- 对象.style.属性只用于获取和设置行内样式
- 对于非行内样式，获取属性需要使用
  - 对象.currentStyle[属性名] 支持IE
  - getComputedStyle(对象,false)[属性名] 不支持IE，高级浏览器支持

  ​

  ​

##6.定时器

- 一次性定时器
  - 设置定时器：timer = setTimeout(函数,毫秒);
  - 清除定时器：clearTimeout(timer);
  - 只执行一次

- 周期性定时器
  - 设置定时器：timer = setInterval(函数,毫秒);
  - 清除定时器：clearInterval(timer);

效果：反选、联动全选、选项卡

## 作业

1. 代码3遍

2. Date、String、Math，Array里的方法都做一个例子

3. 实现如下图所示功能，点击上箭头，输入框数值增加，点击向下箭头数值减小，如果数值等于0，则不再减小

    ![num](image/num.png)

