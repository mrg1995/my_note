## 0. 表单
- 查找表单的三种方法
    - 通用方式
    - 通过document.forms[0]获得form
    - 通过name查找 document.name得到方法
- 表单元素查找 表单.元素名
- 表单提交 document.表单.submit()
## 1. Ajax
AJAX即“Asynchronous Javascript And XML”（异步JavaScript和XML），AJAX 是一种用于创建快速动态网页的技术。
通过在后台与服务器进行少量数据交换，AJAX可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

**必须通过服务器运行页面才能使用ajax的功能**

![ajax](ajax.jpg)

## 2. Ajax使用
- 第一步，创建ajax对象
    - 高级浏览器，包括火狐、chrome、opera，ie7以上
    ```js
    var xhr = new XMLHttpRequest();
    ```
    - ie7及以下
    ```js
    var xhr = new ActiveXObject("Microsoft.XMLHTTP");   //垃圾浏览器的方式
    var xhr = ActiveXObject("Microsoft.XMLHTTP");
    var xhr = new ActiveXObject("Msxml2.XMLHTTP.3.0");  
    var xhr = new ActiveXObject("Msxml2.XMLHTTP.5.0");  
    var xhr = new ActiveXObject("Msxml2.XMLHTTP.6.0");  //IE维护的最高版本
    ```

- 第二步，创建HTTP请求
    - 使用XMLHttpRequest对象的open创建请求
    ```js
    /*参数说明：
    method：该参数用于指定HTTP的请求方法，一共有get、post、head、put、delete五种方法
            ，常用的方法为get和post。
    URL：该参数用于指定HTTP请求的URL地址，可以是绝对URL，也可以是相对URL。
         该文件可以是任何类型的文件，比如 .txt 和 .xml，或者服务器脚本文件，比如 .asp 和 .php（在传回响应之前，能够在服务器上执行任务）。
    flag：该参数为可选参数，参数值为布尔型。该参数用于指定是否使用异步方式。
          true表示异步方式、false表示同步方式，默认为true。
    name：该参数为可选参数，用于输入用户名。如果服务器需要验证，则必须使用该参数。
    password：该参数为可选参数，用于输入密码。
    XMLHttpRequest.open(method,URL,flag,name,password);
    */
    //例
    xhr.open('get','2.py?username=tom&pwd=123');
    ```

    - 如果是get请求，参数需要附加到url里

- 第三步，发送请求
    - 如果是get请求，send参数可以为空；
    - 如果为post请求，参数必须在send参数中传递，参数格式和url中设置的一样
    - 如果为post方式需要在send前，设置请求头信息：xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded")
    ```js
    //get方式
    xhr.send(null);

    //post方式
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.send('username=tom&pwd=123');
    ```
- 第四步，监听Ajax状态变化
  向服务器发送请求的目的是为了获得服务器端的数据，要获得服务器端返回的数据，需要监听XMLHttpRequest的状态，每当XMLHttpRequest状态发生改变时，会触发事件onreadystatechange，我们可以编写onreadystatechange事件处理函数，获取服务器返回的数据。
    - XMLHttpRequest对象的状态，可以通过属性readyState获取，公有以下5种状态：
        - 0: 请求未初始化
        - 1: 服务器连接已建立
        - 2: 请求已接收
        - 3: 请求处理中
        - 4: 请求已完成，且响应已就绪 
    - 当readyState值为4时，就可以获取返回数据了，但返回的数据是成功还是失败，需要根据http的状态码确定，XMLHttpRequest的status属性用于判断http的状态，200表示访问成功
    ```js
    xhr.onreadystatechange = function () {
        if (4 == xhr.readyState) {
    		if (200 == xhr.status ) {
    			alert(xhr.responseText);
    		}
    	}
    };
    ```
- 第五步，获取响应数据
    - 可以通过XMLHttpRequest对象的responseText获取数据，现在已经不再使用responseXML获取数据了
    - 客户端获取json数据
    ```js
    xhr.onreadystatechange = function () {
    	if (4 == this.readyState && 200 == this.status) {
    		//1.通过eval将json字符串转换为对象 
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
        var obj = JSON.parse(json字符串);

        //或者
        var obj = eval('(' + json字符串 + ')');

        //json对象转json串
        var str=obj.toJSONString();
        //或
        var str=JSON.stringify(obj); 
        ```


## 第六步，局部更新客户端页面
## 3. 同步异步
- 同步： ajax请求数据时，客户端js代码必须等服务器返回请求的结果后再继续执行
- 异步： ajax请求数据时，客户端js代码不必等候ajax请求的结果，可以继续执行，啥时候ajax请求返回数据在进行处理。
- 同步请求是onreadystatechange事件处理绑定必须在open前，否则错误。

## 4. ajax封装

~~~
/**
 * [ajax 自定义ajax请求]
 * @param  {[string]} type    [请求类型：post/get]
 * @param  {[string]} url     [请求地址]
 * @param  {[json]} data    [请求参数：{key:value,key:value}]
 * @param  {[funciton]} success [用户自定义的处理函数]
 * @return {[type]}         [无]
 */
function ajax(type,url,data,success){
	//1 创建ajax对象
	var xhr = new XMLHttpRequest();


	//请求参数
	var para = '';

	//将请求参数转换为字符串:key=value&key=value
	//对象遍历，key是属性名，data[key]是属性值
	for(key in data) {
		para += key + '=' + data[key] + '&'
	}

	//截取最后面的&
	//substring(star,end),从start开始截取到end，start和end是字符串索引，索引从0开始
	//最后一个字符索引值为串长度减1
	para = para.substring(0,para.length - 1)
	//console.log(para.substring(0,para.length - 1));

	if ('get' == type) {
		//如果没有？
		if (url.indexOf('?') == -1) {
			url += '?'+para;
		} else {
			url += '&' + para;
		}
	}
	// console.log(url);

	//2 创建请求对象
	//第一个参数是请求类型:get、post
	//第二个参数：url，如果是get请求，请求参数拼接到url后面
	//第三个参数：是同步请求还是异步请求，默认是异步请求
	xhr.open(type,url);


	//3.发送请求
	if ('get' == type) {
		xhr.send(null);
	} else {//post
		xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
		xhr.send(para);
	}
		
	//4.获取服务器返回信息
	xhr.onreadystatechange = function() {
		console.log(xhr.readyState);		
			if (4 == xhr.readyState) {
					if (200 == xhr.status) {
						//xhr.reponseText是服务器返回的信息
						//console.log(xhr.responseText);
						//调用用户自定义处理函数，处理服务器返回信息
						success(xhr.responseText);
			}
		}
	}

}
~~~



## 作业

1.用ajax测试register.php接口，完成用户注册

~~~
请求地址：http://www.codingfans.cc/test/register.php
请求参数：
       用户名： username  字符串类型 
       密码：   password  字符串类型
返回值：返回json字符串
   成功：
     {
        "code":0,
         "message":'注册成功'     
     }
     
    失败：
      {
        'code':1,
        'message:'注册失败'
      }
~~~



​       
