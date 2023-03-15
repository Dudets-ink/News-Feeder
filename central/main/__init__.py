from flask import Blueprint


bp = Blueprint('main', __name__)

from central.main import routes, forms