from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
from app.models import Peptoid, Author

@app.route('/')

#home route
@app.route('/home')
def home():
    return render_template('home.html',title = 'Home')

#search route
@app.route('/search',methods = ['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for {}'.format(
        form.search.data))
        return redirect(url_for('index'))
    return render_template('search.html', title='Search', form=form)
