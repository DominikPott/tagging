"""Data structures and bindings to work with sql alchemy.

:mod:`tagging.model` this module holds datastrucktures which are placed in the project database.
They shouldn't be accessed directly only through the :mod:`tagging.control` functions.
"""

from sqlalchemy import Table, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from tagging.db_config import database

__author__ = 'Dominik'


Base = declarative_base()

association_table = Table('associations', Base.metadata,
                          Column('items.id', Integer, ForeignKey('items.id')),
                          Column('.id', Integer, ForeignKey('tags.id'))
                          )


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    hash = Column(String(40), nullable=False)
    tags = relationship('Tag',
                        secondary=association_table,
                        backref='items')


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


engine = create_engine(database)
Base.metadata.create_all(engine)
