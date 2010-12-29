from elixir import *
from datetime import datetime


class Person(Entity):
    names = ManyToMany('Name')
    urls = OneToMany('Url')
    relations = ManyToMany('Relation')
    wishes = OneToMany('Relation')

    def __repr__(self):
        return 'a' #'<Person %s, %s>' % (self.names, self.urls)

class Url(Entity):
    url = Field(Unicode(255))
    person = ManyToOne('Person')

    def __repr__(self):
        return '<Url %s>' % (self.url)

class Name(Entity):
    name = Field(Unicode(255))
    person = ManyToMany('Person')

    def __repr__(self):
        return '<Name %s>' % (self.name)


class Relation(Entity):
    created = Field(DateTime, default=datetime.now)
    participants = ManyToMany('Person')
    user = ManyToOne('User')
    type = Field(Unicode(255))
    wishers = ManyToOne('Person')

    def __repr__(self):
        return '<Relation %s %s>' % (self.type, self.participants)


class User(Entity):
    email = Field(Unicode(255))
    name = Field(Unicode(255))
    password = Field(Unicode(255))
    relations = OneToMany('Relation')

    def __repr__(self):
        return '<User %s %s>' % (self.name, self.email)
