from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class LoginForm(FlaskForm):
    username = StringField(label='username',render_kw={'placeholder':'username'},validators=[DataRequired()])
    password = PasswordField(label='password',render_kw={'placeholder':'password'},validators=[DataRequired()])
    remember_me = BooleanField()
    sign_in = SubmitField(label='sign in')

class RegisterForm(FlaskForm):
    username = StringField(label='username',render_kw={'placeholder':'username'},validators=[DataRequired(),Length(0,255)])
    password = PasswordField(label='password',render_kw={'placeholder':'password'},validators=[DataRequired(),Length(0,255)])
    repeat_password = PasswordField(label='repeat password',render_kw={'placeholder':'repeat password'},validators=[EqualTo('password')])
    email = EmailField(label='email',render_kw={'placeholder':'email'},validators=[DataRequired(),Email(),Length(0,255)])
    remember_me = BooleanField()
    register = SubmitField(label='register')

class ResetPasswordForm(FlaskForm):
    email = EmailField(label='email',render_kw={'placeholder':'email'},validators=[DataRequired(),Email()])
    send_email = SubmitField(label='send email')

class NewPasswordForm(FlaskForm):
    password = PasswordField(label='password',render_kw={'placeholder':'password'},validators=[DataRequired(),Length(0,255)])
    repeat_password = PasswordField(label='repeat password',render_kw={'placeholder':'repeat_password'},validators=[EqualTo('password')])
    update_password = SubmitField(label='update password')
