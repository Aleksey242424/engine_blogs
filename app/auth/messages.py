from app import mail
from flask_mail import Message
from flask import render_template

def reset_password_message(token,email):
    msg = Message(subject='reset your password',recipients=[email])
    msg.html = render_template('auth/reset_password_message.html',token=token)
    mail.send(msg)