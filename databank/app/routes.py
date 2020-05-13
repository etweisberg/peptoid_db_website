from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm

@app.route('/')
@app.route('/index')
def index():
    peptoid = {
    'name':'19AB1-2-A',
    'experiment':'X-ray diffraction',
    'authors':'Castellano, V.; Chippindale, A.M.; Hamley, I.W.; Barnett, S.; Hasan, A.; Lau, K.H.A.'
    }
    return render_template('index.html',title = 'Home',peptoid = peptoid)

@app.route('/search',methods = ['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for {}'.format(
        form.search.data))
        return redirect(url_for('index'))
    return render_template('search.html', title='Search', form=form)
