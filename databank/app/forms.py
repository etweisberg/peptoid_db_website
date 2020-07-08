from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

#making form for searching data bank
class SearchForm(FlaskForm):
    option = RadioField('Select an option for searching the peptoid data bank', choices=[
        ('residue','Peptoid Residue'),
        ('author','Name of Author'),
        ('experiment','Experimental Technique'),
        ('doi','DOI'),
        ])
    search = StringField('Enter search terms', validators=[DataRequired()])
    submit = SubmitField('Go')
