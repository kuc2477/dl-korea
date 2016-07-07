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
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from croniter import croniter
from ..categories.models import Category, Unit
from ..users.models import User
from ..extensions import db
from ..exceptions import CronFormatError
from ..utils.datetime import coerce_datetime as _coerce


def _count(iterator):
    counter = itertools.count()
    deque(zip(iterator, counter), maxlen=0)
    return next(counter)


class Plan(db.Model):
    DEFAULT_CRON = '0 0 1 * *'

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey(User.id), nullable=False)

    @declared_attr
    def user(cls):
        return relationship(User, backref=backref(
            'plans', cascade='all, delete-orphan', cascade_backrefs=False
        ))

    @declared_attr
    def category_id(cls):
        return Column(Integer, ForeignKey(Category.id), nullable=False)

    @declared_attr
    def category(cls):
        return relationship(Category, backref=backref(
            'plans', cascade='all, delete-orphan', cascade_backrefs=False
        ))

    @declared_attr
    def load_unit_id(cls):
        return Column(Integer, ForeignKey(Unit.id), nullable=False)

    @declared_attr
    def load_unit(cls):
        return relationship(Unit, backref=backref(
            'plans', cascade='all, delete-orphan', cascade_backrefs=False
        ))

    def __init__(self, user=None, category=None, load_unit=None,
                 private=False, active=True,
                 title=None, description=None, cron=None,
                 load_index=0, total_load=None, daily_load=None,
                 start_at=None, end_at=None):
        self.category = category
        self.load_unit = load_unit

        self.private = private
        self.active = active

        self.user = user
        self.title = title
        self.description = description

        self.load_index = load_index
        self.total_load = total_load
        self.daily_load = daily_load

        self.cron = cron or self.DEFAULT_CRON
        self.start_at = _coerce(start_at) or datetime.now()
        self.end_at = _coerce(end_at)

    @classmethod
    def create(cls, **kwargs):
        daily_load = kwargs.pop('daily_load')
        total_load = kwargs.pop('total_load')
        cron = kwargs.pop('cron')
        start_at = _coerce(kwargs.pop('start_at'))
        end_at = _coerce(kwargs.pop('end_at'))

        if not total_load:
            assert(daily_load and cron and start_at and end_at), \
                '''Some of required keyword arguments are missing:
            daily_load: {}
            cron: {}
            start_at: {}
            end_at: {}
            '''.format(daily_load, cron, start_at, end_at)
            return cls._from_missing_total_load(
                daily_load=daily_load, cron=cron,
                start_at=start_at, end_at=end_at,
                **kwargs
            )
        elif not daily_load:
            assert(total_load and cron and start_at and end_at), \
                '''Some of required keyword arguments are missing:
            total_load: {}
            cron: {}
            start_at: {}
            end_at: {}
            '''.format(total_load, cron, start_at, end_at)
            return cls._from_missing_daily_load(
                total_load=total_load, cron=cron,
                start_at=start_at, end_at=end_at,
                **kwargs
            )
        else:
            assert(total_load and daily_load and cron and start_at), \
                '''Some of required keyword arguments are missing:
            total_load: {}
            daily_load: {}
            cron: {}
            start_at: {}
            '''.format(total_load, daily_load, cron, start_at)
            return cls._from_missing_end(
                total_load=total_load, daily_load=daily_load, cron=cron,
                start_at=start_at, **kwargs
            )

    @classmethod
    def _from_missing_total_load(
            cls, daily_load, cron, start_at, end_at, **kwargs):
        # retrieve total load from free variables
        total_load = cls.get_total_load_from(
            daily_load, cron, start_at, end_at
        )
        return cls(
            total_load=total_load, daily_load=daily_load,
            cron=cron, start_at=start_at, end_at=end_at,
            **kwargs
        )

    @classmethod
    def _from_missing_daily_load(
            cls, total_load, cron, start_at, end_at, **kwargs):
        # retrieve daily load from free variables
        daily_load = cls.get_daily_load_from(
            total_load, cron, start_at, end_at)
        return cls(
            total_load=total_load, daily_load=daily_load,
            cron=cron, start_at=start_at, end_at=end_at,
            **kwargs
        )

    @classmethod
    def _from_missing_end(
            cls, total_load, daily_load, cron, start_at=None, **kwargs):
        # retrieve end date from free variables
        start_at = start_at or datetime.now()
        end_at = cls.get_end_from(total_load, daily_load, cron, start_at)
        return cls(
            total_load=total_load, daily_load=daily_load,
            cron=cron, start_at=start_at, end_at=end_at,
            **kwargs
        )

    @classmethod
    def _get_datetimes(cls, cron, start_at, end_at):
        try:
            iterator = croniter(cron, start_at, ret_type=datetime)
        except (ValueError, AttributeError):
            raise CronFormatError(cron)
        else:
            datetimes = itertools.takewhile(lambda d: d <= end_at, iterator)
            return datetimes

    @classmethod
    def get_total_load_from(cls, daily_load, cron, start_at, end_at):
        datetimes = cls._get_datetimes(
            cron, _coerce(start_at), _coerce(end_at)
        )
        return _count(datetimes) * daily_load

    @classmethod
    def get_daily_load_from(cls, total_load, cron, start_at, end_at):
        datetimes = cls._get_datetimes(
            cron, _coerce(start_at), _coerce(end_at)
        )
        return total_load / _count(datetimes)

    @classmethod
    def get_end_from(cls, total_load, daily_load, cron, start_at=None):
        count = (int)(total_load / daily_load)
        try:
            iterator = croniter(
                cron, _coerce(start_at) or datetime.now(),
                ret_type=datetime
            )
        except (ValueError, AttributeError):
            raise CronFormatError(cron)
        else:
            return next(itertools.islice(iterator, count))

    def update(self, total_load, daily_load, cron, start_at, end_at,
               commit=False):
        if not total_load:
            total_load = self.get_total_load_from(
                daily_load, cron, start_at, end_at
            )
        elif not daily_load:
            daily_load = self.get_daily_load_from(
                total_load, cron, start_at, end_at
            )
        elif not end_at:
            end_at = self.get_end_from(
                total_load, daily_load, cron, start_at
            )

        self.total_load = total_load
        self.daily_load = daily_load
        self.cron = cron
        self.start_at = start_at
        self.end_at = end_at

        if commit:
            db.session.commit()

    def stage(self, titles, loads):
        return [Stage(self, title, load) for title, load in zip(titles, loads)]

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    private = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

    load_index = Column(Integer, default=0)
    total_load = Column(Integer, nullable=False)
    daily_load = Column(Integer, nullable=False)

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
        return relationship(Plan, backref=backref(
            'stages', cascade='all, delete-orphan'))

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
