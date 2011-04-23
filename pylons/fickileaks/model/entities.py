# -*- coding: utf-8 -*-

from elixir import *
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound


class User(Entity):
    email = Field(Unicode())  # FIXME: email data type
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
    urls = ManyToMany('Url')  # FIXME: URL should be unique among Person objects of a single user

    relations = ManyToMany('Relation')

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __init__(self, creator, namestrings, urlstrings):
        self.creator = creator

        for namestring in namestrings:
            self.addName(namestring, creator)

        for urlstring in urlstrings:
            self.addUrl(urlstring, creator)

    def __repr__(self):
        return '<Person \n\t Names: %s, \n\t URLs: %s, \n\t Relations: %s>' % (self.names, self.urls, self.relations)

    def _getCountedNames(self):
        countednames = {}
        namelist = [n.name for n in self.names]
        for name in namelist:
            countednames[name] = namelist.count(name)
        print countednames

    def _getSortedNames(self):
        sortednames = self.names
        sortednames.sort()
        return sortednames

    def _getSortedUrls(self):
        sortedurls = self.urls
        sortedurls.sort()
        return sortedurls        

    def addName(self, namestring, creator):
        #try:
            # if Name object with corresponding creator and namestring is available, use it
        #    name = Name.query.filter_by(name=namestring).one()
        #except NoResultFound:
        name = Name(namestring, creator)

        self.names.append(name)

    def addUrl(self, urlstring, creator):
        #try:
            # if Url object with corresponding urlstring is available, use it
        #    url = Url.query.filter_by(url=urlstring).one()
        #except NoResultFound:
        url = Url(urlstring, creator)

        self.urls.append(url)


class Name(Entity):
    name = Field(Unicode())
    person = ManyToMany('Person')

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __init__(self, name, creator):
        self.name = name
        self.creator = creator

    def __repr__(self):
        return '<Name %s>' % (self.name)

    def __eq__(self, other):
        return (self.name == other.name)

    def __lt__(self, other):
        return (self.name < other.name)

    def __gt__(self, other):
        return (self.name > other.name)


class Url(Entity):
    url = Field(Unicode())  # FIXME: URL data type
    person = ManyToMany('Person')

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __init__(self, url, creator):
        self.url = url
        self.creator = creator

    def __repr__(self):
        return '<Url %s>' % (self.url)

    def __eq__(self, other):
        return (self.url == other.url)

    def __lt__(self, other):
        return (self.url < other.url)

    def __gt__(self, other):
        return (self.url > other.url)


class Relation(Entity):
    participants = ManyToMany('Person')
    type = Field(Enum('GROPE', 'KISS', 'FUCK', 'ORAL', 'ANAL', 'SM'))

    created = Field(DateTime, default=datetime.now)
    creator = ManyToOne('User')

    def __init__(self, creator, type, participants):
        self.creator = creator
        self.type = type

        for participant in participants:
            self.addParticipant(participant)

    def __repr__(self):
        names = [person.names for person in self.participants]
        return '\n\t\t<Relation %s: %s>' % (self.type, names)

    def addParticipant(self, person):
        self.participants.append(person)

    def removeParticipant(self, person):
        self.participants.remove(person)
