import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators import jsonify
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController, render
from fickileaks.model import Relation, Person

from sqlalchemy.exc import IntegrityError

from datetime import datetime
from random import random

from hashlib import md5

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

        #print result
        return result

    @jsonify
    def infovis(self):
        query = Relation.query.all()
        
        nodeset = set([])
        nodecache = {}
        
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
                # node 1 is the person that should replace node 2 in the final result
                relation2.removeParticipant(node2)
                # FIXME: do not use persistence level, but create display objects
                node1.relations.append(relation2)
                # IMPORTANT: node1 gets automatically to relation2 due to elixir
        
                # remember that node2 has been replaced with node1
                nodecache[node2] = node1
        
        def fixrelations(nodeset):
            for node in nodeset:
                for relation in node.relations:
                    for participant in relation.participants:
                        # replace legacy nodes with upgraded variants
                        while participant in nodecache.keys() and participant in relation.participants:
                            # replace legacy node with upgraded node
                            relation.removeParticipant(participant)
                            relation.addParticipant(nodecache[participant])

        # get nodes
        for relation in query:
            nodeset.update(relation.participants)

        foldednodeset = set([])
        for node in nodeset:
            addToFoldedSet = True
            for foldednode in foldednodeset:
                if equivalent(node, foldednode):
                    merge(foldednode, node)
                    addToFoldedSet = False
            if addToFoldedSet:
                foldednodeset.add(node)

        nodeset = foldednodeset

        fixrelations(nodeset)

        # serialize structure so it can be jsonified
        nodelist = []
        
        for node in nodeset:
            serialnode = {
                'id': node._getSortedUrls()[0].url,
                'name': node._getSortedNames()[0].name,
                'data': {
                    # set hack used so both Names and URLs occur only once
                    'names': [n.name for n in node._getSortedNames()],
                    'urls': [u.url for u in node._getSortedUrls()]
                },
                'adjacencies': []
            }

            for relation in node.relations:
                #print node, relation
                for participant in relation.participants:
                    if not (node._getSortedUrls()[0] == participant._getSortedUrls()[0]):
        
                        adjacencynodeexists = False
                        
                        for adjacency in serialnode['adjacencies']:
                            if (adjacency['nodeTo'] == participant._getSortedUrls()[0].url):
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
                                'nodeTo': participant._getSortedUrls()[0].url,
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
