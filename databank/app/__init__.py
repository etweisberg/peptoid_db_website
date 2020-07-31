#importing essential modules for instantiating application and extensions
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_graphql import GraphQLView

#flask app factory pattern
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
limiter = Limiter(app, key_func=get_remote_address)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.routes import bp as routes_bp
app.register_blueprint(routes_bp)

#importing models from app module
from app import models
from .schema import schema

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))