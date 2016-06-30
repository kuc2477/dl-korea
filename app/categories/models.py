from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from ..extensions import db


class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name=None):
        self.name = name


class Unit(db.Model):
    @declared_attr
    def category_id(cls):
        return Column(Integer, ForeignKey(Category.id), nullable=False)

    @declared_attr
    def category(cls):
        return relationship(Category, backref='units')

    def __init__(self, category, name, integer=True):
        self.category = category
        self.name = name
        self.integer = integer

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    integer = Column(Boolean, nullable=False, default=True)
