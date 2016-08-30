from marshmallow import fields
from sqlalchemy import sql
from flask import request
from flask.ext.restful import Resource, abort
from flask.ext.login import current_user
from .forms import (
    PlanCreationForm,
    PlanUpdateForm,
)
from .models import Plan, Stage
from ..categories.models import Category, Unit
from ..utils.ma import serialize
from ..utils.restful import PaginatedResource, assert_ownership
from ..extensions import ma, db


# ================
# Helper Functions
# ================

def _get_category_or_404(name):
    category = Category.query\
        .filter(Category.name == name)\
        .first()
    if not category:
        abort(404)
    else:
        return category


def _get_load_unit_or_404(category, name):
    load_unit = Unit.query\
        .filter(Unit.category_id == category.id)\
        .filter(Unit.name == name)\
        .first()
    if not load_unit:
        abort(404)
    else:
        return load_unit


# =======
# Schemes
# =======

class PlanSchema(ma.ModelSchema):
    category = fields.Function(lambda obj: obj.category.name)
    load_unit = fields.Function(lambda obj: obj.load_unit.name)
    stages = fields.Function(lambda obj: serialize(obj.stages))

    class Meta:
        model = Plan


class StageSchema(ma.ModelSchema):
    class Meta:
        model = Stage


class PlanResource(Resource):
    def get(self, id):
        plan = Plan.query.get_or_404(id)
        return serialize(plan, PlanSchema)

    def delete(self, id):
        plan = Plan.query.get(id)
        assert_ownership(plan, current_user)

        db.session.delete(plan)
        db.session.commit()
        return '', 204

    def put(self, id):
        plan = Plan.query.get(id)
        assert_ownership(plan, current_user)

        form = PlanUpdateForm(**request.json)
        plan.category = _get_category_or_404(form.category.data)
        plan.load_unit = _get_load_unit_or_404(form.load_unit.data)
        plan.private = form.private.data
        plan.active = form.active.data
        plan.title = form.title.data
        plan.description = form.description.data
        plan.load_index = form.load_index.data
        plan.update(
            total_load=form.total_load.data,
            daily_load=form.daily_load.data,
            cron=form.cron.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
        )
        db.session.commit()
        return '', 200


class PlanListResource(PaginatedResource):
    model = Plan
    schema = PlanSchema

    def get_query(self):
        if current_user.is_anonymous:
            return Plan.query.filter(sql.false())
        else:
            return Plan.query\
                .filter(Plan.user_id == current_user.id)\
                .order_by(sql.desc(Plan.created_at))

    def post(self):
        form = PlanCreationForm(**request.json)
        form.validate()

        category = _get_category_or_404(form.category.data)
        load_unit = _get_load_unit_or_404(category, form.load_unit.data)
        plan = Plan.create(
            user=current_user,
            category=category,
            load_unit=load_unit,
            private=form.private.data,
            active=form.active.data,
            title=form.title.data,
            description=form.description.data,
            cron=form.cron.data,
            load_index=form.load_index.data,
            total_load=form.total_load.data,
            daily_load=form.daily_load.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data
        )
        stages = plan.stage(form.titles.data, form.loads.data)

        db.session.add(plan)
        db.session.add_all(stages)
        db.session.commit()
        return serialize(plan, PlanSchema)
