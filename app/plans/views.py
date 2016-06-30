from flask import Blueprint
from flask.ext.restful import Api, abort

bp = Blueprint('plans_bp', __name__, template_folder='templates')
api = Api(bp)
