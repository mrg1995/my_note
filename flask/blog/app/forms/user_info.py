from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, ValidationError, BooleanField, RadioField,IntegerField, SelectField
from wtforms.validators import DataRequired, Length,NumberRange


class User_info(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空'), Length(min=6, max=12, message='长度为6到12位')],render_kw={'placeholder': '请输入用户名'})
    gender = SelectField('性别',coerce=int,choices=[(0,'男'),(1,'女')])
    age = IntegerField('年龄',validators=[DataRequired(message='年龄不能为空'),NumberRange(6,100,message='请输入正确的年龄')],render_kw={'placeholder':'请输入您的年龄'})
    submit = SubmitField('修改')











