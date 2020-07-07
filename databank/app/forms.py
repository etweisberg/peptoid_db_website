from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#making form for searching data bank
class SearchForm(FlaskForm):
    search = StringField('Enter search terms', validators=[DataRequired()])
    submit = SubmitField('Go')
