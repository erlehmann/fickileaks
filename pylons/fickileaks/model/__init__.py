"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from fickileaks.model.meta import Session, metadata

_Base = declarative_base()

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine


class Person(_Base):
    __tablename__ = "persons"

    id = sa.Column(sa.types.Integer, primary_key=True)
    urls = relation("Url", backref="person")
    names = relation("Name", backref="person")

class Url(_Base):
    __tablename__ = "urls"

    url = sa.Column(sa.types.String(255), primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))

class Name(_Base):
    __tablename__ = "names"

    id = sa.Column(sa.types.Integer, primary_key=True)
    name = sa.Column(sa.types.String(255))
    person_id = Column(Integer, ForeignKey('persons.id'))


participants = Table('participants', Base.metadata,
                    Column('relation_id', Integer, ForeignKey('relations.id')),
                    Column('person_id', Integer, ForeignKey('persons.id'))
            )

wishers = Table('wishers', Base.metadata,
                    Column('wishes_id', Integer, ForeignKey('wishes.id')),
                    Column('person_id', Integer, ForeignKey('persons.id'))
            )

class Relation(_Base):
    __tablename__ = "relations"

    id = sa.Column(sa.types.Integer, primary_key=True)
    type = sa.Column(sa.types.String(255))
    participants = relation("Person", secondary=participants)
    timestamp = sa.Column(sa.types.DateTime())
    user_id = Column(Integer, ForeignKey('users.id'))
    wishers = relation("Person", secondary=wishers)


class User(_Base):
    __tablename__ = "users"

    username = sa.Column(sa.types.String(255), primary_key=True)
    password = sa.Column(sa.types.String(255))
    email = sa.Column(sa.types.String(255))
    relations = relation("Relation", backref="user")
