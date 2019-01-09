from flask import Flask,render_template
from app.settings import config
from app.extensions import config_extensions
from app.views import config_blueprint
from app.models import User,Post



# 初始化当前正个应用的函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 给所有第三方扩展库实例化对象
    config_extensions(app)
    # 注册所有蓝本的函数
    config_blueprint(app)
    errors(app)
    return app


def errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/error.html',error=e)

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('errors/error.html', error=e)



