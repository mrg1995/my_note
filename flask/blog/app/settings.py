import os
base_path=os.path.abspath(os.path.dirname(__file__))

# 所有环境配置的基类
class Config(object):

    SECRET_KEY = 'jiami'
    # 追踪数据库对象是否改变
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 数据库自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '17764501101@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '19975201314AI')
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    # 配置上传文件
    MAX_CONTENT_LENGTH=1024*1024*64
    UPLOADED_PHOTOS_DEST=os.path.join(base_path,'static/upload')
    #
    PAGE_NUM = 3
    # 缓存存活时间
    # CACHE_DEFAULT_TIMEOUT = 200

# 测试配置
class TestiongConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/testing'


# 开发配置
class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/hz1802'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_path,'develop.sqlite')

# 生产配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/production'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestiongConfig,
    'default': DevelopmentConfig,
}
