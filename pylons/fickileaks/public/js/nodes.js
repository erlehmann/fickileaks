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

$jit.RGraph.Plot.NodeTypes.implement({
    'sun': {
       'render': function(node, canvas) {
            var c = canvas.getCtx();
            var dim = node.getData('dim');
            var sradius = dim*1.5;
            var pos = node.getPos();  /* polar coordinates */
            var cpos = node.getPos().toComplex();  /* complex coordinates */

            c.lineWidth = node.getData('lineWidth') * 2;
            c.strokeStyle = '#edd400'; // Butter 2
            c.fillStyle = '#fce94f'; // Butter

            var angle = Math.PI / 9;
            c.save();
            c.translate(cpos.x, cpos.y);
            c.beginPath();
            c.moveTo(sradius, 0);
            for (var i = 0; i < 17; i++) {
                    c.rotate(angle);
                if (i % 2 == 0) {
                    c.lineTo((sradius / 0.35) * 0.2, 0);
                } else {
                    c.lineTo(sradius, 0);
                }
            }
            c.closePath();
            c.fill();
            c.stroke();
            c.restore();

            this.nodeHelper.circle.render('fill', cpos, dim, canvas);
            this.nodeHelper.circle.render('stroke', cpos, dim, canvas);
        },
        'contains': function(node, pos) {
            var dim = node.getData('dim');
            var npos = node.getPos().toComplex();

            return this.nodeHelper.circle.contains(npos, pos, dim*1.5);
        }
    }
});

