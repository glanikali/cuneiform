#################
#### imports ####
#################

from flask import render_template

from . import core_blueprint


################
#### routes ####
################


@core_blueprint.route("/")
def index():
    return render_template("core/home.html.j2")
