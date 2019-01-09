# pymysql操作mysql数据库

## 一、外键

如果表A的主关键字是表B中的字段，则该字段称为表B的外键，表A称为主表，表B称为从表

- 数据库引擎必须是innodb
- 主表和从表相关的外键字段类型必须兼容

~~~
创建外键
ALTER TABLE 从表名
ADD CONSTRAINT 外键名称 FOREIGN KEY (从表的外键列) REFERENCES 主表名 (主键列) 
[ON DELETE reference_option]
[ON UPDATE reference_option]

reference_option:
RESTRICT | CASCADE | SET NULL | NO ACTION
  1. CASCADE: 从父表中删除或更新对应的行，同时自动的删除或更新子表中匹配的行。ON DELETE CANSCADE和ON UPDATE CANSCADE都被InnoDB所支持。
  
  2. SET NULL: 从父表中删除或更新对应的行，同时将子表中的外键列设为空。注意，这些在外键列没有被设为NOT NULL时才有效。ON DELETE SET NULL和ON UPDATE SET SET NULL都被InnoDB所支持。

  3. NO ACTION: InnoDB拒绝删除或者更新父表。

  4. RESTRICT: 拒绝删除或者更新父表。指定RESTRICT（或者NO ACTION）和忽略ON DELETE或者ON UPDATE选项的效果是一样的。

删除外键
ALTER TABLE 从表 DROP FOREIGN KEY 外键名
~~~



## 二、视图

有时候经常会遇到复杂的查询，写起来比较麻烦，这时候我们可以使用视图简化查询。视图就是固化的sql语句，可以不把视图当做基本表使用

- 不要在视图上进行增、删、改

~~~
创建视图
create view 视图名(字段列表) as 
select子句

删除视图
drop view 视图名
~~~



## 三、pymysql操作mysql数据库

- 安装pymysql

    ~~~
    pip install pymysql
    ~~~

### 3.1 pymysql操作数据库的五行拳

1. 连接数据库

   使用Connect方法连接数据库

   ~~~
   pymysql.Connections.Connection(host=None, user=None, password='', database=None, port=0,  charset='')
   参数说明：
       host – 数据库服务器所在的主机。
       user – 登录用户名。
       password – 登录用户密码。
       database – 连接的数据库。
       port – 数据库开放的端口。（默认: 3306）
       charset – 连接字符集。
   返回值：
      返回连接对象
      
   例子：
   link = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', db='zzl', charset='utf8')

   ~~~

   - 连接对象方法

   | 方法                  | 说明              |
   | ------------------- | --------------- |
   | begin()             | 开启事务            |
   | commit()            | 提交事务            |
   | cursor(cursor=None) | 创建一个游标用来执行sql语句 |
   | rollback()          | 回滚事务            |
   | close()             | 关闭连接            |
   | select_db(db)       | 选择数据库           |

2. 创建游标

   ~~~
   cursor = link.cursor()
   print(cursor.rowcount) #打印受影响行数
   ~~~

   | 方法                        | 说明                                       |
   | ------------------------- | ---------------------------------------- |
   | close()                   | 关闭游标                                     |
   | execute(query, args=None) | 执行单条语句，传入需要执行的语句，是string类型；同时可以给查询传入参数，参数可以是tuple、list或dict。执行完成后，会返回执行语句的影响行数。 |
   | fetchone()                | 取一条数据                                    |
   | fetchmany(n)              | 取多条数据                                    |
   | fetchall()                | 取所有数据                                    |

3. 执行sql语句

   ~~~
   # 执行sql语句
   sql = 'select * from user1'
   # 执行完sql语句，返回受影响的行数
   num = cursor.execute(sql)
   ~~~

4. 获取结果集

   ~~~
   result1 = cursor.fetchone()
   print(result1)
   ~~~

5. 关闭连接

   ~~~
   cursor.close()
   link.close()
   ~~~

- 注意：

  写完代码后，需要将py文件添加可执行权限 

  ~~~
  sudo chmod +x conndb.py
  ./conndb.py
  ~~~


### 3.2 pymysql中事务处理

pymysql默认是没有开启自动提交事务，所以我们如果进行增、删、改，就必须手动提交或回滚事务。

~~~
sql = 'delete from user where id=%s' % user_id

# 如果要执行增删改语句的时候，下面的就是固定格式
try:
	cursor.execute(sql)
	# 如果全部执行成功，提交事务
	link.commit()
	print(cursor.lastrowid) #获取最后插入记录的自增id号
except Exception as e:
	print(e)
	link.rollback()
finally:
	cursor.close()
	link.close()

~~~

