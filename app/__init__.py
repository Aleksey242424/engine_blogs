from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from elasticsearch import Elasticsearch
from flask_moment import Moment

login = LoginManager()
mail = Mail()
moment = Moment()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    login.init_app(app)
    app.es = Elasticsearch(hosts=[app.config['ELASTICSEARCH_HOST']],basic_auth=(app.config['ELASTICSEARCH_USERNAME'],app.config['ELASTICSEARCH_PASSWORD']))
    login.login_view = 'auth_bp.login'
    login.login_message = 'Пожалуйста авторизуйтесь'
    mail.init_app(app)
    moment.init_app(app)
    from app.auth import auth_bp
    from app.chat import chat_bp
    from app.profile import profile_bp
    from app.posts import posts_bp
    app.register_blueprint(auth_bp,url_prefix='/')
    app.register_blueprint(chat_bp,url_prefix='/chat/')
    app.register_blueprint(profile_bp,url_prefix='/profile/')
    app.register_blueprint(posts_bp,url_prefix='/posts/')
    return app
