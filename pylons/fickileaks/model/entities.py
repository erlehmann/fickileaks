# -*- coding: utf-8 -*-

from elixir import *
from datetime import datetime


class User(Entity):
    email = Field(Unicode(), primary_key=True)  # FIXME: email data type
    password = Field(Unicode())  # FIXME: use hashes instead of plaintext

    # every user has its own relationship “universe”
    persons = OneToMany('Person')  # user has many beliefs about persons
    relations = OneToMany('Relation')  # user has many beliefs about relations

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %s>' % (self.email)

    def addPerson(self, person):
        self.persons.append(person)

    def addRelation(self, relation):
        self.relations.append(relation)


class Person(Entity):
    # persons have many names and many URLs
    names = ManyToMany('Name')
    urls = OneToMany('Url')  # many URLs can denote one person

    relations = ManyToMany('Relation')

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __repr__(self):
        return '<Person %s, %s>' % (self.names, self.urls)

    def addName(self, name):
        self.names.append(name)

    def addUrl(self, url):
        self.urls.append(url)


class Name(Entity):
    name = Field(Unicode(), primary_key=True)
    person = ManyToMany('Person')

    created = Field(DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %s>' % (self.name)


class Url(Entity):
    url = Field(Unicode(), primary_key=True)  # FIXME: URL data type
    person = ManyToOne('Person')  # a person can have many URLs

    created = Field(DateTime, default=datetime.now)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Url %s>' % (self.url)


class Relation(Entity):
    participants = ManyToMany('Person')
    type = Field(Enum("FUCK", "KISS"))

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        names = [person.names for person in self.participants]
        return '<Relation %s: %s>' % (self.type, names)

    def addPerson(self, person):
        self.participants.append(person)
