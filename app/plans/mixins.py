from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Column, Integer, ForeignKey


class OrderedTreeMixin(object):
    @declared_attr
    def parent_id(cls):
        return Column(Integer, ForeignKey(cls.id))

    @declared_attr
    def parent(cls):
        return relationship(
            cls, remote_side=[cls.id],
            collection_class=ordering_list('ordering'),
            order_by=cls.ordering, backref=backref(
                'children', cascade='all, delete-orphan',
                cascade_backrefs=False
            ),
        )

    @property
    def is_root(self):
        return not self.parent

    @property
    def root(self):
        return self if self.is_root else self.parent

    @property
    def tree(self):
        return [self, *[c.tree for c in self.children]]

    @property
    def tree_serialized(self):
        return [self.serialized, *[c.tree_serialized for c in self.children]]

    ordering = Column(Integer, nullable=False) if parent else None
