from flask import Blueprint

bp = Blueprint('routes', __name__, template_folder='templates')

from backend.routes.task import *
from backend.routes.user import *
