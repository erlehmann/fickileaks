from fickileaks.model import Session, Relation, Person
from elixir import metadata

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
        for relation2 in node2.relations:
            for participant in relation2.participants:
                if equivalent(participant, node1):
                    pos = relation2.participants.index(participant)
                    relation2.participants[pos] = node1

Session.close()
