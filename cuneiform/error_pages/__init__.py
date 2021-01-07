# handlers.py
"""
The core Blueprint handles the creation, modification, deletion,
and viewing of core func. for this application.
"""
from flask import Blueprint

errors_blueprint = Blueprint("errors", __name__, template_folder="templates")

from . import views