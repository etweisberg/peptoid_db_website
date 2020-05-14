from app import app
from app.models import Peptoid

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Peptoid': User}
