from os import getenv
from dotenv import load_dotenv

class Config:
    load_dotenv()
    DEBUG = True
    SECRET_KEY = getenv('SECRET_KEY')
    UPLOAD_FOLDER = getenv('UPLOAD_FOLDER')
    JWT_KEY = getenv('JWT_KEY')
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USE_TLS = getenv('MAIL_USE_TLS')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    ELASTICSEARCH_HOST = getenv('ELASTICSEARCH_HOST')
    ELASTICSEARCH_USERNAME = getenv('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD = getenv('ELASTICSEARCH_PASSWORD')

    
    