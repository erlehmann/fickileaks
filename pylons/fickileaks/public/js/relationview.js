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
    'rainbow-relation': {
        'render': function() {
            // TODO
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
        type: 'line',
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

var json = [
    {
        'id': 'http://metamemory.de/',
        'name': 'artnoveau',
        'adjacencies': [
            'http://dieweltistgarnichtso.net',
            'http://tinkar.tumblr.com/',
            'http://moeffju.net',
            'http://mnt.mn',
            'http://twitter.com/darktwit',
            'http://plomlompom.de',
            'http://twitter.com/le_chatte_noire',
            'http://dridde.net',
            'http://irgendwasanderes.wordpress.com'
        ]
    }, {
        'id': 'http://dieweltistgarnichtso.net',
        'name': 'erlehmann',
        'adjacencies': [
            'http://tinkar.tumblr.com/',
            'http://twitter.com/le_chatte_noire',
            'http://irgendwasanderes.wordpress.com'
        ]
    }, {
        'id': 'http://tinkar.tumblr.com/',
        'name': 'Tinkar',
        'adjacencies': [
            'http://moeffju.net',
            'http://twitter.com/ledentist'
        ]
    }, {
        'id': 'http://moeffju.net',
        'name': 'moeffju',
        'adjacencies': [
            'http://julia-seeliger.de',
            'http://kathrinpassig.kulturidustrie.com',
            'http://twitter.com/darktwit'
        ]
    }, {
        'id': 'http://mnt.mn',
        'name': 'mntmn',
        'adjacencies': [
            'http://irgendwasanderes.wordpress.com'
        ]
    }, {
        'id': 'http://julia-seeliger.de',
        'name': 'zeitrafferin',
        'adjacencies': [
            'http://netzpolitik.org',
            'http://mspr0.de'
        ]
    }, {
        'id': 'http://twitter.com/darktwit',
        'name': 'darktwit',
        'adjacencies': [
            'http://kathrinpassig.kulturidustrie.com',
            'http://rampke.net',
            'http://adrianlang.de/'
        ]
    }, {
        'id': 'http://plomlompom.de',
        'name': 'plomlompom'
    }, {
        'id': 'http://kathrinpassig.kulturidustrie.com',
        'name': 'bilch'
    }, {
        'id': 'http://twitter.com/le_chatte_noire',
        'name': 'änne',
        'adjacencies': [
            'http://irgendwasanderes.wordpress.com'
        ]
    }, {
        'id': 'http://dridde.net',
        'name': 'dridde',
        'adjacencies': [
            'http://irgendwasanderes.wordpress.com'
        ]
    }, {
        'id': 'http://irgendwasanderes.wordpress.com',
        'name': 'irgendwieanders',
        'adjacencies': [
            'http://twitter.com/ledentist',
            'http://adrianlang.de/'
        ]
    }, {
        'id': 'http://rampke.net',
        'name': 'matthiasr'
    }, {
        'id': 'http://netzpolitik.org',
        'name': 'markusb'
    },
    {
        'id': 'http://mspr0.de',
        'name': 'mspro',
        'adjacencies': [
            'http://fotografiona.wordpress.com'
        ]
    }, {
        'id': 'http://fotografiona.wordpress.com',
        'name': 'fotografiona'
    }, {
        'id': 'http://twitter.com/ledentist',
        'name': 'ledentist'
    }, {
        'id': 'http://adrianlang.de/',
        'name': 'adrianlang'
        }
];

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

//g.loadJSON(json);

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
            //alert("Could not reach fickileaks JSON API.");
            console.log("Could not reach fickileaks JSON API.");
        }
    }
};
req.send(null);

