# Website for the peptoid data bank
<a href = "http://ethan-dev.com/" target="_blank">Development Domain</a>
## Running for development

- enter the databank directory using `cd databank`
- run the Flask application using `flask run`

## Required Python packages
- flask
- flask-migrate
- flask-sqlalchemy
- flask-wtf
- flask-bootstrap
- flask-limiter
- flask-graphql
- graphene
- graphene-sqlalchemy

For simplicity, use the following commands to install the required packages with pip
```shell
cd databank
pip install -r requirements.txt
```
----------------------------------------------------------------------------------------
# What is Flask?
According to the [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/), "Flask is a lightweight WSGI web application framework"

**Flask** is a useful web framework because of its ease of use and operating in Python. Not only, is Python used for the organization of the application and its routes, but also for the front end templating, as Flask supports the use of jinja, a web template engine for Python.

Further, Miguel Grinberg's [Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) serves as an effective way to get a functioning web application with an SQL database deployed quickly.
# Essential Application Structure
- Database
- Flask application (initialized in `__init__.py`, defined in `databank.py`, for which the FLASK_APP environment variable in `.flaskenv` is set equal to)
- App module
  - `app/routes/routes.py` defines all of the web application routes (ex. '/peptoid', '/search', '/home', etc.)
  - `app/models.py` defines the schema for the SQL database
  - `app/schema.py` defines the schema for the GraphQL API
  - `app/routes/forms.py` defines the class for the SearchForm that is rendered in the /search route using flask-wtforms
  - `app/routes/__init__.py` initalizes the Flask application, database, and all Flask extensions
  - `app/api/routes.py` defines the acceptable RESTful API Routes
  - `app/api/__init__.py` initializes the API
  - `app/api/errors.py` tells the API what payload to return in the event of errors
- Additional files
    - Python script for populating database `db_add.py`
    - Python script for clearing database `db_clear.py`
    - *(JSON object form of database)*
# How to add to the flask-sqlalchemy database
## Examine Database in the Flask Shell
- Use the flask shell to:
    1. Examine database contents
    2. Make minor tweaks *e.g. change spelling of author's name*
    3. Test queries
- When in the `databank` directory run command `flask shell`
- Use [queries](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records) to examine and/or tweak the databse
  - The database and Peptoid, Residue, and Author models should already be instantiated as `db`, `Peptoid`, `Residue`, and `Author` respectively.
  - Although these should be automatically imported **it is possible for this to not work**. This is easy to fix. Just run the following code in your flask shell:
    1. `from app import app, db`
    2. `from app.models import Peptoid, Author, Residue`
## Add a residue
Add a new object to `Residue.json` with the following format
```json
{
    "Short name": "<shortened name>",
    "Long name": "<IUPAC name>",
    "SMILES": "<SMILES string>",
    "monomer structure": "<Structural DOI of capped monomer>",
    "Backbone": "<Backbone type>"
}
```
All residues included in the sequences of the peptoids in `Structure.json` must be added to `Residue.json` in this manner or the database population script will throw an and the database will not populate properly.
## Add a structure
Add a new object to `Structure.json` with the following format:
```json
{
    "Authors": "<Last, First\n ... \nLast, First>",
    "Citation": "<Citation>",
    "Code": "<Peptoid Data Bank code>",
    "Experiment": "<Technique structure solved using>",
    "Publication doi": "<Publication DOI>",
    "Release": "<m/d/y>",
    "Sequence": "<Long Name\n ... \nLong Name>",
    "Structure doi": "<Structure DOI>",
    "Title": "<Title>",
    "Topology": "<C, A, or M>"
}
```
## Finalize changes
Run `python db_add.py` to add all of your changes to the database

Use `flask shell` or `flask run` to examine the changes you made.

# How to containerize application with Docker and deploy to the server