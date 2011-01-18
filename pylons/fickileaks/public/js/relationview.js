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

$jit.RGraph.Plot.NodeTypes.implement({
    'cloud': {
        'render': function(node, canvas) {
            var c = canvas.getCtx();
            c.lineWidth = node.getData('lineWidth') * 2;

            var dim = node.getData('dim');
            var pos = node.getPos().toComplex();

            var lowerLeftPos = {x: pos.x - dim/1.5, y: pos.y};
            var lowerRightPos = {x: pos.x + dim/1.5, y: pos.y};
            var upperLeftPos = {x: pos.x - dim/3, y: pos.y - dim/3 };
            var upperRightPos = {x: pos.x + dim/3, y: pos.y - dim/3 };

            this.nodeHelper.square.render('stroke', pos, dim/1.5, canvas);
            this.nodeHelper.circle.render('stroke', { x: lowerLeftPos.x, y: lowerLeftPos.y }, dim/1.5, canvas);
            this.nodeHelper.circle.render('stroke', { x: lowerRightPos.x, y: lowerRightPos.y }, dim/1.5, canvas);
            this.nodeHelper.circle.render('stroke', { x: upperLeftPos.x, y: upperLeftPos.y }, dim/1.25, canvas);
            this.nodeHelper.circle.render('stroke', { x: upperRightPos.x, y: upperRightPos.y }, dim/1.5, canvas);

            this.nodeHelper.square.render('fill', pos, dim/1.5, canvas);
            this.nodeHelper.circle.render('fill', { x: lowerLeftPos.x, y: lowerLeftPos.y }, dim/1.5, canvas);
            this.nodeHelper.circle.render('fill', { x: lowerRightPos.x, y: lowerRightPos.y }, dim/1.5, canvas);
            this.nodeHelper.circle.render('fill', { x: upperLeftPos.x, y: upperLeftPos.y }, dim/1.25, canvas);
            this.nodeHelper.circle.render('fill', { x: upperRightPos.x, y: upperRightPos.y }, dim/1.5, canvas);
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

                var width = correctWidth(edge.data.relations[i].creators.length);
                paintedWidth += width;
                c.lineWidth = width;

                var p = paintedWidth + width - totalWidth/2;

                var posFromNormal = new $jit.Complex(posFrom.x+posTo.y, posFrom.y-posTo.x);
                posFromNormal = posFromNormal.scale(1/posFromNormal.norm());
                posFromAdjusted = posFrom.add(posFromNormal.scale(p));

                var posToNormal = new $jit.Complex(posTo.x+posFrom.y, posTo.y-posFrom.x);
                posToNormal = posToNormal.scale(1/posToNormal.norm());
                posToAdjusted = posTo.add(posToNormal.scale(-p));

                var cp1 = posFromAdjusted.add(posToAdjusted.scale(1/Math.pow(level1+1, 2)));
                var cp2 = posFromAdjusted.scale(1/Math.pow(level2+1, 2)).add(posToAdjusted);

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
        zooming: 20
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

