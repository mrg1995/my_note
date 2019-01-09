```
blog/
	App/
    	__init__.py  #包文件
        static/		#静态文件目录
        	img/
            css/
            js/
            upload
        templates/	#模板文件目录
        	common/
        views/		#视图目录
			__init__.py
        modles/		#模型目录
        	__init__.py
        forms/		#表单目录
        	__init__.py
        settings.py	#配置文件
        extensions.py	#加载第三方扩展库的文件
        email.py		#发送邮件的文件
    venv/
    migrations/
    manage.py
```

![flask_day1](D:\stu\老师资料\week13(夏利g)\day6项目第一天\flask_day1.png)

#### 1 在app/settings.py中将环境配置确认**(配置)**

```python
# app/settings.py
# 所有环境配置的基类
class Config(object):
    SECRET_KEY = 'jiami'

# 测试配置
class TestiongConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/testing'

# 开发配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/hz1802'

# 生产配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/development'

# 将不同的配置写到字典中,方便后续操作
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestiongConfig,
    'default': DevelopmentConfig,
}
```

```python
# app/__init__.py
# 导入settings.py中设置的配置字典
from app.settings import config
from flask import Flask

# 传入的config_name参数 是 字典中对应环境的key值
def create_app(config_name):
	app=Flask(__name__)
    # form_object()方法  参数是config中的环境类  
    # 将app的环境定义为指定的环境
    app.config.form_object(config[config_name])
    return app
```

#### 2 在app/extensions.py文件中 **(第三方库)**

```python
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# 导数据的 Migrate 类 
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)

# 初始化应用的方法  该方法后面要导入 app/__init__.py中 去初始化
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
```

```python
# app/__init__.py
from app.settings import config
from flask import Flask
# 导入 初始化第三方应用的方法
**from app.extensions import config_extensions
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化第三方应用
    **config_extensions(app)
    return app
```

#### 3 在app/views/_init_.py文件中**(蓝本)**

这个文件主要导入各个蓝本,并将这些蓝本整合,并注册

```python
# app/views/__init__.py

# 这两个导入的都是蓝本 
from .main import main
from .user import user

#因为蓝本的数量可能会比较多  可以将它们放到列表中,去循环注册
# 里面的数据是元组  元组中 参数1是蓝本类,参数2是url_prefix
BluePrint = [
    (main, ''),
    (user, '')
]

# 封装一个循环注册蓝本的函数, 后面也要导入到app/_init_.py中
def config_blueprint(app):
    for blueprint, prefix in BluePrint:
        app.register_blueprint(blueprint, url_prefix=prefix)
```

```python
# app/__init__.py
from app.settings import config
from flask import Flask
from app.extensions import config
# 导入注册蓝本的函数
**from app.views import config_blueprint

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config_extensions(app)
    # 执行注册蓝本的函数
    **config_blueprint(app)
    return app
```

#### 4 在manage.py文件中 (执行文件)

```python
from flask_script import Manager
# 导入app/_init_.py 文件中的create_app函数 
# 这个函数 配置了app的config,注册了蓝本,初始化了第三方应用
from app import create_app
# 导入 MigrateCommand 对 manager对象 增加数据库导入的命令
from flask_migrate import MigrateCommand

app = create_app('default')
# 实例化 manager
manager = Manager(app)
# 给manage添加迁移文件的命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

```
# 生成迁移文件目录
python manage.py db init
# 生成迁移文件
python manage.py db migrate
# 执行迁移文件
python manage.py db upgrade
```

到这里,flask的基本的框架分离基本上已经完成了

接下来要做的,无非就是蓝本的完善,因为蓝本包括了 forms表单,models,templates,后台逻辑等





