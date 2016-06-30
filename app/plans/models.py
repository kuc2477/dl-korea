import itertools
from collections import deque
from datetime import datetime
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
from croniter import croniter
from ..categories.models import Category, Unit
from ..users.models import User
from ..extensions import db


def _count(iterator):
    counter = itertools.count()
    deque(itertools.izip(iterator, counter), maxlen=0)
    return next(counter)


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
        return relationship(Category, backref='plans')

    @declared_attr
    def load_unit_id(cls):
        return Column(Integer, ForeignKey(Unit.id), nullable=False)

    @declared_attr
    def load_unit(cls):
        return relationship(Unit, backref='plans')

    def __init__(self, user=None, category=None, load_unit=None,
                 title=None, description=None, cron=None,
                 private=False, active=True, load_index=0,
                 objective_load=None, objective_daily_load=None,
                 child_stage_ids=None):
        self.user = user
        self.category = category
        self.load_unit = load_unit
        self.title = title
        self.description = description
        self.private = private
        self.active = active
        self.load_index = load_index
        self.objective_load = objective_load
        self.objective_daily_load = objective_daily_load
        self.child_stage_ids = child_stage_ids or []

    @classmethod
    def _get_datetimes(cls, cron, start_at, end_at):
        iterator = croniter(cron, start_at)
        datetimes = itertools.takewhile(lambda d: d <= end_at, iterator)
        return datetimes

    @classmethod
    def _get_objective_load_from(
            cls, objective_daily_load, cron, start_at, end_at):
        datetimes = cls._get_datetimes(cron, start_at, end_at)
        return _count(datetimes) * objective_daily_load

    @classmethod
    def _get_objective_daily_load_from(
            cls, objective_load, cron, start_at, end_at):
        datetimes = cls._get_datetimes(cron, start_at, end_at)
        return objective_load / _count(datetimes)

    @classmethod
    def _get_end_from(cls, objective_load, objective_daily_load, cron):
        count = (int)(objective_load / objective_daily_load)
        iterator = croniter(cron, datetime.now())
        return next(itertools.islice(iterator, count))

    def stage(self, titles, loads):
        return [Stage(self, title, load) for title, load in zip(titles, loads)]

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    private = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

    load_index = Column(Integer, default=0)
    objective_load = Column(Integer, nullable=False)
    objective_daily_load = Column(Integer, nullable=False)

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
        return relationship(Plan, backref='stages')

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
