##  sqlalchemy 模型

#### 安装： sudo pip3 install flask-sqlalchemy

#### orm使用的好处

1. 增加少sql的重复使用率
2. 使表更加的可读性
3. 可移植性



## 一、原生sql

#### (1) 新建一个数据库

create database if not exists 库名 character set utf8;

alter database 库名 character set utf8;

alter table 表名 character set utf8;

alter table 表名 modify 字段名 字段类型 可选约束条件 character set utf8

### (2) 安装操作数据库的模块

pip3 install pymysql

### (3) 安装 flask-sqlalchemy

sudo pip3 install flask-sqlalchemy

### (4) 配置路径

DB_URI = 'mysql+pymysql://root:password@host:port/database'



**实例**

```python
from sqlalchemy import create_engine

HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'demo'
PORT = 3306
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)

engine = create_engine(DB_URI)

with engine.connect() as db:
    data = db.execute('select * from user')
    # print(data)
    # for row in data:
    #     print(row)
    db.execute('delete from user where id=1')
```



## 二、在flask中使用ORM模型

#### 配置

```python
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#配置链接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/demo'
#开启自动提交 不需要提交或者回滚
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#关闭数据追踪的配置 关闭占据额外的消耗的资源
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #实例化ORM
manager = Manager(app)
```



## 三、设计表模型

#### (1) 字段类型

| 类型名       | python中的类型    | 说明           |
| ------------ | ----------------- | -------------- |
| Integer      | int               | 存储整形 32位  |
| SmallInteger | int               | 小整形 16为    |
| BigInteger   | int               | 大整形         |
| Float        | float             | 浮点数         |
| String       | str               | 字符串 varchar |
| Text         | str               | 长文本         |
| Boolean      | bool              | bool值         |
| Date         | datetimedate      | 日期           |
| Time         | datetime.time     | 时间           |
| datetime     | datetime.datetime | 时间日期       |

#### (2) 可选条件

| 选项        | 说明                    |
| ----------- | ----------------------- |
| primary_key | 主键                    |
| unique      | 唯一索引                |
| index       | 常规索引                |
| nullable    | 是否可以为null 默认True |
| default     | 默认值                  |



## 四、创建模型

```python
#自定义模型类
class User(db.Model):
    __tablename__ = 'user' #起表名
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    sex = db.Column(db.Boolean,default=True)
    info = db.Column(db.String(50))
```

#### 创建表

```python
@app.route('/create')
def create():
    db.drop_all() #删除表
    db.create_all() #创建表
    return '创建表'
```



## 五、数据的增add add_all 删 delete 改

### (1) 添加一条数据 add

```python
@app.route('/insert/')
def insert():
    try:
        u = User(username='王五',info='王五的默认值')
        db.session.add(u)
        db.session.commit() #事物的提交
    except:
        db.session.rollback() #回滚
        pass
    return '添加数成功'
```

### (2) 添加多条数据 add_all

```python
@app.route('/insert_many/')
def insert_many():
    u1 = User(username='李四', info='李四的默认值')
    u2 = User(username='小胖', info='小胖的默认值')
    db.session.add_all([u1,u2]) #多条数据对象 放在列表中
    db.session.commit()
    return '添加多条数据'
```

### (3) 修改数据

```python
#数据的修改
@app.route('/update/')
def update():
    u = User.query.get(1)  #拿到id为1的数据对象
    # print(u) #数据对象
    # print(u.username) #获取username属性的值
    u.username = '不起昵称会死嘛？'
    db.session.add(u)
    db.session.commit()
    return '修改'
```

### (4) 删除 delete

```python
#删除
@app.route('/delete/')
def delete():
    u = User.query.get(1)
    db.session.delete(u)
    db.session.commit()
    return '删除id为1的数据'
```

**注意：**

sqlalchemy默认开启了事物处理

操作完成以后需要提交或者回滚

```python
db.session.commit()
db.session.rollback()
```



## 六、拆分成mvt

目录结构

