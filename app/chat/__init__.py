from flask import Blueprint
chat_bp = Blueprint('chat_bp',__name__,template_folder='templates')
from app.route import generate_token_
generate_token_(chat_bp)
from app.route import search_form_
search_form_(chat_bp)
from app.chat import route