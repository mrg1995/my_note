## 博客服务器搭建过程记录  Nginx + uwsgi + Django


### 第一步   Django已完成项目  设置修改

- settings.py 文件的修改

  ```
  //settings.py
  DEBUG = False
  ALLOWED_HOSTS = ['*']

  # STATICFILES_DIRS 是在开发过程中 使用django自带服务器时  设置的静态文件路径
  # STATIC_ROOT 这个路径是 执行 ./manage.py collectstatic (将每个app中静态文件汇总)  后 那些静态文件放的路径  
  # 当放到nginx服务器上时 保留STATIC_ROOT路径  以方便以后修改

  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  # STATICFILES_DIRS = [
  #     os.path.join(BASE_DIR, 'static')
  # ]   
  ```

- 在与manage.py同级目录下 创建project.conf  文件

- 在配置前  先看下原理

  ```
  #首先客户端请求服务资源，
  #nginx作为直接对外的服务接口,接收到客户端发送过来的http请求,会解包、分析，
  #如果是静态文件请求就根据nginx配置的静态文件目录，返回请求的资源，
  #如果是动态的请求,nginx就通过配置文件,将请求传递给uWSGI；uWSGI 将接收到的包进行处理，并转发给	wsgi，
  #wsgi根据请求调用django工程的某个文件或函数，处理完后django将返回值交给wsgi，
  #wsgi将返回值进行打包，转发给uWSGI，
  #uWSGI接收后转发给nginx,nginx最终将返回值返回给客户端(如浏览器)。
  #*注:不同的组件之间传递信息涉及到数据格式和协议的转换
  ```

  ```
  # project.conf 
  user www-data;
  worker_processes auto;
  pid /run/nginx.pid;

  events {
  	worker_connections 768;
  	# multi_accept on;
  }

  http {
  	sendfile on;
  	tcp_nopush on;
  	tcp_nodelay on;
  	keepalive_timeout 65;
  	types_hash_max_size 2048;
  	include /etc/nginx/mime.types;
  	default_type application/octet-stream;
  	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
  	ssl_prefer_server_ciphers on;
  	access_log /var/log/nginx/access.log;
  	error_log /var/log/nginx/error.log;
  	gzip on;
  	gzip_disable "msie6";
  	include /etc/nginx/conf.d/*.conf;
  	include /etc/nginx/sites-enabled/*;
  	
  	# 以下需配置
  	server {
        listen         80;
        server_name    www.19950314nina.top;   # 你的服务器的域名地址
        charset UTF-8;
        access_log      /var/log/nginx/myweb_access.log; 
        error_log       /var/log/nginx/myweb_error.log;
    
        client_max_body_size 75M;
  	#如果是动态的请求,nginx将请求传递给uWSGI；uWSGI将接收到的包进行处理，并转发wsgi，
        location / {
           include uwsgi_params;
           uwsgi_pass 127.0.0.1:8000;    # 注意  这个8000端口需要和后面的 uwsgi.ini 端口一致
           uwsgi_read_timeout 10;    # 时间建议可以长一些  否则有时会返回504
        }
       #如果是静态文件请求 根据nginx配置的静态文件目录，返回请求的资源，
        location /static {
            expires 30d;
            autoindex on;
            add_header Cache-Control private;
            alias /home/mrg/PycharmProjects/myblog/static/; # 你的静态文件路径  即之前在setting.py 设置的 STATIC_ROOT 的路径
       }
     }
  }
  ```


- 在与manage.py同级目录下 创建projectname_uwsgi.ini文件

  ```
  [uwsgi]
  socket = :8000   # 注意 需要和nginx的配置文件端口一致
  chdir=/home/mrg/PycharmProjects/myblog  # django项目目录绝对路径
  module= myblog.wsgi		# wsgi.py在项目中的相对路径 
  master = true         
  processes=2
  threads=2
  max-requests=2000
  chmod-socket=664
  vacuum=true
  daemonize = /home/mrg/PycharmProjects/myblog/uwsgi.log # uwsgi日志存储路径 可以不写  
  ```

  ```
  #简易版本
  [uwsgi]
  socket= :8000
  chdir = /home/mrg/PycharmProjects/myblog  #django项目目录绝对路径
  module = myblog.wsgi
  master = true
  processes = 4
  vacumm = true
  ```

- 最后

  - 去nginx配置文件的根目录拷贝**mime.types**(/etc/nginx/mime.types),以及**uwsgi_params**复制到工程目录**和project.conf放在一起**。


### 第二步 使用git

对我来说  使用git 比较方便  

也可以选择其他方式上传文件到服务器

- Github创建一个空仓库 

