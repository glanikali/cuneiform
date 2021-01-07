# __init__.py for cuneiform
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_injector import FlaskInjector
from injector import inject
from cuneiform.dependencies import configure

#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.

db = SQLAlchemy()
# bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"


# db = SQLAlchemy(app)
# Migrate(app,db)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# Register Blueprints (modularization for scaling, more semantic)


######################################
#### Application Factory Function ####
######################################


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    FlaskInjector(app=app, modules=[configure])
    return app


##########################
#### Helper Functions ####
##########################


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    # db.init_app(app)
    # db = SQLAlchemy(app)
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # Flask-Login configuration
    # from cuneiform.models import User


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from cuneiform.items.views import items_blueprint
    from cuneiform.users.views import users_blueprint
    from cuneiform.core import core_blueprint
    from cuneiform.error_pages import errors_blueprint

    app.register_blueprint(core_blueprint)
    app.register_blueprint(errors_blueprint)
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(items_blueprint, url_prefix="/items")
