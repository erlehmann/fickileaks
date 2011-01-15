"""Setup the fickileaks application"""
import logging

import pylons.test

from fickileaks.config.environment import load_environment
from fickileaks.model import Session, metadata

from fickileaks.model.entities import User, Person, Relation

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup fickileaks here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    metadata.create_all(bind=Session.bind)

    # Populate the database on 'paster setup-app'

    # Users
    alice = User("alice@example.org", "123456")
    bob = User("bob@example.org", "654321")
    charlie = User("charlie@example.org", "password")

    # User alice claims to be aware of the existence of these persons
    ap0 = Person(alice, ["Alice Alison"], ["http://example.com/alice72"])
    ap1 = Person(alice, ["Bob Bobson"], ["http://example.com/bob81"])
    ap2 = Person(alice, ["Charlie Charleson"], ["http://example.com/charlie90"])
    ap3 = Person(alice, ["Dave Davidson"], ["http://example.com/davedavedave"])

    # User alice claims to be aware of the existence of these relationships
    ar0 = Relation(alice, 'FUCK', [ap0, ap1])
    ar1 = Relation(alice, 'FUCK', [ap0, ap2])
    ar2 = Relation(alice, 'KISS', [ap0, ap3])

    # User bob claims to be aware of the existence of these persons
    bp0 = Person(bob, ["Alise"], ["http://example.net/~alice"])
    bp1 = Person(bob, ["Bobby"], ["http://example.com/bob81"])
    bp2 = Person(bob, ["Dave the Face"], ["http://example.com/davedavedave"])

    # User bob claims to be aware of the existence of these relationships
    br0 = Relation(bob, 'FUCK', [bp0, bp1])
    br1 = Relation(bob, 'FUCK', [bp0, bp2])
    br2 = Relation(bob, 'KISS', [bp1, bp2])

    # User charlie claims to be aware of the existence of these persons
    cp0 = Person(charlie, ["Alice"], ["http://example.com/alice72", "http://example.net/~alice"])
    cp1 = Person(charlie, ["Bob from Berlin"], ["http://example.com/bob81"])
    cp2 = Person(charlie, ["Davey"], ["http://example.com/davedavedave"])
    cp3 = Person(charlie, ["Emily", "Em"], ["http://emily.example.net"])

    # User charlie claims to be aware of the existence of these relationships
    cr0 = Relation(charlie, 'KISS', [cp0, cp1])
    cr1 = Relation(charlie, 'KISS', [cp0, cp2])
    cr2 = Relation(charlie, 'KISS', [cp1, cp3])
    cr3 = Relation(charlie, 'FUCK', [cp2, cp3])

    Session.commit()
