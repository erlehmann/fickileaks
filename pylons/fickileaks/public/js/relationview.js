var g = new $jit.RGraph({
    injectInto: 'graph',
    color: '#000000',

    Navigation: {
        enable: true,
        panning: true,
        zooming: 200
    },

    Node: {
        overridable: true,
        type: 'cloud',
        CanvasStyles: {
            fillStyle: '#ffffff',
            strokeStyle: '#2e3436'
        },
        lineWidth: 2
    },

    Edge: {
        overridable: true,
        type: 'rainbow-line',
        lineWidth: 2
    },

    Label: {
        overridable: true,
        type: 'Native',
        size: 16,
        color: '#000000',
        textBaseline: 'bottom'
    },

    Events: {
        enable: true,

        onMouseEnter: function(node) {
            g.canvas.getElement().style.cursor = 'pointer';
        },

        onMouseLeave: function() {
            g.canvas.getElement().style.cursor = '';
        },

        onClick: function(node) {
            if (node) {
                g.onClick(node.id);
                displayNodeInformation(node);
            }
        }
    },

    interpolation: 'polar',
    levelDistance: 200
});

function displayNodeInformation(node) {
    $('#nodename').text(node.name);
    displayItemList(node.data.names, '#namelist', '#namecount', false);
    displayItemList(node.data.urls, '#urllist', '#urlcount', true);
    displayRelationList(node, '#relationlist', '#relationcount');
}

function displayItemList(dict, listselector, countselector, createHyperlinks) {
    var itemList = $(listselector);
    itemList.empty();

    var countNode = $(countselector);
    var count = 0;

    $.each(dict, function(index, value) {
        var itemListEntry = document.createElement('li');

        var itemListDetails = document.createElement('details');
        var item = document.createElement('summary');
        if (createHyperlinks) {
            var hyperlink = document.createElement('a');
            hyperlink.href = hyperlink.textContent = index;
            item.appendChild(hyperlink);
        } else {
            item.textContent = index;
        }
        itemListDetails.appendChild(item);

        var creatorList = document.createElement('ul');
        itemListDetails.appendChild(creatorList);
        $(itemListEntry).appendWebshim(itemListDetails);

        $.each(value, function(index, value) {
            var creator = document.createElement('li');
            creator.textContent = value;
            creatorList.appendChild(creator);
        });

        itemList.append(itemListEntry);
        count++;
    });

    countNode.text(count);
}

function displayRelationList(node, listselector, countselector) {
    var relationList = $(listselector);
    relationList.empty();

    var countNode = $(countselector);
    var count = 0;

    node.eachAdjacency(function(adjacency) {

        var relationListEntry = document.createElement('li');

        var relationListDetails = document.createElement('details');
        var relation = document.createElement('summary');
        relation.textContent = adjacency.nodeTo.name;

        relationListDetails.appendChild(relation);

        var creatorList = document.createElement('ul');
        relationListDetails.appendChild(creatorList);
        $(relationListEntry).appendWebshim(relationListDetails);

        relationList.append(relationListEntry);
        count++;
    });

    countNode.text(count);
};

function centerFix(g) {
    var centerNodes = [];
    do {
        centerNodes = [];
        g.compute();
        g.graph.eachNode(function(node) {
            if (node.pos.rho == 0) {
                centerNodes.push(node);
            }
        });
        if (centerNodes.length > 1) {
            /* connect center nodes through invisible line */
            g.graph.addAdjacence(
                centerNodes[0],
                centerNodes[1],
                {
                    '$type': 'line',
                    '$alpha': 0
                }
            );
        }
    } while (centerNodes.length > 1);
}

function radiusFix(g) {
    // radius of circles should be proportional to number of adjacencies
    g.graph.eachNode(function(node) {
        var count = 0;
        node.eachAdjacency(function() {
            count++;
        });
        node.setData('dim', 16 + count*4);
    });
}

function getPleasureCenter(graph) {
    var centerNode;
    var centerNodeAdjacencies = 0;

    g.graph.eachNode(function(node) {
        var count = 0;
        node.eachAdjacency(function() {
            count++;
        });

        if (count > centerNodeAdjacencies) {
            centerNode = node;
            centerNodeAdjacencies = count;
        }
    });

    return centerNode;
}

function graphRender(json) {
    g.loadJSON(json);

    centerFix(g);
    var centerNode = getPleasureCenter(g);
    centerNode.setData('type', 'sun');

    radiusFix(g);
    g.compute();

    g.onClick(centerNode.id);
    displayNodeInformation(centerNode);
    g.refresh();
}

function graphUpdate() {
    /* build query */
    var query = {
        users: []
    }
    $('#querylist > li').each(function(index) {
        /* contents()[0] gives the text node containing the value */
        query['users'].push($(this).contents()[0].textContent);
    });
    $.get('/relations/infovis', query, function(json){
        graphRender(json['nodes']);
    });
}

var req = new XMLHttpRequest();
req.open('GET', 'infovis', true);
req.onreadystatechange = function (aEvt) {
    if (req.readyState == 4) {
        if(req.status == 200) {
            var json = JSON.parse(req.responseText);
            graphRender(json['nodes']);
        } else {
            alert("Could not reach fickileaks JSON API.");
        }
    }
};
req.send(null);

var inputField = $('input[type=email].autocomplete');
inputField.autocomplete({
    source: "/users/autocomplete"
    /*minLength: 2*/
    });

$('.add').click(function() {
    var value = inputField.val();

    $('#querylist > li').each(function(index) {
        /* empty input field if value has already been added */
        if ($(this).text() == value) {
            inputField.val('');
        }
    });

    /* add value if it is not empty */
    if (inputField.val() != '') {
        $('#querylist').append($('<li>' + value + '<button type="button" class="remove"><img src="/img/icons/list-remove.png" alt="Entfernen"></button></li>'));
        inputField.val('');

        $('.remove').click(function() {
            $(this.parentNode).remove();
            graphUpdate()
        });
        graphUpdate()
    }
});
