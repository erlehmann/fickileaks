# -*- coding: utf-8 -*-

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
    alice = User("alice@host.invalid", "123456")
    bob = User("bob@host.invalid", "123456")
    charlie = User("charlie@host.invalid", "123456")

    # User alice claims to be aware of the existence of these persons
    ap0 = Person(alice, ["Maine"], ["http://example.net/~maine"])
    ap1 = Person(alice, ["Alabama"], ["http://example.net/~alabama", "https://example.com/~alabama"])
    ap2 = Person(alice, ["Delaware"], ["http://example.com/~delaware"])
    ap3 = Person(alice, ["Georgia"], ["http://example.org/~georgia"])
    ap4 = Person(alice, ["Montana"], ["http://example.net/~montana"])
    ap5 = Person(alice, ["Indiana"], ["http://example.com/~indiana"])
    ap6 = Person(alice, [u"ˌkælɪˈfɔrnjə"], ["http://example.com/~california"])
    ap7 = Person(alice, [u"ˌpɛnsɪlˈveɪnjə"], ["http://example.net/~pennsylvania"])

    # User alice claims to be aware of the existence of these relationships
    Relation(alice, 'KISS', [ap1, ap2])
    Relation(alice, 'FUCK', [ap1, ap2])
    Relation(alice, 'KISS', [ap0, ap3])
    Relation(alice, 'KISS', [ap3, ap4])
    Relation(alice, 'FUCK', [ap3, ap4])
    Relation(alice, 'KISS', [ap0, ap5])
    Relation(alice, 'KISS', [ap2, ap3])
    Relation(alice, 'KISS', [ap3, ap5])
    Relation(alice, 'GROPE', [ap3, ap5])
    Relation(alice, 'KISS', [ap3, ap6])
    Relation(alice, 'FUCK', [ap5, ap6])
    Relation(alice, 'GROPE', [ap0, ap7])
    Relation(alice, 'KISS', [ap0, ap7])
    Relation(alice, 'FUCK', [ap0, ap7])
    Relation(alice, 'ORAL', [ap0, ap7])

    # User bob claims to be aware of the existence of these persons
    bp0 = Person(bob, ["Alabama"], ["http://example.net/~alabama"])
    bp1 = Person(bob, ["Delaware"], ["http://example.com/~delaware"])
    bp2 = Person(bob, ["Indiana"], ["http://example.com/~indiana"])
    bp3 = Person(bob, [u"ˌkælɪˈfɔrnjə"], ["http://example.com/~california"])

    # User bob claims to be aware of the existence of these relationships
    Relation(bob, 'KISS', [bp0, bp1])
    Relation(bob, 'FUCK', [bp0, bp1])
    Relation(bob, 'GROPE', [bp2, bp3])

    # User charlie claims to be aware of the existence of these persons
    cp0 = Person(charlie, ["Maine"], ["http://example.net/~maine"])
    cp1 = Person(charlie, ["Georgia", u"ˈdʒɔrdʒə"], ["http://example.org/~georgia", "http://example.net/memory"])

    # User charlie claims to be aware of the existence of these relationships

    Relation(charlie, 'GROPE', [cp0, cp1])
    Relation(charlie, 'KISS', [cp0, cp1])
    Relation(charlie, 'FUCK', [cp0, cp1])
    Relation(charlie, 'ORAL', [cp0, cp1])
    Relation(charlie, 'ANAL', [cp0, cp1])
    Relation(charlie, 'SM', [cp0, cp1])

    Session.commit()
