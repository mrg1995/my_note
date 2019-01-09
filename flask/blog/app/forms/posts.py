from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length


class Posts(FlaskForm):
    content = TextAreaField('发表博客',validators=[DataRequired(message='帖子不能为空'),Length(6,100,message='6到100字')],render_kw={'placeholder':'发表想法','style':'resize:none;'})
    # submit = SubmitField('发表')





















