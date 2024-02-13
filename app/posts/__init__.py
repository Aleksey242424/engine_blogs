from flask import Blueprint
posts_bp = Blueprint('post_bp',__name__,template_folder='templates')
from app.route import generate_token_
generate_token_(posts_bp)
from app.route import search_form_
search_form_(posts_bp)
from app.posts import route