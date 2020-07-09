from flask import render_template, flash, redirect, url_for, abort
from app import app
from app.forms import SearchForm
from app.models import Peptoid, Author, Residue

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')

#home route
@app.route('/home')
def home():
    logo = url_for('static', filename = 'pep1.png')
    peptoid_codes = []
    peptoid_urls = []
    images = []
    for p in Peptoid.query.order_by(Peptoid.release.desc()).all():
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))
    return render_template('home.html',
            logo = logo,
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
        flash('{cat} search requested for {term}'.format(cat = form.option.data.upper(), term = form.search.data))
        var = form.search.data
        if '/' in var:
            var = var.replace('/','$')
        return redirect(url_for(form.option.data, var = var))
    return render_template('search.html', title='Search', form=form)

#route for each peptoid
@app.route('/peptoid/<code>')
def peptoid(code):
    #data passed to front end
    peptoid = Peptoid.query.filter_by(code=code).first_or_404()
    i = peptoid.image
    i = i[:-4]
    image = url_for('static', filename = i + '_full.png')
    title = peptoid.title
    code = peptoid.code
    release = peptoid.release
    experiment = peptoid.experiment
    doi = peptoid.doi
    
    #lists of objects also passed to front end
    authors = []
    residues = []

    for author in peptoid.peptoid_author:
        authors.append(author)

    for residue in peptoid.peptoid_residue:
        residues.append(residue)

    #rendering html template
    return render_template('peptoid.html',
        peptoid = peptoid,
        image = image,
        title = title,
        code = code,
        release = release,
        experiment = experiment,
        doi = doi,
        authors = authors,
        residues = residues
    )

@app.route('/residue/<var>')
def residue(var):
    peptoid_codes = []
    peptoid_urls = []
    images = []
    residue = Residue.query.filter_by(nomenclature = var).first_or_404()
    
    for p in residue.peptoids:
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))

    return render_template('home.html',
            title = 'Filtered by Residue: ' + var,
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )

@app.route('/author/<var>')
def author(var):
    name_split = []
    peptoid_codes = []
    peptoid_urls = []
    images = []
    space = " "
    if space in var:
        name_split = var.split()
        first_name = name_split[0]
        last_name = name_split[1]
        author = Author.query.filter_by(first_name = first_name, last_name = last_name).first_or_404()
    else:
        author = Author.query.filter((Author.first_name == var) | (Author.last_name == var)).first_or_404()
    
    for p in author.peptoids:
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))
    
    return render_template('home.html',
            title = 'Filtered by Author: ' + var,
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )

@app.route('/experiment/<var>')
def experiment(var):
    peptoid_codes = []
    peptoid_urls = []
    images = []
    for p in Peptoid.query.filter_by(experiment = var).all():
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))
    
    if len(peptoid_codes) == 0:
        abort(404)
    
    return render_template('home.html',
            title = 'Filtered by Experiment: ' + var,
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )

@app.route('/doi/<var>')
def doi(var):
    var = var.replace('$','/')
    peptoid_codes = []
    peptoid_urls = []
    images = []
    
    for p in Peptoid.query.filter_by(doi = var).all():
        peptoid_codes.append(p.code)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static', filename = p.image))

    if len(peptoid_codes) == 0:
        abort(404)
    
    return render_template('home.html',
            title = 'Filtered by DOI: ' + var,
            peptoid_codes = peptoid_codes,
            peptoid_urls = peptoid_urls,
            images = images
        )

