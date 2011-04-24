function cloudRender(object, mode, pos, dim, canvas) {
    var lowerLeftPos = {x: pos.x - dim/1.5, y: pos.y};
    var lowerRightPos = {x: pos.x + dim/1.5, y: pos.y};
    var upperLeftPos = {x: pos.x - dim/3, y: pos.y - dim/3 };
    var upperRightPos = {x: pos.x + dim/3, y: pos.y - dim/3 };

    object.nodeHelper.square.render(mode, pos, dim/1.5, canvas);
    object.nodeHelper.circle.render(mode, { x: lowerLeftPos.x, y: lowerLeftPos.y }, dim/1.5, canvas);
    object.nodeHelper.circle.render(mode, { x: lowerRightPos.x, y: lowerRightPos.y }, dim/1.5, canvas);
    object.nodeHelper.circle.render(mode, { x: upperLeftPos.x, y: upperLeftPos.y }, dim/1.25, canvas);
    object.nodeHelper.circle.render(mode, { x: upperRightPos.x, y: upperRightPos.y }, dim/1.5, canvas);
}

$jit.RGraph.Plot.NodeTypes.implement({
    'cloud': {
        'render': function(node, canvas) {
            var c = canvas.getCtx();
            var dim = node.getData('dim');
            var pos = node.getPos().toComplex();

            c.lineWidth = node.getData('lineWidth') * 2;
            cloudRender(this, 'stroke', pos, dim, canvas);

            cloudRender(this, 'fill', pos, dim, canvas);
        },
        'contains': function(node, pos) {
            var dim = node.getData('dim');
            var npos = node.getPos().toComplex();

            var lowerLeftPos = {x: npos.x - dim/1.5, y: npos.y};
            var lowerRightPos = {x: npos.x + dim/1.5, y: npos.y};
            var upperLeftPos = {x: npos.x - dim/3, y: npos.y - dim/3 };
            var upperRightPos = {x: npos.x + dim/3, y: npos.y - dim/3 };

            return this.nodeHelper.square.contains(npos, pos, dim/1.5)
                || this.nodeHelper.circle.contains(lowerLeftPos, pos, dim/1.5)
                || this.nodeHelper.circle.contains(lowerRightPos, pos, dim/1.5)
                || this.nodeHelper.circle.contains(upperLeftPos, pos, dim/1.25)
                || this.nodeHelper.circle.contains(upperRightPos, pos, dim/1.5);
        }
    }
});

function correctWidth(width) {
    return width;
}

