from flask import Blueprint
from flask.ext.restful import Api
from .resources import PlanListResource, PlanResource

bp = Blueprint('plans_bp', __name__, template_folder='templates')
api = Api(bp)
api.add_resource(PlanListResource, '/plans')
api.add_resource(PlanResource, '/plans/<int:id>')
