from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,FileField,SubmitField
from wtforms.validators import Length

class ChangeDataProfileForm(FlaskForm):
    username = StringField(label='username',render_kw={'placeholder':'username'},validators=[Length(0,255)])
    about_me = TextAreaField(label='about me',render_kw={'placeholder':'about me'})
    change = SubmitField(label='change')

class AvatarForm(FlaskForm):
    avatar = FileField()
    change_avatar = SubmitField(label='change avatar')
