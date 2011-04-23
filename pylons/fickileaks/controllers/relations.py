import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators import jsonify
from pylons.controllers.util import abort, redirect

from fickileaks.lib.base import BaseController, render
from fickileaks.model import Relation, Person

from sqlalchemy.exc import IntegrityError

from datetime import datetime

log = logging.getLogger(__name__)

class RelationsController(BaseController):

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
                node1.addName(name2.name, name2.creator)
        
            for url2 in node2.urls:
                node1.addUrl(url2.url, url2.creator)
        
            for relation2 in node2.relations:
                # node 1 is the person that should replace node 2 in the final result
                relation2.removeParticipant(node2)
                # FIXME: do not use persistence level, but create display objects
                node1.relations.append(relation2)
                # IMPORTANT: node1 gets automatically added to relation2 due to elixir
        
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

            # FIXME: this should work on one less level of intendation
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
                    'names': {},
                    'urls': {}
                },
                'adjacencies': []
            }

            # Who calls this node by what name?
            for n in node.names:
                if not n.name in serialnode['data']['names'].keys():
                    serialnode['data']['names'][n.name] = [n.creator.email]
                else:
                    serialnode['data']['names'][n.name].append(n.creator.email)
                # remove doubles
                serialnode['data']['names'][n.name] = list(set(serialnode['data']['names'][n.name]))

            # Who calls this node by what URL?
            for u in node.urls:
                if not u.url in serialnode['data']['urls'].keys():
                    serialnode['data']['urls'][u.url] = [u.creator.email]
                else:
                    serialnode['data']['urls'][u.url].append(u.creator.email)
                # remove doubles
                serialnode['data']['urls'][u.url] = list(set(serialnode['data']['urls'][u.url]))
            

            for relation in node.relations:
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
                                    'relations': [
                                        {
                                            'type': relation.type,
                                            'creators': [relation.creator.email],
                                        }
                                    ]
                                }
                            }
                            serialnode['adjacencies'].append(adjacencynode)

            nodelist.append(serialnode)

        return nodelist

class PersonContainer:
    "Data container for presentation purposes, filled by Person entity."

    def __init__(self, names, urls, relations):
        self.names = {}
        self.urls = {}
        self.relations = []

class RelationContainer:
    "Data container for presentation purposes, filled by Relation entity."

    def __init__(creator, participants, type):
        self.creator = None
        self.participants = []
        self.type = None
