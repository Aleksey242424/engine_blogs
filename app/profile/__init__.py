from flask import Blueprint
profile_bp = Blueprint('profile_bp',__name__,template_folder='templates')
from app.route import generate_token_
generate_token_(profile_bp)
from app.route import search_form_
search_form_(profile_bp)
from app.route import update_last_seen
update_last_seen(profile_bp)
from app.profile import route