# importing important route-related flask functions, form for searching database, database models, blueprint for routes
from flask import render_template, flash, redirect, url_for, abort
from app.routes.forms import SearchForm, ApiRequest
from app.models import Peptoid, Author, Residue
from app.routes import bp

def get_home(peptoids):
    peptoid_codes = []
    peptoid_urls = []
    peptoid_titles = []
    sequence_max = 128
    peptoid_sequences = []
    images = []
    data = []

    for p in peptoids:
        peptoid_codes.append(p.code)
        peptoid_titles.append(p.title)
        peptoid_urls.append(url_for('routes.peptoid',code=p.code))
        # images.append(url_for('static',filename = p.code + '.png'))
        if len(p.sequence) < sequence_max:
            peptoid_sequences.append(p.sequence)
        else:
            l = [pos for pos, char in enumerate(p.sequence) if char == ',']
            peptoid_sequences.append(p.sequence[:l[2]] + " ...")
        if p.experiment == 'X-Ray Diffraction':
            data.append("https://www.doi.org/{}".format(p.struct_doi))
        else:
            data.append("https://www.doi.org/{}".format(p.pub_doi))

    return [peptoid_codes, peptoid_urls, peptoid_titles, peptoid_sequences, images, data]

# base route
@bp.route('/')
# home route displaying all petoids in reverse chron order using home.html template
@bp.route('/home')
def home():
    properties = get_home([p for p in Peptoid.query.order_by(Peptoid.release.desc()).all()])
    return render_template('home.html',
            title = 'Gallery',
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            data = properties[5]
        )

# route for all residues renders residues.html
@bp.route('/residues')
def residues():
    title = 'Residues'
    residues = [r for r in Residue.query.all()]
    return render_template('residues.html', title=title, residues=residues)
# search route renders the form using the search.html template and the SearchForm() from forms.py
# if the user has submitted the form they are redirected to the route for the serial choice with
# var = their search box input
@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('{cat} search for <{term}>'.format(cat=form.option.data.upper(), term=form.search.data),
        'success')
        var = form.search.data
        if '/' in var:
            var = var.replace('/', '$')
        return redirect(url_for('routes.'+form.option.data, var=var))
    return render_template('search.html',
    title='Search',
    form=form,
    info='Filter by any property from the choices below.',
    description='Peptoid Data Bank - Explore by property')

@bp.route('/peptoid/<code>')
def peptoid(code):
    # data passed to front end
    peptoid = Peptoid.query.filter_by(code=code).first_or_404()
    image = url_for('static', filename = peptoid.image)
    title = peptoid.title
    code = peptoid.code
    release = str(peptoid.release.month) + "/" + \
                  str(peptoid.release.day) + "/" + str(peptoid.release.year)
    experiment = peptoid.experiment
    if experiment == 'X-Ray Diffraction':
        data=peptoid.struct_doi
    else:
        data=peptoid.pub_doi

    # lists of objects also passed to front end
    authors = []
    residues = []

    for author in peptoid.peptoid_author:
        authors.append(author)

    for residue in peptoid.peptoid_residue:
        residues.append(residue)

    sequence = peptoid.sequence
    author_list = ", ".join([a.first_name + " " + a.last_name for a in authors])
    # rendering html template
    return render_template('peptoid.html',
        peptoid=peptoid,
        image=image,
        title=title,
        code=code,
        release=release,
        experiment=experiment,
        data=data,
        authors=authors,
        residues=residues,
        sequence=sequence,
        author_list=author_list
    )

# residue route for residue, name = var, returns home.html (gallery view)
@bp.route('/residue/<var>')
def residue(var):
    if var == 'null':
        return render_template('404.html')
    residue = Residue.query.filter((Residue.long_name == var) | (Residue.short_name == var)).first_or_404()
    properties = get_home([p for p in residue.peptoids])

    return render_template('home.html',
            title = 'Filtered by Residue: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            data = properties[5]
        )

# author route for author. If name entered has a space search by both words for first name and last name.
# if name entered is just one word check if it is an author's first name or last name
# returns home.html (gallery view)
@bp.route('/author/<var>')
def author(var):

    if "," in var:
        name_split = var.split(', ')
        last_name = name_split[0]
        first_name = name_split[1]
        author = Author.query.filter_by(first_name = first_name, last_name = last_name).first_or_404()
    else:
        author = Author.query.filter((Author.first_name == var) | (Author.last_name == var)).first_or_404()

    #generating peptoids according to sorted list date keys
    properties = get_home([p for p in author.peptoids])

    return render_template('home.html',
            title = 'Filtered by Author: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            data = properties[5]
        )

# experiment route for Peptoid.experimet = var, returns home.html (gallery view), if no peptoid found returns a 404
@bp.route('/experiment/<var>')
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
            data = properties[5]
        )

# doi route for Peptoid.doi = var, returns home.html (gallery view), if no peptoid found returns a 404
@bp.route('/doi/<var>')
def doi(var):
    var = var.replace('$','/')
    peptoids = Peptoid.query.order_by(Peptoid.release.desc()).filter((Peptoid.struct_doi == var) | (Peptoid.pub_doi == var)).all()
    properties = get_home([p for p in peptoids])

    if len(properties[0]) == 0:
        abort(404)

    return render_template('home.html',
            title = 'Filtered by DOI: ' + var,
            peptoid_codes = properties[0],
            peptoid_urls = properties[1],
            peptoid_titles = properties[2],
            peptoid_sequences = properties[3],
            images = properties[4],
            data = properties[5]
        )

# filtering according to topology
@bp.route('/top/<var>')
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
            data = properties[5]
        )

# about route returns about.html template
@bp.route('/about')
def about():
    return render_template('about.html', title="About us")

@bp.route('/api', methods=['GET', 'POST'])
def api():
    form = ApiRequest()
    if form.validate_on_submit():
        var = form.search.data
        if '/' in var:
            var = var.replace('/', '$')
        return redirect(url_for('api.get_peptoid', code=var))
    return render_template('api.html', title ="PeptoidDB API", form = form)
