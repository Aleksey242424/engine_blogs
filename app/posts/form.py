from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,FileField,SubmitField
from wtforms.validators import DataRequired,Length

class PostNameBodyForm(FlaskForm):
    post_name = StringField(label='post name',render_kw={'placeholder':'title'},validators=[DataRequired(),Length(0,255)])
    body = TextAreaField(label='body',render_kw={'placeholder':'content'},validators=[DataRequired(),Length(0,3000)])
    create_post = SubmitField(label='create_post')


class LikeDislikeForm(FlaskForm):
    like = SubmitField(label='+')
    dislike = SubmitField(label='-')