#top level definition of Flask application instance
from app import app, db
from app.models import Peptoid, Author, Residue

#making a shell context for database work
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Peptoid': Peptoid, 'Author': Author, 'Residue': Residue}
