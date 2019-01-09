from app.forms import Posts
from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import Post
from app.extensions import db, cache

posts = Blueprint('posts', __name__)


# 发表帖子

@posts.route('/send_posts/', methods=['GET', 'POST'])
def send_posts():
    form = Posts()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # 拿到实例化的对象
            u = current_user._get_current_object()
            p = Post(content=form.content.data, user=u)
            db.session.add(p)
            flash('帖子发表成功')
            cache.clear()
            return redirect(url_for('main.index'))
        else:
            flash('还未登陆,请登录')
            return redirect(url_for('user.login'))
    return render_template('posts/send_posts.html', form=form)


@posts.route('/favorite/<pid>')
def favorite(pid):
    # 如果收藏了  就清除缓存
    cache.clear()
    try:
        if current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
        else:
            current_user.add_favorite(pid)
        return jsonify({'stat': 200})
    except:
        return jsonify({'stat': 500})




