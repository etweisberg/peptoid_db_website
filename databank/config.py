import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQL Alchemy configure from object
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4wsetdfghjv#loAu^%Liyftu'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
