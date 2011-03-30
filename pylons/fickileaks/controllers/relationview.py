import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators import jsonify
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController, render
from fickileaks.model import Relation, Person

from datetime import datetime
from random import random

log = logging.getLogger(__name__)

class RelationviewController(BaseController):

    def index(self):
        return render('relationview.mako')

    @jsonify
    def relations(self):
        relations = Relation.query.all()
        result = {}
        result['datetime'] = datetime.now().isoformat()
        result['relations'] = []

        for r in relations:
            relation = {}
            relation['created'] = r.created.isoformat()
            relation['creator'] = r.creator.email
            relation['type'] = r.type

            relation['participants'] = []
            for p in r.participants:
                participant = {}
                participant['names'] = [n.name for n in p.names]
                participant['urls'] = [u.url for u in p.urls]
                relation['participants'].append(participant)

            result['relations'].append(relation)

        print result
        return result

    @jsonify
    def infovis(self):
        query = Relation.query.all()
        nodeset = set([])
        
        # see if two different nodes share URLs
        def equivalent(node1, node2):
            if (node1 != node2):
                for url1 in node1.urls:
                    for url2 in node2.urls:
                        if (url1 == url2):
                            return True
            return False
        
        def merge(node1, node2):
            for name2 in node2.names:
                node1.addName(name2.name)
        
            for url2 in node2.urls:
                node1.addUrl(url2.url)
        
            for relation2 in node2.relations:
                pos2 = relation2.participants.index(node2)
                relation2.participants[pos2] = node1
            node1.relations.extend(node2.relations)
        
        # get nodes
        for relation in query:
            nodeset.update(relation.participants)
        
        for node in nodeset:
            print node
        
        # fold nodes
        while True:
            try:
                for node1 in nodeset:
                    for node2 in nodeset:
                        if equivalent(node1, node2):
                            merge(node1, node2)
                            nodeset.remove(node2)
                break
            except RuntimeError:  #Set changed size during iteration
                pass
        
        for node in nodeset:
            print node
        
        # fix-fold relations
        for node1 in nodeset:
            for node2 in nodeset:
                for relation1 in node1.relations:
                    for participant in relation1.participants:
                        if equivalent(participant, node2):
                            pos = relation1.participants.index(participant)
                            relation1.participants[pos] = node2
                try:
                    for relation2 in node2.relations:
                        for participant in relation2.participants:
                            if equivalent(participant, node1):
                                pos = relation2.participants.index(participant)
                                relation2.participants[pos] = node1
                except IntegrityError:
                    pass  # FIXME: I have no idea why this is happening sometimes
        
        # serialize structure so it can be jsonified
        nodelist = []
        
        for node in nodeset:
            serialnode = {
                'id': node.urls[0].url,
                'name': node.names[0].name,
                'data': {
                    # set hack used so both Names and URLs occur only once
                    'names': list(set([n.name for n in node.names])),
                    'urls': list(set([u.url for u in node.urls]))
                },
                'adjacencies': []
            }
        
            for relation in node.relations:
                for participant in relation.participants:
                    if not (node.urls[0] == participant.urls[0]):
        
                        adjacencynodeexists = False
                        for adjacency in serialnode['adjacencies']:
                            if (adjacency['nodeTo'] == participant.urls[0].url):
                                adjacencynodeexists = True
                                adjacencynode = adjacency

                            relationnodeexists = False
                            for relation0 in adjacency['data']['relations']:
                                if (relation0['type'] == relation.type):
                                    relationnodeexists = True
                                    relationnode = relation0

                            if not relationnodeexists:
                                relationnode = {
                                    'type': relation.type,
                                    'creators': [relation.creator.email],
                                }
                            
                                adjacencynode['data']['relations'].append(relationnode)
                            else:
                                if not (relation.creator.email in relationnode['creators']):
                                    relationnode['creators'].append(relation.creator.email)

                        if not adjacencynodeexists:
                            adjacencynode = {
                                'nodeTo': participant.urls[0].url,
                                'data': {
                                    'relations': []
                                }
                            }
                            serialnode['adjacencies'].append(adjacencynode)

            nodelist.append(serialnode)

        return nodelist


    @jsonify
    def infovis_dummy(self):
        """ dummy data for infovis, remove when infovis controller is mature """

        def sometime():
            offset = int(random()*1000)
            return datetime.fromordinal(offset + 733000).isoformat()

        def creators(list):
            result = {}
            for creator in list:
                result[creator] = sometime()
            return result

        nodes = [
            {
                'id': 'alice',
                'name': 'Alice Alisson',
                'data': {
                    'names': [],
                    'urls': []
                },
                'adjacencies': [
                    {
                        'nodeTo': 'bob',
                        'data': {
                            'relations': [
                                {
                                    'type': 'GROPE',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org',
                                            'charlie@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'KISS',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org',
                                            'charlie@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'FUCK',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'ORAL',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'ANAL',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'SM',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }
                            ]
                        }
                    }
                ]
            },
            {
                'id': 'bob',
                'name': 'Bob Bobsen',
                'data': {
                    'names': [],
                    'urls': []
                },
                'adjacencies': [
                    {
                        'nodeTo': 'charlie',
                        'data': {
                            'relations': [
                                {
                                    'type': 'GROPE',
                                    'creators': creators(
                                        [
                                            'alice@example.org',
                                            'bob@example.org',
                                            'charlie@example.org'
                                        ]
                                    )
                                },
                                {
                                    'type': 'KISS',
                                    'creators': creators(
                                        [
                                            'bob@example.org',
                                            'charlie@example.org'
                                        ]
                                    )
                                }
                            ]
                        }
                    }
                ]
            },
            {
                'id': 'charlie',
                'name': 'Charlie Charlesson',
                'data': {
                    'names': [],
                    'urls': []
                },
                'adjacencies': [
                    {
                        'nodeTo': 'alice',
                        'data': {
                            'relations': [
                                {
                                    'type': 'KISS',
                                    'creators': creators(
                                        [
                                            'charlie@example.org'
                                        ]
                                    )
                                }
                            ]
                        }
                    }, {
                        'nodeTo': 'eve',
                        'data': {
                            'relations': [
                                {
                                    'type': 'KISS',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }
                            ]
                        }
                    }, {
                        'nodeTo': 'zoe',
                        'data': {
                            'relations': [
                                {
                                    'type': 'GROPE',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }, {
                                    'type': 'KISS',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }, {
                                    'type': 'FUCK',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }, {
                                    'type': 'ORAL',
                                    'creators': creators(
                                        [
                                            'alice@example.org'
                                        ]
                                    )
                                }
                            ]
                        }
                    }
                ]
            }, {
                'id': 'dave',
                'name': 'Dave Davidsson',
                'data': {
                    'names': [],
                    'urls': []
                },
                'adjacencies': [
                    {
                        'nodeTo': 'alice',
                        'data': {
                            'relations': [
                                {
                                    'type': 'KISS',
                                    'creators': [
                                        {
                                            'creator': 'charlie@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }, {
                'id': 'eve',
                'name': 'Eve Evil',
                'data': {
                    'names': [],
                    'urls': []
                }
            }, {
                'id': 'zoe',
                'name': 'Zoe Zoolander',
                'data': {
                    'names': [],
                    'urls': []
                }
            }
        ]

        return nodes
