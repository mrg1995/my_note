## mongodb的安装

#### 安装与使用

##### 安装

将下载好的安装包解压

>tar -zxvf mongodb-linux-x86_64-ubuntu1604-3.6.5.tgz 

解压后,进入到对应解压目录下的bin目录下  

>cd  /home/guoxd/tool/mongodb-linux-x86_64-ubuntu1604-3.6.5/bin

新建一个 mongod.conf文件 ,这个文件新建在任何位置都可以,在这里为了方便 ,所以在bin目录下新建

这个文件是mongodb的配置文件

```python
verbose=true
#端口号
port=27017
# 日志文件存放目录
logpath=/var/log/mongodb/mongodb.log
# 以append方式写日志
logappend=true
# 数据库存放目录
dbpath=/var/lib/mongodb/db
# 设置每个数据库保存在一个单独的文件夹中
directoryperdb=true
#验证
auth=false
# 守护进程形式运行MongoDB
fork=true
# 安静输出
quiet=true
```

保存退出后,建立对应的目录,文件

>sudo mkdir /var/lib/mongodb/db -p  

>sudo mkdir /var/log/mongodb

>sudo touch  var/log/mongodb/mongodb.log

##### 使用

到/home/guoxd/tool/mongodb-linux-x86_64-ubuntu1604-3.6.5/bin目录下

>sudo ./mongod -f mongod.conf

这样MongoDB就跑起来了



#### 注册开机启动

将解压的文件移动到/usr/local/mongodb/目录下(任意目录都可以,这里做个示例)

>sudo mv  mongodb***-3.6.5/ /usr/local/mongodb

然后将启动的配置文件mongod.conf  移动(或者新建)到  /etc/   目录下

在这里新建一个好了

```python
verbose=true
port=27017
logpath=/var/log/mongodb/mongodb.log
logappend=true
dbpath=/var/lib/mongodb/db
directoryperdb=true
auth=false
fork=true
quiet=true
```



##### 写启动脚本

>sudo vim /etc/init.d/mongodb

```python
. /lib/lsb/init-functions
#!/bin/sh
### BEGIN INIT INFO
# Provides: mongodb
# Required-Start:
# Required-Stop:
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: mongodb
# Description: mongo db server
### END INIT INFO
. /lib/lsb/init-functions
# 这个目录/usr/local/mongodb/bin/需要放到环境变量中
PROGRAM=/usr/local/mongodb/bin/mongod
MONGOPID=`ps -ef | grep 'mongod' | grep -v grep | awk '{print $2}'`
test -x $PROGRAM || exit 0
case "$1" in
 start)
  ulimit -n 65535
   log_begin_msg "Starting MongoDB server"
    # 执行的指令 mongod.conf是你写的MongoDB启动配置文件 
    $PROGRAM -f /etc/mongod.conf
         log_end_msg 0
          ;;
           stop)
            log_begin_msg "Stopping MongoDB server"
                 if [ ! -z "$MONGOPID" ]; then
                  kill -15 $MONGOPID
                   fi
                    log_end_msg 0
                         ;;
                          status)
                           ;;
                            *)
                                 log_success_msg "Usage: /etc/init.d/mongodb {start|stop|status}"
                                  exit 1
                                  esac
                                  exit 0
```

##### 注册该脚本为开机脚本

```python
# 然后给该文件赋予执行权限
sudo chmod +x /etc/init.d/mongodb 

# 注册该文件为开机脚本
sudo update-rc.d mongodb defaults

#如果要移除该开机脚本
sudo update-rc.d -f mongodb remove
```

##### 配置环境变量

```python
sudo vim /etc/profile 或者  sudo vim ~/.bashrc
前者是全局环境变量  后者是 对应用户的环境变量
在最后一行键入

export PATH=/usr/local/mongodb/bin/:$PATH
    
保存退出,然后source一下
source ~/.bashrc
```

##### 使用命令

>sudo service mongodb start    #启动mongodb
>
> sudo service mongodb stop    #停止mongodb

#### 客户端

>mongo

