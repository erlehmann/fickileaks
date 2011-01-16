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

        nodes = []

        # create nodes
        for r in query:
            for p in r.participants:
                names = [n.name for n in p.names]
                urls = [u.url for u in p.urls]

                # other participants in that relation
                others = []
                for q in r.participants:
                    if (p != q):
                        others.append(q)

                # urls of those participants
                relations = {}
                relations[r.type] = []
                for o in others:
                    for u in o.urls:
                        relations[r.type].append(
                            {
                                'url': u.url,
                                'creator': r.creator.email
                            }
                        )

                node = {
                    'data': {
                        'names': names,
                        'urls': urls,
                        'relations': relations
                    }
                }

                nodes.append(node)

        result = []

        # fold nodes to merge all nodes who share URLs
        # the outer loop is necessary since merges on one pass can enable
        # further merges on subsequent passes.
        for i in range(len(nodes)-1):
            for node in nodes:
                addNode = True  # assume node will be added

                for resultNode in result:
                    urls = set(node['data']['urls'])
                    resultUrls = set(resultNode['data']['urls'])

                    # merge nodes if two of them share the same URL
                    if (urls.intersection(resultUrls)):
                        resultNode['data']['urls'] = list(urls.union(resultUrls))

                        names = set(node['data']['names'])
                        resultNames = set(resultNode['data']['names'])
                        resultNode['data']['names'] = list(names.union(resultNames))

                        for type in node['data']['relations']:
                            relations = node['data']['relations'][type]

                            try:
                                resultRelations = resultNode['data']['relations'][type]
                            except KeyError:
                                # resultNode has no relations of that type yet
                                resultNode['data']['relations'][type] = relations
                                break

                            if (relations and resultRelations):  # both not None
                                resultNode['data']['relations'][type].extend(relations)

                        # do not add current node to result
                        addNode = False

                if (addNode):
                    result.append(node)

            nodes = result
            result = []

        # create names and ids
        for node in nodes:
            node['name'] = node['data']['names'][0]
            node['id'] = node['data']['urls'][0]

        def getNodeByUrl(nodes, url):
            for node in nodes:
                if url in node['data']['urls']:
                    return node

        # create edges
        for node in nodes:
            node['adjacencies'] = []

            for type in node['data']['relations']:
                for relation in node['data']['relations'][type]:
                    targetNode = getNodeByUrl(nodes, relation['url'])

                    adjacency = {
                        'nodeTo': targetNode['id'],
                        'data': {
                            'type': type,
                            'creators': [relation['creator']]
                        }
                    }

                    node['adjacencies'].append(adjacency)

        # fold edges to merge all edges with same nodes and type
        for node in nodes:
            result = []

            for adjacency in node['adjacencies']:
                addAdjacency = True

                for resultAdjacency in result:
                    nodeTo = adjacency['nodeTo']
                    resultNodeTo = resultAdjacency['nodeTo']

                    type = adjacency['data']['type']
                    resultType = resultAdjacency['data']['type']

                    # merge edges if type and target node id are the same
                    if ((nodeTo == resultNodeTo) and \
                        (type == resultType)):
                        resultAdjacency['data']['creators'].extend(adjacency['data']['creators'])

                        addAdjacency = False

                if (addAdjacency):
                    result.append(adjacency)

            node['adjacencies'] = result
            result = []


        # get rid of temporary edge data
        for node in nodes:
            del node['data']['relations']

        return nodes


    @jsonify
    def infovis_dummy(self):
        """ dummy data for infovis, remove when infovis controller is mature """

        def sometime():
            offset = int(random()*1000)
            return datetime.fromordinal(offset + 733000).isoformat()

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
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'charlie@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'KISS',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'charlie@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'FUCK',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'ORAL',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'ANAL',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'SM',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
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
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        },
                                        {
                                            'creator': 'charlie@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                },
                                {
                                    'type': 'KISS',
                                    'creators': [
                                        {
                                            'creator': 'bob@example.org',
                                            'timestamp': sometime()
                                        },
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
                                    'creators': [
                                        {
                                            'creator': 'charlie@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }
                            ]
                        }
                    }, {
                        'nodeTo': 'eve',
                        'data': {
                            'relations': [
                                {
                                    'type': 'KISS',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }
                            ]
                        }
                    }, {
                        'nodeTo': 'zoe',
                        'data': {
                            'relations': [
                                {
                                    'type': 'GROPE',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }, {
                                    'type': 'KISS',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }, {
                                    'type': 'FUCK',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
                                }, {
                                    'type': 'ORAL',
                                    'creators': [
                                        {
                                            'creator': 'alice@example.org',
                                            'timestamp': sometime()
                                        }
                                    ]
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
