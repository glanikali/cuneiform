# __init__.py for cuneiform

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'
# Register Blueprints
from cuneiform.items.views import items_blueprint
from cuneiform.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(items_blueprint, url_prefix='/items')
