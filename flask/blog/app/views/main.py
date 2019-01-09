from flask import Blueprint, render_template, redirect, url_for,current_app
from app.models import Post,User
from app.extensions import cache

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.page_show',page=1))


@main.route('/page_show/<int:page>/')
@cache.memoize(timeout=500)
# @cache.cached(timeout=100,key_prefix='index')
# 显示页面 传入页数
def page_show(page):
    print('能看到我几次')
    # 从数据库中提取出page参数对应的对象
    # pid为0 创建时间倒序
    # paginate()类  参数1是第几页  参数2是每页显示的数量(放到config中管理起来方便)
    #参数3是查询出错时是否抛出错误
    pagination = Post.query.filter_by(pid=0).order_by(Post.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    # 当前page的所有数据
    data = pagination.items
    # 将数据传入模板
    return render_template('main/index.html',data=data,pagination=pagination)