from flask_login import current_user
from datetime import datetime
from flask import Blueprint
from app.system_db import db_session
from flask import g
from app._jwt import generate_token
from app.form import SearchForm

def update_last_seen(blueprint:Blueprint):
    @blueprint.before_app_request
    def update_last_seen():
        current_user.last_seen = datetime.utcnow()
        db_session.commit()
def generate_token_(blueprint:Blueprint):
    @blueprint.before_app_request
    def generate_jwt():
        g.token = generate_token

def search_form_(blueprint:Blueprint):
    @blueprint.before_app_request
    def search_form():
        g.search = SearchForm()