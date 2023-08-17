from flask import Blueprint

leagues = Blueprint('leagues', __name__)

from . import views, errors
