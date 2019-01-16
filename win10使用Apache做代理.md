## win10环境下,在虚拟机搭建一个网站,如何让外网查看?

第一，一直只能本机访问，其他机器访问不了，原因就是apache的配置，需要修改httpd.conf和httpd-vhosts.conf两个问题，我开始只修改了httpd.conf，所以一直没起作用，心里很焦虑。

第二，就是内网可以访问，但是外网访问不了，后来发现是局域网路由器的问题，后来找到了这个解决方案，我把它记录下来了，如果以后有人遇到这个问题，可以参考一下，如下：

用WampServer搭建服务器放网站，需要让外网能访问，本文就以自己的家庭电脑为例演示如何让外网访问本地的WampServer。本文内容来自文章《[How to put online your WampServer](https://www.simonewebdesign.it/how-to-put-online-your-wampserver/)》。



## Apache反向代理

本地运行一个应用,如果没有nginx,可以使用Apache来反向代理

1. 修改httpd.conf中一个值

   ```
   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_ajp_module modules/mod_proxy_ajp.so
   LoadModule proxy_http_module modules/mod_proxy_http.so
   ```

   将这三项的注释去除

2. 在httpd-vhosts.conf中增加如下代码

   ```
   <VirtualHost *:80>
       ServerName 127.0.0.1
       ProxyRequests Off
       <Proxy *>
       Order deny,allow
       Allow from all
       </Proxy>
       ProxyPass / http://192.168.1.12:80/
       ProxyPassReverse / http://192.168.1.12:80/
   </VirtualHost>
   ```

3. 修改系统的hosts文件

   ```
   127.0.0.1    192.168.1.12
   ```

   ​

## 配置路由器，迎接外网的访问

> 本节需要得到的结果：
>
> - 本机公网地址，例如111.161.177.135
> - 本机局域网地址，例如192.168.1.4
> - 需要监听的端口号，例如80，随后要写进apache配置里
> - 设置路由器的端口映射，需要用到局域网地址和端口号

百度一下“我的IP地址”，就能获得自己机器的IP，例如我的地址是111.161.177.135，直接访问这个地址肯定什么也打不开，因为路由器不知道WampServer安装在局域网内的哪台机器上。所以第一步，先要让路由器做端口映射，监听某个端口，将这个端口的访问转到装有服务器的机器的IP地址，例如192.168.1.11

要知道自己机器在局域网内的IP地址，打开windows cmd，输入命令ipconfig，就能得到ip地址

接下来访问路由器的管理界面，地址通常是192.168.1.1，找到服务器的端口映射界面，没有此功能的路由器无法实现外网访问。

添加两条记录，一条UDP，一条TCP。

![端口映射](端口映射.png)

## 配置WampServer，处理80端口的请求

现在，路由器会帮忙把所有对80端口的访问转到IP为192.168.1.11的机器上，这台机器装有WampServer，当它接到请求后，WampServer要负责处理.

- 先来更改httpd.conf，设置监听端口，你可以左键点击WampServer图标，选择Apache->httpd.conf打开这个文件，或者直接找到它

找到

```
#   onlineoffline tag - don't remove
    Require local
```

改为

```
#   onlineoffline tag - don't remove
    Require all granted
```

重启WampServer。







