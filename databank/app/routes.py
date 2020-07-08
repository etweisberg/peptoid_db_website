from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
from app.models import Peptoid, Author, Residue

@app.route('/')

#home route
@app.route('/home')
def home():
    peptoid_codes = []
    peptoid_urls = []
    images = []
    for p in Peptoid.query.all():
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))
    return render_template('home.html',
            title = 'Gallery',
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )

#search route
@app.route('/search',methods = ['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for {}'.format(
        form.search.data))
        return redirect(url_for('residue', res = form.search.data))
    return render_template('search.html', title='Search', form=form)

#route for each peptoid
@app.route('/peptoid/<code>')
def peptoid(code):
    #data passed to front end
    peptoid = Peptoid.query.filter_by(code=code).first_or_404()
    image = url_for('static', filename = peptoid.image)
    title = peptoid.title
    code = peptoid.code
    release = peptoid.release
    experiment = peptoid.experiment
    doi = peptoid.doi
    authors = str()
    for auth in peptoid.peptoid_author:
        authors += auth.first_name + ' ' + auth.last_name + ', '
    authors = authors[:-2]
    print(image)
    #rendering html template
    return render_template('peptoid.html',
        peptoid = peptoid,
        image = image,
        title = title,
        code = code,
        release = release,
        experiment = experiment,
        doi = doi,
        authors = authors
    )

@app.route('/residue/<res>')
def residue(res):
    peptoid_codes = []
    peptoid_urls = []
    images = []
    residue = Residue.query.filter_by(nomenclature = res).first_or_404()
    for p in residue.peptoids:
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))

    return render_template('home.html',
            title = 'Residue Search',
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )
