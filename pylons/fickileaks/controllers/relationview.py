import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators import jsonify
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController, render
from fickileaks.model import Relation, Person

from datetime import datetime

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

        nodes = {}

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

        # fold nodes to merge all nodes who share URLs
        # the outer loop is necessary since merges on one pass can enable
        # further merges on subsequent passes.
                # helper function to insert node into nodes
                def insertNode(nodes,node):
                    urls = set(node['data']['urls'])
                    resultNode = node # if we don't find any matching URL below, it's just a new node
                    for url in urls:
                        # merge nodes, if one with this URL already exists and they are not the same object (i.e. already merged)
                        if url in nodes and node is not nodes[url]:
                            resultNode = nodes[url]     # merge with the first node we find sharing a URL

                            resultNode['data']['urls'] = list(set(urls).union(set(resultNode['data']['urls'])))

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
                            break # do not look for more matching URLs, this will be done below

                    for url in resultNode['data']['urls']:
                        urlInNodes = url in nodes
                        if not urlInNodes:
                            nodes[url] = resultNode
                        elif resultNode is not nodes[url]: # we need to merge resultNode and some other node already in nodes
                            temp = nodes[url]           # yank out the other node
                            nodes[url] = resultNode     # replace it with resultNode
                            insertNode(nodes,temp)       # and re-merge it in (repeat through recursion until all nodes sharing URLs merged)
                        else:
                            pass

                insertNode(nodes,node)

        def getNodeByUrl(nodes, url):
            return nodes[url]

        def nodeSet(nodes):
            d = {}
            r = []
            for node in nodes.values():
                id = node['data']['urls'][0]
                if id not in d:
                    d[id] = 1
                    r.append(node)
            return r

        # create names and ids
        for node in nodeSet(nodes):
            node['name'] = node['data']['names'][0]
            node['id'] = node['data']['urls'][0]

        # create edges
        for node in nodeSet(nodes):
            node['adjacencies'] = []

            for type in node['data']['relations']:
                for relation in node['data']['relations'][type]:
                    targetNode = getNodeByUrl(nodes, relation['url'])

                    adjacency = {
                        'nodeTo': targetNode['id'],
                        'data': {
                            'type': type,
                            'creators': [relation['creator']],
                            '$lineWidth': 1
                        }
                    }

                    node['adjacencies'].append(adjacency)

        # fold edges to merge all edges with same nodes and type
        for node in nodeSet(nodes):
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
                        resultAdjacency['data']['$lineWidth'] += adjacency['data']['$lineWidth']
                        resultAdjacency['data']['creators'].extend(adjacency['data']['creators'])

                        addAdjacency = False

                if (addAdjacency):
                    result.append(adjacency)

            node['adjacencies'] = result
            result = []


        # get rid of temporary edge data
        for node in nodeSet(nodes):
            del node['data']['relations']

        return list(nodeSet(nodes))
