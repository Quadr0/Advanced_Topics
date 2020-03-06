var id, posX, posY, vx, vy;

var maxBlockY, minPaddleY = 500;

var bricks;

const NumRects = 20;
const RecWidth = 100, RecLength = 35;

function setup() {
bricks = getRects();

    resetRects();

    resetBall();
}

function resetGame() {
    if(id != null) {
        clearInterval(id);
        id = null;
    }

    setup();
}

function resetBall() {
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));
    console.log(radius);

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);

    posX = radius + Math.random() * (widthBBox - radius*2);
    posY = 300 + radius + Math.random() * (100 - radius);
    
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);

    vx = Math.random() > .5 ? -1 : 1;
    vy = 1;
}

function resetRects() {
    var origX = 50.5, origY = 50;

    var curX = origX, curY = origY;

    var bbox = document.getElementById("container").getBoundingClientRect();
    var bboxWidth = parseFloat(bbox.width);
    for(var i = 0; i < NumRects; i++) {

        if(curX + RecWidth + 15 >= bboxWidth) {
            curX = origX;
            curY += RecLength + 15;
        }

        curRect = rects[i];

        curRect.setAttribute("x", curX);
        curRect.setAttribute("y", curY);
        curRect.setAttribute("width", RecWidth);
        curRect.setAttribute("height", RecLength);
        curRect.setAttribute("fill", getRandomColor());
        curRect.setAttribute("stroke", "black");
        curRect.setAttribute("stroke-width", .5);


        curX += RecWidth + 33.33;
    }
    biggestBlockY = curY + RecLength + 20;
}

function mousePosition(e) {
    var xMouse = parseFloat(e.clientX);
    
    var paddle = document.getElementById("paddle");
    var widthPaddle = parseFloat(paddle.getAttribute("width"));

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);
    var rightBBox = parseFloat(bbox.right);
    var leftBBox = parseFloat(bbox.left);

    if (xMouse + widthPaddle/2 >= rightBBox) {
        paddle.setAttribute("x", widthBBox - widthPaddle);
    }
    else if (xMouse - widthPaddle/2 <= leftBBox) {
        paddle.setAttribute("x", 0);
    }
    else {
        paddle.setAttribute("x", xMouse - leftBBox - widthPaddle/2);
    }
}

function startGame() {
    if (id == null) {
        id = setInterval(gameActions, 5);
    }
}

function gameActions() {
    var ball = document.getElementById("ball"); 
    
    wallCollisions();
    paddleCollision();
    brickCollisions();

    posX += vx;
    posY += vy;
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);

    if(bricks.length == 0) {
        alert("You have won the game");
        clearInterval(id);
        id = null;
    }
}

function paddleCollision() {
    
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));

    if(posY <= minPaddleY) return;

    var paddle = document.getElementById("paddle");
    var xPaddle = parseFloat(paddle.getAttribute("x"));
    var yPaddle = parseFloat(paddle.getAttribute("y"));
    var widthPaddle = parseFloat(paddle.getAttribute("width"));
    var heightPaddle = parseFloat(paddle.getAttribute("height"));

    //console.log(xBall)

    // Check if ball bounces of top of paddle.
    // TODO: should this not be yPadde + heightPaddle - .5
    if(posX >= xPaddle && posX <= xPaddle + widthPaddle && inRange(posY + radius, yPaddle + heightPaddle - 1, yPaddle + heightPaddle + 1)) {
        vy = -1;
    }

    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX - radius, xPaddle + widthPaddle - 1, xPaddle + widthPaddle + 1)) {
        vy = -1;
        vx = 1;
    }

    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX + radius, xPaddle - 1, xPaddle + 1)) {
        vy = -1;
        vx = -1;
    }

}

function brickCollisions() {
    
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));
    //console.log(bricks.length);

    if(posY >= maxBlockY) return;

    for(var i = bricks.length-1; i >= 0; i--) {

        var curBrick = bricks[i];
        var xBlock = parseFloat(curBrick.getAttribute("x"));
        var yBlock = parseFloat(curBrick.getAttribute("y"));
        var widthBlock = parseFloat(curBrick.getAttribute("width"));
        var heightBlock = parseFloat(curBrick.getAttribute("height"));

        // bottom of brick
        if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY - radius, yBlock + heightBlock - 1, yBlock + heightBlock + 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            //console.log("asdf")
            return;
        }

        // top of brick
        else if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY + radius, yBlock - 1, yBlock + 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            //console.log("asdf")
            return;
        }

        //right of brick
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX - radius, xBlock + widthBlock - 1, xBlock + widthBlock + 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            //console.log("asdf")
            return;
        }

        //left of brick
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX + radius, xBlock - 1, xBlock + 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            //console.log("asdf")
            return;
        }
        
    }
}

function wallCollisions() {
    var ball = document.getElementById("ball"); 
    var radius = parseFloat(ball.getAttribute("r")); 
    var svgWidth = parseFloat(document.getElementById("container").getAttribute("width"));
    var svgHeight = parseFloat(document.getElementById("container").getAttribute("height"))

    if (posX + radius  >= svgWidth) { 
        vx = -1;
        //c.setAttribute("fill", getRandomColor());
  
    }
    else if (radius >= posX){
        vx = 1;
        //c.setAttribute("fill", getRandomColor());
    }

    // If you hit the bottom wall, you lose the game. 
    if (posY + radius  >= svgHeight) { 
        vy = -1;

        clearInterval(id); 
        alert("You lost the game");
    }
    else if (radius >= posY){
        vy = 1;
        //c.setAttribute("fill", getRandomColor());
    }
}

function inRange(val, min, max) {
    if (val >= min && val <= max) return true;
    else return false;
}

function getRandomColor() {
    return "hsl(" + 360 * Math.random() + ',' +
    (25 + 70 * Math.random()) + '%,' + 
    (80 + 2 * Math.random()) + '%)'
}

// function getRandomColor() {
//     return '#' + (Math.random().toString(16) + "000000").substring(2,8);
// }

function getRects() {
    rects = [];

    for(var i = 0; i < NumRects; i++) {
        var curRect = document.getElementById("r"+i.toString());
        curRect.style.visibility = "visible";
        rects.push(curRect);
    }

    return rects;
}