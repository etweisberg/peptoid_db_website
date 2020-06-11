from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
from app.models import Peptoid

@app.route('/')
@app.route('/index')
def index():
    peptoid = Peptoid.query.all()[0]
    code = peptoid.code
    return render_template('index.html',title = 'Home',code = code)

@app.route('/search',methods = ['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for {}'.format(
        form.search.data))
        return redirect(url_for('index'))
    return render_template('search.html', title='Search', form=form)
