from .main import main
from .user import user
from .posts import posts

BluePrint = [
    (main, ''),
    (user, ''),
    (posts, ''),
]


# 封装一个注册蓝本的函数
def config_blueprint(app):
    for blueprint, prefix in BluePrint:
        app.register_blueprint(blueprint, url_prefix=prefix)
