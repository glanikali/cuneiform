"""
The core Blueprint handles the creation, modification, deletion,
and viewing of core func. for this application.
"""
from flask import Blueprint

core_blueprint = Blueprint("core", __name__, template_folder="templates")

from . import views
