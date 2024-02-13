from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField(label='search',render_kw={'placeholder':'search'},validators=[DataRequired()])
    send_search = SubmitField(label='search')