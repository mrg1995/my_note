import os
from app.models import User
from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from app.forms import Register, Login, Icon, User_info
from app.extensions import db, file, cache
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image

user = Blueprint('user', __name__)


@user.route('/register/', methods=['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():
        # 实例化user
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()
        # 生成token
        token = u.generate_token()
        # 发送邮件
        send_mail('邮件激活', form.email.data, 'activate', username=form.username.data, token=token)
        # 提示注册
        flash('注册成功,去激活')
        # 跳转登陆页面
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_token(token):
        flash('激活成功 ')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


# 登陆
@user.route('/login/', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('该用户不存在')
        elif not u.confirm:
            flash('未激活')
        elif u.checked_password_hash(form.password.data):
            flash('登陆成功')
            cache.clear()
            login_user(u, remember=form.remeber.data)
            return redirect(url_for('main.index'))
        else:
            flash('请输入正确的密码')
    return render_template('user/login.html', form=form)


# 退出登陆
@user.route('/logout/')
def logout():
    cache.clear()
    logout_user()
    flash('退出成功')
    return redirect(url_for('main.index'))


@user.route('/test/')
@login_required
def test():
    return '必须登陆后才能访问'


def new_name(shuffix, length=32):
    import string, random
    myStr = string.ascii_letters + '0123456789'
    return ''.join(random.choice(myStr) for i in range(length)) + shuffix


# 修改头像

@user.route('/change_icon/', methods=['POST', 'GET'])
def change_icon():
    form = Icon()
    if form.validate_on_submit():
        shuffix = os.path.splitext(form.file.data.filename)[-1]
        print(current_app.config['UPLOADED_PHOTOS_DEST'])
        while True:
            newname = new_name(shuffix)
            print(newname)
            if not os.path.exists(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], newname)):
                break
        file.save(form.file.data, name=newname)
        # 执行缩放
        img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], newname))
        img.thumbnail((300, 300))
        # 保存缩略图 名称为s
        img.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], 's_' + newname))
        # 判断用户更改完头像
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], 's_' + current_user.icon))

        current_user.icon = newname
        db.session.add(current_user)
        flash('头像上传成功')

    img_url = file.url(current_user.icon)
    cache.clear()
    return render_template('user/change_icon.html', form=form, img_url=img_url)


@user.route('/user_info_change/', methods=['POST', 'GET'])
@login_required
def change_user_info():
    form = User_info()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        u.username = form.data.get('username')
        u.sex = form.data.get('gender')
        u.age = form.data.get('age')
        db.session.add(u)
        cache.clear()
        flash('个人信息修改完成')
        return redirect(url_for('user.user_info'))
    return render_template('user/user_info_change.html', form=form)


@user.route('/user_info/')
@login_required
def user_info():
    user = current_user._get_current_object()
    if user.sex:
        user.gender = '女'
    else:
        user.gender = '男'
    return render_template('user/userinfo.html', user=user)








