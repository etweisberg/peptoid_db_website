#imports forms modules from flask wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired

#making form for searching data bank with radiofield for selecting search option and string
#field for input
class SearchForm(FlaskForm):
    option = RadioField('Select an option for searching the peptoid data bank',
    validators = [InputRequired()],
    choices=[
        ('residue','Peptoid Residue'),
        ('author','Name of Author'),
        ('experiment','Experimental Technique'),
        ('doi','DOI'),
        ])
    search = StringField('Enter search terms', validators=[DataRequired()])
    submit = SubmitField('Go')