- 在项目目录下执行以下步骤

  ```
  git init   #初始化项目
  git remote add origin 远程仓库地址   # 链接远程仓库
  git add .  # 添加代码文件
  git commit -m '初始版本'  #代码提交到本地库
  git push origin master   # 代码推送到仓库
  ```

  如果出现代码冲突情况

  ```
  #如果希望保留生产服务器上所做的改动,仅仅并入新配置项, 处理方法如下:
  git stash
  git pull
  git stash pop

  #如果希望用代码库中的文件完全覆盖本地工作版本. 方法如下:
  git reset --hard
  git pull
  ```

- 使用ubuntu自带的ssh 工具登陆 服务器

  ```
  ssh username@10.31.125.165
  ```

  顺利连上之后 创建用户(如果已经有了就不需要重复了)

  ```
  # 在 root 用户下运行这条命令创建一个新用户，mrg 是用户名
  # 选择一个你喜欢的用户名，不一定非得和我的相同
  root@localhost:~# useradd -m -s /bin/bash mrg

  # 把新创建的用户加入超级权限组
  root@localhost:~# usermod -a -G sudo mrg

  # 为新用户设置密码
  # 注意在输密码的时候不会有字符显示，不要以为键盘坏了，正常输入即可
  root@localhost:~# passwd mrg

  # 切换到创建的新用户
  root@localhost:~# su  mrg

  # 切换成功，@符号前面已经是新用户名而不是 root 了
  mrg@localhost:~$
  ```


### 第三步  环境配置 

- 安装常见的库

```
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install man gcc  make sudo lsof ssh openssl tree vim dnsutils iputils-ping net-tools psmisc sysstat curl telnet traceroute wget libbz2-dev libpcre3 libpcre3-dev libreadline-dev libsqlite3-dev libssl-dev zlib1g-dev git mysql-server mysql-client zip  p7zip mycli
```

- 创建虚拟环境

  ```
  - sudo apt-get python3-pip
  - sudo pip3 install virtualenv  
  - sudo virtualenv -p python3 env_name  创建虚拟环境
  - source ~/env_name/bin/active    开启虚拟环境
  - pip install uwsgi  安装uwsgi
  - deactivate  退出虚拟环境
  - sudo ufw allow 80   开启80端口

  ```

- mysql数据库修改字符集

  ```
  修改mysql的配置文件

  cd /etc/mysql/mysql.conf.d

  sudo cp mysql.cnf  mysql.cnf.bak

  sudo vim mysql.cnf

  在[mysqld]下增加一句：

  character_set_server = utf8

  保存并重启服务

  sudo systemctl restart mysql.service  #重启服务
  ```

- 安装Nginx

  ```
  sudo apt-get install nginx  #安装
  sudo /etc/init.d/nginx start[or stop or restart]  #启动,关闭,重启
  ```


### 第四步  一些设置的确认及修改

- 数据库的一些操作

  ```
  # 创建用户
  grant all on *.* to 'django'@'%' identified by 'djangopwd';
  # 刷新使用户生效
  flush privileges;
  # 创建对应的表
  create database project
  ```

- django数据库迁移,以及静态文件夹的生成

  ```
  #cd到项目目录下
  ./manage.py makemigrations  # 生成迁移文件
  ./manage.py migrate  # 迁移
  ./manage.py collectstatic  # 生成静态文件夹
  ```

- 确认项目目录下配置文件中的路径是否和服务器上对应的路径一致

  - 主要为以下需要确认的配置文件

    ```
    1.settings.py 

    2.project.conf
    alias /home/mrg/PycharmProjects/myblog/static/; # 你的静态文件路径  即之前在setting.py 设置的 STATIC_ROOT 的路径

    3.projectname_uwsgi.ini
    chdir=/home/mrg/PycharmProjects/myblog  # django项目目录绝对路径

    主要是2,3 两个文件中的路径是否设置正确
    ```

- 确认无误后

  ```
  # cd 到项目目录下
  uwsgi --ini project_uwsgi.ini   

  nginx -c /home/mrg/PycharmProjects/myblog/project.conf    # 注意该路径必须为绝对路径

  ```



到这里基本上已经配置完成了,你也可以在网页上打开你的页面了

**-----------------------------------------------------------------------------------------------------------------------------**

1. 如果启动时就报错，查看终端信息，解决错误。 
   如果终端没有报错，但是浏览时出现500、502等错误，就去项目目录查看nginx日志和uWSGI日志，解决错误。
2. 在本文中，使用了virtualenv开发环境,但只是用单独的一个conf文件，在nginx上部署了一个工程，没有说明部署多个工程的问题,也没有说明使用supervisor来管理进程等。请根据个人爱好和需要去实践扩展。

### 后记

**献给和我一样懵懂中不断汲取知识，进步的人们。**

------

霓虹闪烁，但人们真正需要的，只是一个可以照亮前路的烛光

参考博客: 

https://blog.csdn.net/c465869935/article/details/53242126

https://www.cnblogs.com/fnng/p/5268633.html

https://www.zmrenwu.com/post/20/