$jit.RGraph.Plot.EdgeTypes.implement({
    'rainbow-line': {
        'render': function(edge, canvas) {
            var c = canvas.getCtx();
            var posFrom = edge.nodeFrom.getPos().toComplex();
            var posTo = edge.nodeTo.getPos().toComplex();

            var totalWidth = 0;
            var i = edge.data.relations.length;
            while (i--) {
                var count = 0; for (j in edge.data.relations[i].creators) { count++; }
                totalWidth += correctWidth(count);
            }

            var paintedWidth = 0;

            // TODO: sort relations so colors are always right order
            var i = edge.data.relations.length;
            while (i--) {
                switch (edge.data.relations[i].type) {
                    case "GROPE":
                        c.strokeStyle = '#ef2929'; // Scarlet Red
                        break;

                    case "KISS":
                        c.strokeStyle = '#fcaf3e'; // Orange
                        break;

                    case "FUCK":
                        c.strokeStyle = '#fce94f'; // Butter
                        break;

                    case "ORAL":
                        c.strokeStyle = '#8ae234'; // Chameleon
                        break;

                    case "ANAL":
                        c.strokeStyle = '#729fcf'; // Sky Blue
                        break;

                    case "SM":
                        c.strokeStyle = '#ad7fa8'; // Plum
                        break;
                }

                var width = correctWidth(count);
                paintedWidth += width;
                c.lineWidth = width + 1; // FIXME: Why is this necessary?

                var p = paintedWidth - totalWidth/2;

                var line = new $jit.Complex(posTo.y-posFrom.y, -posTo.x+posFrom.x);
                var lineNormal = line.scale(1/line.norm());

                var posFromAdjusted = posFrom.add(lineNormal.scale(p));
                var posToAdjusted = posTo.add(lineNormal.scale(p));

                var level1 = edge.nodeTo.pos.rho/g.config.levelDistance;
                var level2 = edge.nodeFrom.pos.rho/g.config.levelDistance;

                // control points for individual rainbow strands
                cp1 = posFromAdjusted.add(posToAdjusted.scale(1/Math.pow(level1+1, 2)));
                cp2 = posFromAdjusted.scale(1/Math.pow(level2+1, 2)).add(posToAdjusted);

                // crude control point fix, get rid of those near to end points
                var dimFrom = edge.nodeTo.getData('dim');
                if (this.nodeHelper.circle.contains(posFromAdjusted, cp1, dimFrom)) {
                    cp1 = posFromAdjusted;
                }

                var dimTo = edge.nodeTo.getData('dim');
                if (this.nodeHelper.circle.contains(posToAdjusted, cp2, dimTo)) {
                    cp2 = posToAdjusted;
                }

                c.beginPath();
                c.moveTo(posFromAdjusted.x, posFromAdjusted.y)
                c.bezierCurveTo(cp1.x, cp1.y, cp2.x, cp2.y, posToAdjusted.x, posToAdjusted.y);
                c.stroke()
            }
        }
    }
});

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

    Tips: {
        enable: true,
        onShow: function(tip, node) {
            var data = node.data;

            html = '<h1>Namen</h1>';
            html += '<ul>'
            $.each(data.names, function(index, value) {
                html += '<li>' + '<b>' + index + '</b>: ' + value + '</li>';
                });
            html += '</ul>';
            html += '<h1>URLs</h1>';
            html += '<ul>'
            $.each(data.urls, function(index, value) {
                html += '<li><b><a href="' + index + '">' + index + '</a></b>: ' + value + '</li>';
                });
            html += '</ul>';
            tip.innerHTML = html;
        }
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

                displayItemList(node.data.names, '#namelist', false)
                displayItemList(node.data.urls, '#urllist', true)
            }
        },
    },

    interpolation: 'polar',
    levelDistance: 200
});

function displayItemList(dict, selector, createHyperlinks) {
    itemList = $(selector);
    itemList.empty();

    $.each(dict, function(index, value) {
        var itemListEntry = document.createElement('li');

        var item = document.createElement('b');
        if (createHyperlinks) {
            var hyperlink = document.createElement('a');
            hyperlink.href = hyperlink.textContent = index;
            item.appendChild(hyperlink);
        } else {
            item.textContent = index;
        }
        itemListEntry.appendChild(item);

        var creatorList = document.createElement('ul');
        itemListEntry.appendChild(creatorList);

        $.each(value, function(index, value) {
            var creator = document.createElement('li');
            creator.textContent = value;
            creatorList.appendChild(creator);            
        });

        itemList.append(itemListEntry);
    });
}

function radiusFix(g) {
    // radius of circles should be proportional to number of adjacencies
    g.graph.eachNode(
        function(node) {
            var count = 0;
                node.eachAdjacency(
                    function() {
                    count++;
                }
            );
            node.setData('dim', 16 + count*4);
        }
    );
}

var req = new XMLHttpRequest();
req.open('GET', 'infovis', true);
req.onreadystatechange = function (aEvt) {
    if (req.readyState == 4) {
        if(req.status == 200) {
            var json = JSON.parse(req.responseText);
            g.loadJSON(json);

            radiusFix(g)
            g.refresh()
        } else {
            alert("Could not reach fickileaks JSON API.");
        }
    }
};
req.send(null);

