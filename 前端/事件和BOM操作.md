# 事件和BOM操作

## 一、DOM操作

### 1.查找节点

- parentNode  获得当前元素的父元素
- children 获得当前元素的所有子元素
- firstElementChild
- lastElementChild
- previousElementSibling
- nextElementSibling
- IE8
  - previousSibling 
  - nextSibling
  - firstChild
  - lastChild

### 2. 增加删除元素

- 增加节点应遵循以下步骤：

  - 创建节点

    - createElement   创建节点，只属于document，参数必须是合法的标签名

    ```
    document.createElement('标签名');
    ```

  - cloneNode(boolean deep) 克隆当前节点，deep为true，则同时克隆当前节点的后代节点

  - 添加节点

    - appendChild     追加节点，在父节点的最后面追加一个节点
    - insertBefore    插入节点，插入到父对象下面的某个节点前面

    ```
    oUl.appendChild(oLi);//在父节点末尾追加一个节点
    oUl.insertBefore(oLi,jf);//第一个参数是要插入的节点，第二个是要在哪个节点前插入
    ```

- 删除节点

  - removeChild     删除节点，任何父节点象都可以删除子节点

  - 删除父节点所有的节点  

    ```
    父节点.removeChild(要删除的子节点)
    父节点.innerHTML = '';//全部删除
    ```

## 二.Bom操作

### 1. window对象

- 事件
  - onload 当加载完成，包括资源
  - onresize 当窗体尺寸改变
  - onscroll 当窗体滚动  
- 属性
  - innerWidth  窗口可视区域宽度（包括垂直滚动条的宽）
  - innerHeight  窗口可视区域高度（包括水平滚动条的高）
  - document.documentElement.clientWidth  (不包括垂直滚动条的宽)
  - document.documentElement.clientHeight (不包括水平滚动条的高)


- 弹框
  - alert
  - confirm 确认框
  - prompt 简单信息输入框
  - print()打印页面
- 滚动距离
  - 垂直滚动的距离
    - document.body.scrollTop 只读
    - h5     document.documentElement.scrollTop  只读
  - 水平滚动的距离
    - document.body.scrollLeft 只读
    - h5 document.documentElement.scrollLeft

### 2、history对象

- back() 前一页

- forward（） 后一页

- go(页)  正数向后跳转，负数向前跳转

- 阻止浏览器默认跳

  ```
  <a href="http://www.baidu.com" onclick='return jump()'>百度</a>

  var oA = document.getElementsByTagName('a')[0];
  oA.onclick = function(e){
  	// var res = confirm("你确认跳转到垃圾百度吗？");
  	// if (res) {
  	// 	return true;
  	// } else {
  	// 	return false;
  	// }
  	var ev = e || event;

  	//阻止浏览器的默认跳转行为
  	ev.preventDefault();
  }
  ```

  ​

  ### 3 获得对象坐标和宽高（只读）

  - obj.offsetTop：距离顶部的偏移
  - obj.offsetLeft：距离左边的偏移
  - obj.offsetWidth：获取对象宽度
  - obj.offsetHeight：获取对象高度
  - document.title  窗口标题

## 三、事件绑定

### 1. 事件冒泡

- 当点击一个标签元素时，点击事件会从事件发生的元素开始，依次向该元素的父节点传递。

- 事件也是对象

- 非ie浏览器事件是通过事件处理函数的参数传递的

- ie浏览器使用全局变量event获得事件

- 获得事件对象，兼容不同浏览器的写法：

  var ev = e || event;

- 取消事件冒泡，就是取消事件向父节点传递

  ev.cancelBubble = true; 

  或者

  ev.stopPropagation();

### 2. 事件绑定

- 实现一个事件对应多个处理函数需要使用事件绑定机制

  - 非IE浏览器使用addEventListener方法给事件绑定处理方法
    //事件名称不要带on，例如onclick应该写click
    需要绑定的对象.addEventListener(事件名称,处理方法,可选第三个参数);
  - IE浏览器使用attachEvent方法绑定处理方法
    //事件名称带on，例如onclick
    obj.attachEvent(事件名称，处理方法);

- 兼容ie浏览器的事件绑定写法

  ```
  function bindEvent1(obj,eventnName,fn)
  {
      if (obj.addEventListener) {
      	obj.addEventListener(eventnName,fn,false);
      } else {
       obj.attachEvent('on'+eventnName,fn);
      }
  }
  ```

  ​

- 移除由addEventListener添加的事件处理函数

  - 高级浏览器使用  removeEventListener

  - ie8及早期版本使用detachEvent

  - 兼容性写法： 

    ```
    function removeEvent(obj,ev,func) 
    {
        if (obj.removeEventListener) 
        {
            obj.removeEventListener(ev, func);
        } else if (obj.detachEvent) 
        {
            obj.detachEvent("on"+ev, func);
        }
    }
    ```

    ​

### 3. 事件源

- 事件源就是发生事件的对象。

  - 谷歌和ie使用事件的srcElement表示事件源

  - 火狐使用target表示事件源

    var ev = e || event;
    var obj = ev.srcElement;

- 鼠标的位置(对象的左上角为（0,0）)

  var ev = e || event;
  var x = ev.clientX;
  var y = ev.clientY

- 阻止鼠标右键弹出菜单

  ```
  document.oncontextmenu = function ()
  {
      return false;	
  }
  ```

  ​

- 鼠标跟随

  ```
  document.onmousemove = function(e)
  {

      var ev = e || event;
      var top = ev.clientY;
      var left = ev.clientX;
      	
      ....
  }	
  ```

  ​

### 4. 键盘事件

- obj.onkeydown 按下键
- obj.onkeyup  松开按键
- 获取键值：event.keyCode
  - altKey 是否按下alt键
  - ctrlKey 是否按下control键
  - shiftKey 是否按下shift键

## 四 表单

- 查找表单的三种方法
  - 通用方式
  - 通过document.forms[0]获得form
  - 通过name查找 document.name得到方法
- 表单元素查找 表单.元素名
- 表单提交 document.表单.submit()