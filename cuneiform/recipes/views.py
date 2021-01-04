#################
#### imports ####
#################

from flask import render_template

from . import recipes_blueprint


################
#### routes ####
################


@recipes_blueprint.route('/')
def index():
    return render_template('recipes/home.html.j2')
