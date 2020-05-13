from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    peptoid = {
    'name':'19AB1-2-A',
    'experiment':'X-ray diffraction',
    'authors':'Castellano, V.; Chippindale, A.M.; Hamley, I.W.; Barnett, S.; Hasan, A.; Lau, K.H.A.'
    }
    return render_template('index.html',title = 'Home',peptoid = peptoid)
