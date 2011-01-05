# -*- coding: utf-8 -*-

from elixir import *
from datetime import datetime


class User(Entity):
    email = Field(Unicode(), primary_key=True)  # FIXME: build custom email data type
    password = Field(Unicode())  # FIXME: use hashes instead of plaintext

    # every user has its own relationship “universe”
    persons = OneToMany('Person')  # a user has many beliefs about persons
    relations = OneToMany('Relation')  # a user has many beliefs about relations

    def __repr__(self):
        return '<User %s>' % (self.email)

class Person(Entity):
    # persons have many names and many URLs
    names = ManyToMany('Name')
    urls = OneToMany('Url')  # many URLs can denote one person

    relations = ManyToMany('Relation')

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __repr__(self):
        return '<Person %s, %s>' % (self.names, self.urls)

class Name(Entity):
    name = Field(Unicode(), primary_key=True)
    person = ManyToMany('Person')

    created = Field(DateTime, default=datetime.now)

    def __repr__(self):
        return '<Name %s>' % (self.name)

class Url(Entity):
    url = Field(Unicode(), primary_key=True)  # FIXME: build custom URL data type
    person = ManyToOne('Person')  # a person can have many URLs

    created = Field(DateTime, default=datetime.now)

    def __repr__(self):
        return '<Url %s>' % (self.url)

class Relation(Entity):
    participants = ManyToMany('Person')
    type = Field(Unicode())  # FIXME: build custom relation data type

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __repr__(self):
        return '<Relation %s: %s>' % (self.type, [n.names for n in self.participants])

