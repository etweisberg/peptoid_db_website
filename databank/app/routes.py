# importing important route-related flask functions
from flask import render_template, flash, redirect, url_for, abort
# importing flask application from app module
from app import app
# importing form for searching database
from app.forms import SearchForm, AdvancedQuery
# importing database models
from app.models import Peptoid, Author, Residue
# #for query dictionary
# import json
# import re

def get_home(peptoids):
    peptoid_codes = []
    peptoid_urls = []
    peptoid_titles = []
    peptoid_sequences = []
    images = []
    csds = []
    
    for p in peptoids:
        peptoid_codes.append(p.code)
        peptoid_titles.append(p.title)
        peptoid_urls.append(url_for('peptoid',code=p.code))
        images.append(url_for('static',filename = p.image))
        residues = []
        for residue in p.peptoid_residue:
            residues.append(residue)
        peptoid_sequences.append(", ".join([r.nomenclature for r in residues]))
        csds.append("https://www.ccdc.cam.ac.uk/structures/Search?Doi={doi}&DatabaseToSearch=Published".format(doi=p.doi))

    return [peptoid_codes, peptoid_urls, peptoid_titles, peptoid_sequences, images, csds]


#custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="oops"), 404

# base route


@app.route('/')
# home route displaying all petoids in reverse chron order using home.html template
@app.route('/home')
def home():
    properties = get_home([p for p in Peptoid.query.order_by(Peptoid.release.desc()).all()])
    return render_template('home.html',
            title = 'Gallery',
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# route for all residues renders residues.html
@app.route('/residues')
def residues():
    title = 'Residues'
    residues = [r for r in Residue.query.all()]
    return render_template('residues.html', title=title, residues=residues)
# search route renders the form using the search.html template and the SearchForm() from forms.py
# if the user has submitted the form they are redirected to the route for the serial choice with
# var = their search box input
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('{cat} search requested for {term}'.format(cat=form.option.data.upper(), term=form.search.data),
        'success')
        var = form.search.data
        if '/' in var:
            var = var.replace('/', '$')
        return redirect(url_for(form.option.data, var=var))
    return render_template('search.html',
    title='Search',
    form=form,
    info='Filter by a specific property. To search for a specific sequence or author list separate residues/author last names by commas.',
    description='Peptoid Data Bank - Explore by property')

# #UNUSED route for advanced query boxes
# @app.route('/advanced-query',methods=['GET','POST'])
# def advanced_query():
#     form = AdvancedQuery()
#     if form.validate_on_submit():
#         query = {'seq':form.sequence.data,
#             'res':form.residue.data,
#             'auth':form.author.data,
#             'top':form.topology.data,
#             'exp':form.expriment.data}
#         flash(json.dumps(query))
#         return redirect(url_for('advanced_results',query = json.dumps(query)))
#     return render_template('search.html',
#     title = 'Advanced Query',
#     form = form,
#     info = 'Query by multiple properties using AND or OR statements',
#     description = 'Peptoid Data Bank - Search with Advanced Query'
#     )

# route for each peptoid for a given code renders peptoid.html
@app.route('/peptoid/<code>')
def peptoid(code):
    # data passed to front end
    peptoid = Peptoid.query.filter_by(code=code).first_or_404()
    image = url_for('static', filename = peptoid.image)
    title = peptoid.title
    code = peptoid.code
    release = str(peptoid.release.month) + "/" + \
                  str(peptoid.release.day) + "/" + str(peptoid.release.year)
    experiment = peptoid.experiment
    doi = peptoid.doi

    # lists of objects also passed to front end
    authors = []
    residues = []

    for author in peptoid.peptoid_author:
        authors.append(author)

    for residue in peptoid.peptoid_residue:
        residues.append(residue)

    sequence = ", ".join([r.nomenclature for r in residues])
    author_list = ", ".join([a.last_name for a in authors])
    # rendering html template
    return render_template('peptoid.html',
        peptoid=peptoid,
        image=image,
        title=title,
        code=code,
        release=release,
        experiment=experiment,
        doi=doi,
        authors=authors,
        residues=residues,
        sequence=sequence,
        author_list=author_list
    )

# residue route for residue, nomenclature = var, returns home.html (gallery view)
@app.route('/residue/<var>')
def residue(var):
    initial_peps = {}
    residue = Residue.query.filter_by(nomenclature = var).first_or_404()
    #making dictionary of release date keys and Peptoid values
    for p in residue.peptoids:
        initial_peps[p.release] = p
    #sorting list of datetime keys
    chronological = []
    for key in initial_peps.keys():
        chronological.append(key)
    chronological = sorted(chronological, reverse = True)
    #generating list of peptoid proerties using sorted list
    properties = get_home([initial_peps[date] for date in chronological])

    return render_template('home.html',
            title = 'Filtered by Residue: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# author route for author. If name entered has a space search by both words for first name and last name.
# if name entered is just one word check if it is an author's first name or last name
# returns home.html (gallery view)
@app.route('/author/<var>')
def author(var):
    initial_peps = {}
    
    if " " in var:
        name_split = var.split()
        first_name = name_split[0]
        last_name = name_split[1]
        author = Author.query.filter_by(first_name = first_name, last_name = last_name).first_or_404()
    else:
        author = Author.query.filter((Author.first_name == var) | (Author.last_name == var)).first_or_404()

    # making dictionary of release date keys and Peptoid values
    for p in author.peptoids:
        initial_peps[p.release] = p

    # sorting list of datetime keys
    chronological = []
    for key in initial_peps.keys():
        chronological.append(key)
    chronological = sorted(chronological, reverse = True)

    #generating peptoids according to sorted list date keys
    properties = get_home([initial_peps[date] for date in chronological])

    return render_template('home.html',
            title = 'Filtered by Author: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# experiment route for Peptoid.experimet = var, returns home.html (gallery view), if no peptoid found returns a 404
@app.route('/experiment/<var>')
def experiment(var):
    properties = get_home([p for p in Peptoid.query.order_by(Peptoid.release.desc()).filter_by(experiment = var).all()])
    
    if len(properties[0]) == 0:
        abort(404)

    return render_template('home.html',
            title = 'Filtered by Experiment: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# doi route for Peptoid.doi = var, returns home.html (gallery view), if no peptoid found returns a 404
@app.route('/doi/<var>')
def doi(var):
    var = var.replace('$','/')
    
    properties = get_home([p for p in Peptoid.query.order_by(Peptoid.release.desc()).filter_by(doi = var).all()])

    if len(properties[0]) == 0:
        abort(404)

    return render_template('home.html',
            title = 'Filtered by DOI: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# sequence route for Peptoid residues in a sequence
@app.route('/sequence/<var>')
def sequence(var):
    initial_peps = {}

    # getting peptoids with the same equence
    for p in Peptoid.query.all():
        if var == ",".join([r.nomenclature for r in p.peptoid_residue]):
            initial_peps[p.release] = p

    # making chron order of keys
    chronological = []
    for key in initial_peps.keys():
        chronological.append(key)
    chronological = sorted(chronological, reverse = True)

    #appending peptoids according to reverse chron order
    properties = get_home([initial_peps[date] for date in chronological])
    
    if len(properties[0]) == 0:
        abort(404)

    # returning home
    return render_template('home.html',
            title = 'Filtered by Sequence: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

@app.route('/author-list/<var>')
def author_list(var):
    initial_peps = {}

    # getting peptoids with the same equence
    for p in Peptoid.query.all():
        if var == ",".join([a.last_name for a in p.peptoid_author]):
            initial_peps[p.release] = p

    # making chron order of keys
    chronological = []
    for key in initial_peps.keys():
        chronological.append(key)
    chronological = sorted(chronological, reverse = True)

    #appending peptoids according to reverse chron order
    properties = get_home([initial_peps[date] for date in chronological])
    
    if len(properties[0]) == 0:
        abort(404)

    # returning home
    return render_template('home.html',
            title = 'Filtered by Author List: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# filtering according to topology
@app.route('/top/<var>')
def topology(var):
    properties = get_home([p for p in Peptoid.query.order_by(Peptoid.release.desc()).filter_by(topology = var).all()])

    if len(properties[0]) == 0:
        abort(404)

    return render_template('home.html',
            title = 'Filtered by Topology: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            csds = properties[5]
        )

# about route returns about.html template
@app.route('/about')
def about():
    return render_template('about.html', title="About us")
