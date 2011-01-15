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

$jit.RGraph.Plot.EdgeTypes.implement({
    'stroke-line': {
        'render': function(edge, canvas) {
            var c = canvas.getCtx();
            var posFrom = edge.nodeFrom.getPos().toComplex();
            var posTo = edge.nodeTo.getPos().toComplex();

            if (edge.data.type === 'FUCK') {
                c.strokeStyle = '#ef2929';
            }

            if (edge.data.type === 'KISS') {
                c.strokeStyle = '#729fcf';
            }

            var cp1 = posFrom.add(posTo.scale(0.5));
            var cp2 = posFrom.scale(0.5).add(posTo);

            c.beginPath();
            c.moveTo(posFrom.x, posFrom.y)
            c.bezierCurveTo(cp1.x, cp1.y, cp2.x, cp2.y, posTo.x, posTo.y);
            c.stroke()
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
        type: 'stroke-line',
        color: '#fcaf3e'
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

