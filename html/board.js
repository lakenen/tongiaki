var HEX_SIZE = 60

var c = document.createElement('canvas')
c.width = window.innerWidth
c.height = window.innerHeight
document.documentElement.appendChild(c)
ctx = c.getContext('2d')

function hexPoint(i, x, y, size) {
    var angle = Math.PI / 180 * 60 * i;
    return [x + size * Math.cos(angle), y + size * Math.sin(angle)]
}
function drawHex(x, y, size) {
    ctx.beginPath()
    ctx.moveTo.apply(ctx, hexPoint(0, x, y, size))
    b = []
    for (var i = 1 ; i <= 6; ++i) {
        //ctx.lineTo.apply(ctx, hexPoint(i, x, y, size))
        var pt = hexPoint(i, x, y, size)
        var angle = (Math.PI / 180 * 60) * i + (Math.PI / 180 * 5)
        var prevpt = hexPoint(i-1, x, y, size)
        var cx1 = prevpt[0] + HEX_SIZE / 2.5 * Math.cos(angle)
        var cy1 = prevpt[1] + HEX_SIZE / 2.5 * Math.sin(angle)
        var cx2 = pt[0] - HEX_SIZE / 2.5 * Math.cos(angle)
        var cy2 = pt[1] - HEX_SIZE / 2.5 * Math.sin(angle)
        ctx.bezierCurveTo(
            cx1,
            cy1,
            cx2,
            cy2,
            pt[0], pt[1]);
        b.push([prevpt, [cx1, cy1]])
        b.push([pt, [cx2, cy2]])
    }
    ctx.stroke()

    // draw control points
    // b.forEach(function (pts) {
    //     ctx.beginPath()
    //     ctx.moveTo.apply(ctx, pts[0])
    //     ctx.lineTo.apply(ctx, pts[1])
    //     ctx.stroke()
    // })
}

function drawBoard(tiles) {
    var centerX = c.width / 2,
        centerY = c.height / 2
    tiles.forEach(function (tile) {
        var x = HEX_SIZE * tile.q * 1.5
        var y = HEX_SIZE * Math.sqrt(3) * (tile.r + tile.q / 2)
        drawHex(centerX + x, centerY + y, HEX_SIZE)
    })
}
