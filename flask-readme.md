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
## Add a residue

## Add an author

## Add a peptoid

# How to containerize application with Docker and deploy to the server
## Build an image

## Push to Docker Hub

## SSH into server

## Stop current Docker process and run new container