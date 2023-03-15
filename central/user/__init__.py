from flask import Blueprint


bp = Blueprint('user', __name__)

from central.user import routes, forms
