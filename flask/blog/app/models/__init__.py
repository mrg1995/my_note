from .user import User
from .posts import Post
from app.extensions import db

# 创建一个收藏中间表
collections = db.Table('collections',db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                       db.Column('posts_id',db.Integer,db.ForeignKey('post.id')))









