from flask_login import current_user
from datetime import datetime
from flask import Blueprint,request
from app.system_db import db_session
from flask import g
from app._jwt import generate_token
from app.form import SearchForm
from app.system_db.chats import Chats

def update_last_seen(blueprint:Blueprint):
    @blueprint.before_app_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db_session.commit()

def generate_token_(blueprint:Blueprint):
    @blueprint.before_app_request
    def generate_jwt():
        if current_user.is_authenticated:
            g.token = generate_token

def search_form_(blueprint:Blueprint):
    @blueprint.before_app_request
    def search_form():
        if current_user.is_authenticated:
            g.search = SearchForm()


def generate_chat_id_(blueprint:Blueprint):
    @blueprint.before_app_request
    def generate_chat_id():
        if current_user.is_authenticated:
            g.chat_id = Chats.get_chat_id