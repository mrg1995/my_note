#mysql数据库

## 一、子查询

- 子查询嵌入到其他查询语句中查询语句，子查询只能出现在from，where中
- 子查询不要用select *,exists除外

~~~
select title 
from forum 
where uid in (select id from php_user where name='王琨' );
~~~

##二、多表查询

- 多表连接必须**要有连接条件**，否则结果没有意义
- 多表连接有两种写法：隐式(标准sql)和显式内连接
- 隐式(标准sql)连接 ：  连接条件写到where字句中

 ~~~
select title,content,name,publish_time 
from user u,forum f  #给表起一个别名，方便书写
where u.id = f.uid; 在where写链接条件
			 
select title,content,name,publish_time 
from user u,forum f 
where u.id = f.uid and name='王琨';


select a.username,b.name ,c.title
    -> from bbs_user a,bbs_category b,bbs_forum c
    -> where b.cid = c.cid and c.uid = a.uid;

 ~~~

- 显示内连接（inner join）

 ~~~
mysql> select a.uid,username,title,content 
    -> from bbs_user a inner join bbs_forum b on a.uid =b.uid #关联条件
    -> where a.uid < 5;  #过滤条件
    
    select username,name,title
    -> from bbs_user a inner join bbs_forum c on c.uid =a.uid 
    -> inner join bbs_category b on c.cid = b.cid;

 ~~~

- 表的自身连接

 ~~~
select c2.name 
from category c1,category c2
where c1.pid = c2.cid;
 ~~~

## 三、外连接

两张表关联查询时，根据以那种表为主可以分为左外连接和右外连接

- 左外连接  

​      以左表为主，如果右边的表里没有匹配的记录，则添加一个万能记录（各个字段都为null)与之连接

    ​~~~
select *
from user u left join forum f
on u.id =f.uid;
    ​~~~

- 右外连接

以右表为主，如果左边的表里没有匹配记录，则增加一个万能记录与之连接



## 四、集合操作

可以使用union将两个查询结果合并，mysql只支持并，不支持差和交

- 两个结果集中字段数一样，对应字段类型兼容
- 自动去除重复记录,不去除重复记录可以用 union all
- order by 放到最后

  ~~~
  select * from student where class = '95031'
  union all
  select * from student where ssex='女';
  ~~~



## 五、数据控制

###5.1 事务

- 事务把一组操作看做一个整体，要不都操作成功，要不都操作失败 。
- 表的数据库引擎必须是innodb，innodb支持事物，myisam不支持事务
- 修改表引擎：alter table  表名 engine = innodb

  查询是否为自动提交
  select @@autocommit  (1为自动提交   0为手动提交)
  关闭自动提交
  set autocommit = 0

  start transaction /begin
  一组操作
  commit/rollback

  commit 提交 会把数据写到硬盘
  rollback 回滚 撤销操作

###5.2 授权管理

- 创建用户

   ~~~
   create user '用户名'@'服务器地址' identified by '密码'
   ~~~

- 删除用户

  ~~~
  drop user  '用户名'@'服务器地址'
  ~~~

- 修改密码

  ~~~
  修改当前登录用户
  set password = password('123456');
  			
  一般管理员可以修改任意用户密码
  set password for 'db'@'localhost' = password('2333');
  ~~~

- 刷新

  ~~~
  flush privileges
  ~~~

- 授权

  ~~~
   grant 权限  on 数据库.表  to '用户名'@'服务器地址'
    grant all on *.* to 'dd'@'localhost'
  	 *.* 所有数据库的所有表
  	 all 代表所有权限  
  	 权限包括：select、update、delete、alter
  ~~~

- 回收

  ~~~
   revoke select on test.stars from 'db'@'localhost';
  ~~~

## 六、索引

索引就像图书的目录，可以加快查询速度

- where和order by经常出现的字段可以添加索引
- 频繁修改、删除、插入的表不要加索引
- 索引会占用磁盘空间

###  普通索引

    ​~~~
create index 索引名 on 表名(字段 asc/desc) 默认asc升序
    ​~~~

###  唯一索引

  在唯一索引所在列不能有重复值

~~~
create  unique index 索引名 on 表名(字段 asc/desc) 默认asc升序
~~~

###  主键索引

  创建表，主键索引会自动添加，要求在主键上不能有重复值，不能有空值

### 全文索引（了解）

   一般会用全文索引服务器，不会直接创建全文索引

  ~~~
create  FULLTEXT index 索引名 on 表名(字段 asc/desc)
  ~~~

### 删除索引

  ~~~
drop index 索引名 on 表
  ~~~

### 查看索引

   ~~~
show index form 表 
   ~~~

### 其它创建索引的方式

 ~~~
alter table 表 add index(字段1,字段2,...)
alter table 表 add primary key(字段1,字段2,...)
alter table 表 add unique(字段1,字段2,...)
alter table 表 add fulltext(字段1,字段2,...)
 ~~~





