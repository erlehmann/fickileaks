from fickileaks.model import Session, Relation, Person
from elixir import metadata
from json import dumps

metadata.bind = "sqlite:///development.db"

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

print "=== FOLDED ==="

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
            

print "=== JSONIFIED ==="

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
            if not equivalent(node, participant):

                adjacencynodeexists = False
                relationnodeexists = False
                for adjacency in serialnode['adjacencies']:
                    if (adjacency['nodeTo'] == participant.urls[0].url):
                        adjacencynodeexists = True
                        adjacencynode = adjacency
                    for relation0 in adjacency['data']['relations']:
                        if (relation0['type'] == relation.type):
                            relationnodeexists = True
                            relationnode = relation0

                if not adjacencynodeexists:
                    adjacencynode = {
                        'nodeTo': participant.urls[0].url,
                        'data': {
                            'relations': []
                        }
                    }
                    serialnode['adjacencies'].append(adjacencynode)

                if not relationnodeexists:
                    relationnode = {
                        'type': relation.type,
                        'creators': [relation.creator.email],
                    }
                
                    adjacencynode['data']['relations'].append(relationnode)
                else:
                    if not (relation.creator.email in relationnode['creators']):
                        relationnode['creators'].append(relation.creator.email)
                    

    nodelist.append(serialnode)

print dumps(nodelist, sort_keys=True, indent=2)

#Session.close()