```python
project/
	manage.py
    exts/
    settings.py
    app/
    	__init__.py
        models.py
        views.py
     templates/
     static/
```



## 七、自定义增删改类

#### model中的代码

```python
class Base:
    #保存
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()  # 事物的提交
        except:
            db.session.rollback() #回滚
    #静态方法
    @staticmethod
    def save_all(List):
        try:
            db.session.add_all(List)
            db.session.commit()  # 事物的提交
        except:
            db.session.rollback() #回滚
    #删除
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()  # 事物的提交
        except:
            db.session.rollback() #回滚
#自定义模型类
class User(db.Model,Base):
    ...
```

#### 在views中的使用

```python
#添加数据
@view.route('/insert/')
def insert():
    # u = User(username='王五',info='王五的默认值')
    u = User('张三','张三的默认值')
    u.save()
    return '添加数据'

@view.route('/saveall/')
def saveall():
    u1 = User('张123','张123的默认值')
    u2 = User('123张','123张的默认值')
    User.save_all([u1,u2])
    return '添加多个值'

@view.route('/delete/')
def delete():
    u1 = User.query.get(3)
    u1.delete()
    return '删除数据'
```



## 八、数据库的操作

#### 查询集

数据查询的集合

1. 原始查询集

   不经过任何过滤器返回的结果集 为原始查询集

2. 数据查询集

   将原始查询集经过条件的筛选最终返回的数据



### 过滤器

#### (1)  all() 得到所有的数据查询集 返回列表

类名.query.all() 不能够链式调用

```python
@view.route('/all/')
def all():
    data = User.query.all()
    print(data)
    return '删除数据'
```

### (2) filter()  过滤默认查询所有

类名.query.filter()

类名.query.filter(类名.属性名 条件操作符 条件)

```python
#filter 获取所有数据查询集
@view.route('/filter/')
def filter():
    # data = User.query.filter()
    # data = User.query.filter(User.username=='王五')
    data = User.query.filter(User.username=='王五',User.sex==False)
    print(data)
    for i in data:
        print(i.username,i.sex)
    return '删除数据'
```

### (3) filter_by() 单条件查询

```python
@view.route('/filter_by/')
def filter_by():
    # data = User.query.filter_by()
    #错误写法
    # data = User.query.filter_by(id!=1)
    data = User.query.filter_by(age=18)
    #只能为下面这种关键字的用法   且多个添加为and操作
    # data = User.query.filter_by(username='王五',sex=False)
    # data = User.query.filter_by(username='王五',sex=False)
```

### (4) offset(num) 偏移量

```python
@view.route('/offset/')
def offset():
    # data = User.query.filter().offset(1)
    # data = User.query.filter().offset(2)
    #错误的用法
    data = User.query.all().offset(2)
    # print(User.query.filter())
    # print(data)
    # for i in data:
    #     print(i.username,i.sex)
    return '删除数据'
```

### (5) limit()  取值

```python
@view.route('/offsetlimit/')
def offsetlimit():
    data = User.query.offset(2).limit(2)
    print(data)
    for i in data:
        print(i.username,i.sex)
    return 'limit'
```

### (6) order_by() 排序

1. 默认升序
2. -属性名

```python
@view.route('/orderby/')
def orderby():
    #升序
    data = User.query.order_by(User.age).limit(1)
    #降序
    data = User.query.order_by(-User.age).limit(1)
```

### (7) first()  取出一条数据

```python
@view.route('/first/')
def first():
    # data = User.query.first()  == User.query.get(1)
    # data = User.query.order_by(-User.age).first()
    data = User.query.order_by(User.age).first()
    print(data.age)
    print(data.username)
    # for i in data:
    #     print(i.username,i.sex)
```

### (8) get() 取得id值的数据  

查询成功 返回 对象

查询失败 返回 None

```python
data = User.query.get(10)
print(data)
```

### (9) contains  包含关系

类名.query.filter(类名.属性名.contains('值'))

```python
data = User.query.filter(User.username.contains('五'))
```

### (10) like 模糊查询

类名.query.filter(类名.属性名.like('%值%'))

