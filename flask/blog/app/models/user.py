from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
# 生成token的模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from flask import current_app
from flask_login import UserMixin
from app.extensions import login_manage
from .posts import Post


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(40))
    icon = db.Column(db.String(70), default='default.jpg')
    # 当前账户激活状态
    confirm = db.Column(db.Boolean, default=False)
    # 参数1是模型名称 参数2 是反向引用的字段名称  参数3是加载方式  提供对象
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    # secondary 参数 在多对多关系中,指定关联表的名称
    favorite = db.relationship('Post', secondary='collections', backref=db.backref('users', lazy='dynamic'),
                               lazy='dynamic')

    # 使用  添加使用 append  删除使用 remove

    @property
    def password(self):
        raise ValueError

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 生成token的方法
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'], expires_in=200)
        return s.dumps({'id': self.id})

    # 检测token的方法
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        # 从当前的token中拿出id
        try:
            id = s.loads(token)['id']
        except:
            return False
        # 根据id 拿出对应用户的对象
        u = User.query.get(id)
        # 判断对象是否存在
        print('11')
        if not u:
            return False
        # 判断当前用户的激活状态, 没激活的话,就激活
        if not u.confirm:
            u.confirm = True
            print('激活')
            db.session.add(u)
            db.session.commit()
            return True
        print('22')
        return False

    # 验证密码
    def checked_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    # 判断当前用户是否收藏了这个帖子
    # 传入的是帖子的id
    def is_favorite(self, postsId):
        # 查询提取该用户收藏的所有帖子
        all = self.favorite.all()
        for p in all:
            # 当用户收藏了这个帖子  返回true 否则返回false
            if p.id == int(postsId):
                return True
        return False
        # if len(list(filter(lambda p:p.id==int(postsId),all))):
        # return True

    # 定义一个收藏方法
    def add_favorite(self, pid):
        self.favorite.append(Post.query.get(pid))

    # 定义一个取消收藏的方法
    def remove_favorite(self, pid):
        self.favorite.remove(Post.query.get(pid))


# 登陆认证的回调,保持数据的一致性
@login_manage.user_loader
def user_loader(num):
    print('111')
    return User.query.get(int(num))
