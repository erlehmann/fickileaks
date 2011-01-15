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

        # fold nodes
        for i in range(len(nodes)-1):  # FIXME: brute force is not efficient
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
                            'creators': [relation['creator']],
                            '$lineWidth': 1
                        }
                    }

                    node['adjacencies'].append(adjacency)

        # fold edges
        for node in nodes:
            result = []

            for adjacency in node['adjacencies']:
                addAdjacency = True

                for resultAdjacency in result:
                    nodeTo = adjacency['nodeTo']
                    resultNodeTo = resultAdjacency['nodeTo']

                    type = adjacency['data']['type']
                    resultType = resultAdjacency['data']['type']

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
        for node in nodes:
            del node['data']['relations']

        return nodes