```python
data = User.query.filter(User.username.like('%张%')) #包含张
data = User.query.filter(User.username.like('%张'))	#以张作为结尾	
data = User.query.filter(User.username.like('张%'))	#以张作为开头
```

### (11) startswith 以...开头		endswith以...结尾

```python
data = User.query.filter(User.username.startswith('张')) #以 张作为开头
data = User.query.filter(User.username.endswith('张'))	#以张作为结尾
```

### (12) 比较运算符

1. `__gt__` 大于
2. `__ge__` 大于等于
3. `__lt__` 小于
4. `__le__` 小于等于
5. `>`
6. `<`
7. `>=`
8. `<=`
9. `!=`
10. `==`

```python
data = User.query.filter(User.id>1) #查询id大于1的数据
data = User.query.filter(User.id.__gt__(1)) #查询id大于1的数据
data = User.query.filter(User.id.__ge__(1)) #查询id大于1的数据
data = User.query.filter(User.id>=1) #查询id大于1的数据
data = User.query.filter(User.id<3) #查询id大于1的数据
data = User.query.filter(User.id.__lt__(3)) #查询id大于1的数据
```

### (13) in_ 和 not in 是否包含某个范围内

```python
#in的使用
@view.route('/in/')
def myin():
    data = User.query.filter(User.id.in_([1,2,3,4])) #在...范围内
    data = User.query.filter(~User.id.in_([1,2,3,4])) #not in不再...范围内
    data = User.query.filter(User.username.in_(['张三','王五']))
    return render_template('show.html',data=data)
```

### (14) is_ 	isnot 查询为null/不为null 的数据

```python
#对于null数据的处理
@view.route('/null/')
def null():
    #查询为null数据的
    data = User.query.filter(User.username.is_(None))
    data = User.query.filter(User.username == None)
    data = User.query.filter(~User.username.isnot(None))
    #查询不为null数据的
    data = User.query.filter(~User.username.is_(None))
    data = User.query.filter(User.username.isnot(None))
    data = User.query.filter(User.username != None)
    
    return render_template('show.html',data=data)
```



## 九、数据库的逻辑查询

```python
from sqlalchemy import and_,or_,not_
```

### (1) 逻辑与 and_

```python
#逻辑操作
@view.route('/and/')
def myand():
    data = User.query.filter(User.sex==True,User.age<20)
    data = User.query.filter(User.sex==True).filter(User.age<20)
    data = User.query.filter(and_(User.sex==True,User.age<20))
    return render_template('show.html',data=data)
```

### (2) 逻辑活 or_

```python
#逻辑操作
@view.route('/or/')
def myor():
    #or
    data = User.query.filter(or_(User.sex==True,User.age<20),User.id.in_([1,2,3]))
    #and 和 or的 一起使用
    data = User.query.filter(or_(User.sex==True,User.age<20))
    return render_template('show.html',data=data)
```

### (3) 逻辑非  not_

```python
#逻辑操作
@view.route('/not/')
def mynot():
    data = User.query.filter(not_(User.sex==True))
    #错误写法只能有一个条件
    data = User.query.filter(not_(User.sex==True,User.id!=1))
    data = User.query.filter(~User.sex==True)
    return render_template('show.html',data=data)
```

### (4) count 统计

```python
@view.route('/count/')
def mycount():
    #统计性别为sex的数据条数
    data = User.query.filter(not_(User.sex == True)).count()
    #统计所有数据的条数
    data = User.query.filter().count()
    data = User.query.count()
    return '{}条数据'.format(data)
```



## 十、flask-migrate  文件的迁移

安装：

1. flask-script
2. flask-migrate

**使用**

```python
from flask_migrate import Migrate,MigrateCommand
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand) #给manage添加迁移文件的命令
```

### (1) 生成迁移文件目录

python3 manage.py db init

生成 一个 migrations的迁移文件目录

### (2) 生成迁移文件

python3 manage.py db migrate

### (3) 执行迁移文件

python3 manage.py db upgrade





















































