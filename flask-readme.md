# What is Flask?
According to the [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/), "Flask is a lightweight WSGI web application framework"

**Flask** is a useful web framework because of its ease of use and operating in Python. Not only, is Python used for the organization of the application and its routes, but also for the front end templating, as Flask supports the use of jinja, a web template engine for Python.

Further, Miguel Grinberg's [Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) serves as an effective way to get a functioning web application with an SQL database deployed quickly.
# Essential Application Structure
- Database
- Flask application (initialized in `__init__.py`, defined in `databank.py`, for which the FLASK_APP environment variable in `.flaskenv` is set equal to)
- App module
  - `routes.py` defines all of the web application routes (ex. '/peptoid', '/search', '/home', etc.)
  - `models.py` defines the schem for the database
  - `forms.py` defines the class for the SearchForm that is rendered in the /search route using flask-wtforms
  - `__init__.py` initalizes the Flask application, database, and all Flask extensions
- Additional files
    - Python script for populating database
    - Python script for clearing database
    - *(JSON object form of database)*
# How to add to the flask-sqlalchemy database
## For minor *adjustments*
- When in the databank directory run shell command `flask shell`
- In the Python environment run whatever commands may be required
  - There is no need to import the app, database, or any classes from the schema
  - Simply query the database and change the properties of objects
## Add a residue
1. Checkout a new branch from the repository using `git checkout -b <branch-name>`
2. Clear the database by running python db_clear.py in the base directory
3. Edit the database population script with the new residue and any new relationships that need to be added
     - Define the residue with the short name and specify all properties
     - Ex. `Nspe = Residue(nomenclature='Nspe',pep_type = 'alpha',CSD = 'BABTAA',SMILES='C1=CC=C(C=C1)C[N+](=CC2=CC=CC=C2)[O-]')`
     - Append this new object to the peptoid_author list for any peptoid object necessary
     - Ex. `pep1.peptoid_residue.append(Nspe)`
        - You can also identify the peptoid object by performing a query, such as `Peptoid.query.filter_by(code=<some_code>).first().peptoid_residue.append(Nspe)`. This may make maintaining the database simpler
4. Run the new database population script
5. Test the changes by running `flask run` in the databank directory
6. Push changes and create a pull request
7. Once merged (preferably reviewed) follow deployment protocol
## Add an author
1. Checkout a new branch from the repository using `git checkout -b <branch-name>`
2. Clear the database by running python db_clear.py in the base directory
3. Edit the database population script with the new author and add relationships
    - Define the author with first and last name
    - Ex. `EW = Author(first_name='Ethan',last_name='Weisberg')
    - Append this new object to the `peptoid_author` list for any peptoid objects necessary
    - Ex.`pep1.peptoid_author.append(EW)`
        - You can also identify the peptoid object by performing a query, such as `Peptoid.query.filter_by(code=<some_code>).first().peptoid_author.append(EW)`. This may make maintaining the database simpler
4. Run the new database population script
5. Test the changes by running `flask run` in the databank directory
6. Push changes and create a pull request
7. Once merged (preferably reviewed) follow deployment protocol
## Add a peptoid
1. Checkout a new branch from the repository using `git checkout -b <branch-name>`
2. Clear the database by running python db_clear.py in the base directory
3. Edit the database population script with the new peptoid and add relationships
    - Define the peptoid with:
      - code
      - image
      - title
      - release
      - experiment
      - doi
      - topology
    - Append authors to the `peptoid_author` list
    - Append residues to the `peptoid_residue` list
4. Run the new database population script
5. Test the changes by running `flask run` in the databank directory
6. Push changes and create a pull request
7. Once merged (preferably reviewed) follow deployment protocol
# How to containerize application with Docker and deploy to the server
## Build an image

## Push to Docker Hub

## SSH into server

## Stop current Docker process and run new container
