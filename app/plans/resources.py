from flask import request
from flask.ext.restful import Resource
from .models import Plan, Stage
from .forms import PlanCreationForm
from ..extensions import db


class PlanResource(Resource):
    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return plan.serialized

    def delete(self, id):
        plan = Plan.query.get(id)
        db.session.delete(plan)
        db.session.commit()
        return '', 204

    def put(self, id):
        # TODO: NOT IMPLEMENTED YET
        pass


class PlanListResource(Resource):
    def get(self):
        # TODO: NOT IMPLEMENTED YET
        pass

    def post(self):
        form = PlanCreationForm(**request.json)
        form.validate()

        # TODO: NOT IMPLEMENTED YET
        pass
