var id, posX, posY, vx, vy;

var maxBlockY, minPaddleY = 500;

var bricks;

const NumRects = 20;
const RecWidth = 100, RecLength = 35;

function setup() {
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

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);

    posX = radius + 100 + Math.random() * (widthBBox - radius - 100);
    // poxY = radius + Math.random() * ( - radius);
    posY = 300 + radius + Math.random() * (175 - radius - 50);
    
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);

    vx = Math.random() > .5 ? -1 : 1;
    vy = 1;
}

function resetRects() {
    var origX = 50.5, origY = 50;
    bricks = getRects();

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
        curRect.setAttribute("stroke-width", 1);


        curX += RecWidth + 33.33;
    }
    biggestBlockY = curY + RecLength;
}

function getRects() {
    rects = [];

    for(var i = 0; i < NumRects; i++) {
        var curRect = document.getElementById("r"+i.toString());
        rects.push(curRect);
    }

    return rects;
}

function mousePosition(e) {
    var xMouse = parseFloat(e.clientX);
    
    var addle = document.getElementById("paddle");
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

    posX += vx;
    posY += vy;
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);
}

function paddleCollision() {
    
    var xBall = parseFloat(ball.getAttribute("cx"));
    var yBall = parseFloat(ball.getAttribute("cy"));
    var radius = parseFloat(ball.getAttribute("r"));

    if(yBall <= minPaddleY) return;

    var paddle = document.getElementById("paddle");
    var xPaddle = parseFloat(paddle.getAttribute("x"));
    var yPaddle = parseFloat(paddle.getAttribute("y"));
    var widthPaddle = parseFloat(paddle.getAttribute("width"));
    var lengthPaddle = parseFloat(paddle.getAttribute("height"));

    console.log(xBall)

}

function rectCollision(rect) {
    var ball = document.getElementById("ball");
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

function getRandomColor() {
    return '#' + (Math.random().toString(16) + "000000").substring(2,8);
}