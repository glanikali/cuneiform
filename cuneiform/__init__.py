# __init__.py for cuneiform

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


# Register Blueprints
from cuneiform.items.views import items_blueprint
from cuneiform.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(items_blueprint, url_prefix='/items')
