from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

#initalizing Flask app and database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#initializing bootstrap app to use bootstrap css styles
bootstrap = Bootstrap(app)

from app import routes, models
