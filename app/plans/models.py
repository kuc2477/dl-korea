from datetime import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from ..categories.models import Category, Unit
from ..users.models import User
from ..extensions import db


class Plan(db.Model):
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id), nullable=False)

    @declared_attr
    def user(cls):
        return relationship(User, backref='plans')

    @declared_attr
    def category_id(cls):
        return Column(Integer, ForeignKey(Category.id), nullable=False)

    @declared_attr
    def category(cls):
        return relationship(Category, 'plans')

    @declared_attr
    def load_unit_id(cls):
        return Column(Integer, ForeignKey(Unit.id), nullable=False)

    @declared_attr
    def load_unit(cls):
        return relationship(Unit, 'plans')

    def __init__(self, title=None, description=None,
                 private=False, active=True, load_index=0,
                 objective_load=None, objective_daily_load=None,
                 child_stage_ids=None):
        self.title = title
        self.description = description
        self.private = private
        self.active = active
        self.load_index = load_index
        self.objective_load = objective_load
        self.objective_daily_load = objective_daily_load
        self.child_stage_ids = child_stage_ids or []

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    private = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

    load_index = Column(Integer, default=0)
    objective_load = Column(Integer, nullable=False)
    objective_daily_load = Column(Integer, nullable=False)
    child_stage_ids = Column(postgresql.ARRAY(Integer))

    @property
    def child_stages(self):
        # TODO: NOT IMPLEMENTED YET
        return self.child_stage_ids

    cron = Column(String, nullable=False)
    start_at = Column(DateTime, default=datetime.now, nullable=False)
    end_at = Column(DateTime, default=None)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)


class Stage(db.Model):
    @declared_attr
    def plan_id(cls):
        return Column(Integer, ForeignKey(Plan.id), nullable=False)

    @declared_attr
    def plan(cls):
        return relationship(Plan, backref='descendent_stages')

    def __init__(self, plan=None, title=None, load=0):
        self.plan = plan
        self.title = title
        self.load = load

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    load = Column(Integer, nullable=False)

    @property
    def user(self):
        return self.plan.user

    @property
    def category(self):
        return self.plan.category

    @property
    def load_unit(self):
        return self.plan.load_unit
