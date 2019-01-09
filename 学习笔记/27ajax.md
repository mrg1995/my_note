## 0.表单

- 查找表单的三种方法
  - 通用方法
  - 通过document.form[0]  获得form
  - 通过name查找  document.name得到方法
- 表单内元素查找      表单.元素名
- 表单提交    document.表单.submit()      

## 1.Ajax

AJAX即“Asynchronous Javascript And XML”（异步JavaScript和XML），AJAX 是一种用于创建快速动态网页的技术。
通过在后台与服务器进行少量数据交换，AJAX可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

![img](file:///D:/Program%20Files/feiq/Recv%20Files/27/ajax.jpg?lastModify=1524476400)

## 2.Ajax使用

- #### 第一步,创建ajax对象

  - 高级浏览器

    ```js
    var xhr = new XMLHttpRequest();
    ```

  - ie7及以下

    ```js
    var xhr = new ActiveXObject("Microsoft.XMLHTTP");
    ```

- #### 第二步

  - 使用XMLHttpRequest对象的open创建请求

    ```js
    /*参数说明：
    method：该参数用于指定HTTP的请求方法，一共有get、post、head、put、delete五种方法
            ，常用的方法为get和post。
    URL：该参数用于指定HTTP请求的URL地址，可以是绝对URL，也可以是相对URL。
         该文件可以是任何类型的文件，比如 .txt 和 .xml，或者服务器脚本文件，比如 .asp 和 .php（在传回响应之前，能够在服务器上执行任务）。
    async：该参数为可选参数，参数值为布尔型。该参数用于指定是否使用异步方式。
          true表示异步方式、false表示同步方式，默认为true。
    name：该参数为可选参数，用于输入用户名。如果服务器需要验证，则必须使用该参数。
    password：该参数为可选参数，用于输入密码。
    XMLHttpRequest.open(method,URL,flag,name,password);
    */
    //例
    xhr.open('get','2.py?username=tom&pwd=123');
    ```

  - 如果是get请求,参数需要附加到url里

- #### 第三步,发送请求

  - 如果是get请求,send参数为null;

  - 如果是post参数,参数必须在send参数中传递,参数格式和url中设置的一样

  - 如果为post方式需要在send前,设置请求头信息

    ```
    注意:  XMLHttpRequest对象.open()中的参数3 async 为false时  
      该	XMLHttpRequest对象.send()   这个方法会阻塞并不会返回，直到 readyState 为 4 并且服务器的响应被完全接收后才继续执行后续js代码
      XMLHttpRequest对象.open()中的参数3 async 为true时
      该XMLHttpRequest对象.send() 立即返回(不会阻塞后续js代码的执行)，服务器的响应将在一个后台线程中处理。即readyState 会依次返回 0,1,2,3,4
    ```

    ````js
    //get方式
    xhr.send(null)

    //post方式
    //添加请求头后,再send(data)
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.send('username=tom&pwd=123')
    ````

    ​

- #### 第四步,监听Ajax状态变化

  ​      向服务器发送请求的目的是为了获得服务器端的数据，要获得服务器端返回的数据，需要监听XMLHttpRequest的状态，每当XMLHttpRequest状态发生改变时，会触发事件onreadystatechange，我们可以编写onreadystatechange事件处理函数，获取服务器返回的数据

  - XMLHttpRequest对象的状态,可以通过属性readyState获取,共有5中状态
    - 0:请求未初始化
    - 1:服务器连接已建立
    - 2:请求已接收
    - 3:请求处理中
    - 4:请求已完成,且响应已就绪
  - 当readyState值为4时.就可以获取返回数据,但返回的数据是成功还是失败,需要根据http的状态码确定.XMLHttpRequest的status属性用于判断http的状态,200表示访问成功 

  ````js
   xhr.onreadystatechange = function () {
        if (4 == xhr.readyState) {
          //判断status属性  200表示访问成功
    		if (200 == xhr.status ) {
    			alert(xhr.responseText);
    		}
    	}
    };
  ````

  ​

- #### 第五步    获取响应数据

  - 可以通过XMLHttpRequest对象的responeText获取数据
  - 客户端获取json数据

  ```js
  xhr.onreadystatechange = function () {
  	if (4 == this.readyState && 200 == this.status) {
  		//1.通过eval将json字符串转换为对象 
        //注意:eval 会把括号内的字符串当代码块来执行   因此不建议使用这种方式来获取数据
  	   // var obj = eval('('+xhr.responseText+')');
  	   // console.log(obj);
  		
  	   //2 使用json.parse将json字符串转换为对象
  	   obj = JSON.parse(this.responseText);
  	   console.log(obj);
  	}
  };
  ```

  - JSON字符串和JSON对象的转换

  ```js
  //json字符串 ==> json对象
  var obj = JSON.parse(json字符串)

  //或者
  var obj = eval('('+json字符串+")")

  //json对象 ==> json字符串
  var str = obj.toJSONString()
  //或者
  var str = JSON.stringify(obj)
  ```

  ​

## 3.局部更新客户端页面



#### 	1.同步异步

- 同步: XMLHttpRequest对象.open()中的   参数3 async 为false时  
    该	XMLHttpRequest对象.send()   这个方法会阻塞并不会返回，直到 readyState 为 4 并且服务器的响应被完全接收后才继续执行后续js代码

- 异步:  XMLHttpRequest对象.open()中的   参数3 async 为true时

   该XMLHttpRequest对象.send() 立即返回(不会阻塞后续js代码的执行)，服务器的响应将在一个后台线程中处理。即readyState 会依次返回 0,1,2,3,4

- 因此同步请求时,需要把onreadystatechange监听事件放在send()之前,若放在send()后面,因为readyState已经变化完了(已经是4了),将不会截取到变化,那么该监听事件也就没意义了.

  #### 2.ajax封装





day27

2018.4.23

19:01