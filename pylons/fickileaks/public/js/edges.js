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
