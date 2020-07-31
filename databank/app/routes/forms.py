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
        ('residue','Search by a residue'),
        ('author','Search by an author'),
        ('topology','Search by a topology type'),
        ('experiment','Search by an experimental technique'),
        ('doi',"Search by DOI"),
        ('sequence', "Search for a specific sequence"),
        ('author_list',"Search for a specific list of authors")
        ])
    search = StringField('Enter a search term', validators=[DataRequired()])
    submit = SubmitField('Go')

class ApiRequest(FlaskForm):
    search = StringField('Enter peptoid code', validators=[DataRequired()])
    submit = SubmitField('Request')

# class AdvancedQuery(FlaskForm):
#     sequence = StringField('Sequence')
#     residue = StringField('Residues')
#     author = StringField('Authors')
#     topology = StringField('Topologies')
#     expriment = StringField('Experiments')
#     submit = SubmitField('Go')