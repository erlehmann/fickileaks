$jit.RGraph.Plot.NodeTypes.implement({
    'stroke-circle': {
        'render': function(node, canvas) {
            var c = canvas.getCtx()
            var dim = node.getData('dim');
            var pos = node.getPos().toComplex();
            var count = 0; node.eachAdjacency(function() { count++; });

            this.nodeHelper.circle.render('fill', { x: pos.x, y: pos.y }, dim, canvas);
            this.nodeHelper.circle.render('stroke', { x: pos.x, y: pos.y }, dim, canvas);

            /*
            // more than 5 connections are hard to grep visually
            if (count >= 5) {
                //c.fillStyle = '#888a85';
                c.fillStyle = '#babdb6';
                c.font = + 2*dim - 16 + 'px sans-serif';
                c.textAlign = 'center';
                c.textBaseline = 'middle';
                // pos.y hack to have beautiful vertically centered digits
                c.fillText(count, pos.x, pos.y + dim/8)
            }
            */
        },
        'contains': function(node, pos) {
            var dim = node.getData('dim');
            var npos = node.getPos().toComplex();
            return this.nodeHelper.circle.contains(npos, pos, dim);
        }
    }
});

function correctWidth(width) {
    return width*2;
}

$jit.RGraph.Plot.EdgeTypes.implement({
    'rainbow-line': {
        'render': function(edge, canvas) {
            var c = canvas.getCtx();
            var posFrom = edge.nodeFrom.getPos().toComplex();
            var posTo = edge.nodeTo.getPos().toComplex();

            var totalWidth = 0;
            for (i in edge.data.relations) {
                totalWidth += correctWidth(edge.data.relations[i].creators.length);
            }

            var paintedWidth = 0;

            for (i in edge.data.relations) {
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

                var level1 = edge.nodeTo.pos.rho/g.config.levelDistance
                var level2 = edge.nodeFrom.pos.rho/g.config.levelDistance

                var cp1 = posFrom.add(posTo.scale(1/Math.pow(level1+1, 2)));
                var cp2 = posFrom.scale(1/Math.pow(level2+1, 2)).add(posTo);

                var width = correctWidth(edge.data.relations[i].creators.length);
                var o = paintedWidth + width - totalWidth/2;
                paintedWidth += width;
                c.lineWidth = width;

                c.beginPath();
                c.moveTo(posFrom.x+o, posFrom.y)
                c.bezierCurveTo(cp1.x+o, cp1.y, cp2.x+o, cp2.y, posTo.x+o, posTo.y);
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
        zooming: 20
    },

    Node: {
        overridable: true,
        type: 'stroke-circle',
        CanvasStyles: {
            fillStyle: '#ffffff',
            strokeStyle: '#2e3436',
            lineWidth: 2
        }
    },

    Edge: {
        overridable: true,
        type: 'rainbow-line'
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
            }
        }
    },

    interpolation: 'polar',
    levelDistance: 200
});

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
req.open('GET', 'infovis_dummy', true);
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

