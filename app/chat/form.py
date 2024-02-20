from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class ChatForm(FlaskForm):
    message = StringField(label='message',render_kw={'placeholder':'message'},validators=[DataRequired(),Length(0,255)])
    send = SubmitField(label='send')

class MessageForm(FlaskForm):
    message = StringField(label='message',render_kw={'placeholder':'message'},validators=[DataRequired(),Length(0,255)])
    send = SubmitField(label='send')