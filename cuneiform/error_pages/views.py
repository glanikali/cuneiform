#################
#### imports ####
#################
from flask import Blueprint, render_template

from . import errors_blueprint


@errors_blueprint.app_errorhandler(404)
def error_404(error):
    return render_template("error_pages/404.html.j2"), 404


@errors_blueprint.app_errorhandler(403)
def error_403(error):
    return render_template("error_pages/403.html.j2"), 403
