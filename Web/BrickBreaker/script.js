var id, posX, posY, vx, vy;

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
    rects = getRects();

    var curX = origX, curY = origY;

    var bbox = document.getElementById("container").getBoundingClientRect();
    var bboxWidth = parseFloat(bbox.right);
    for(var i = 0; i < NumRects; i++) {

        if(curX + RecWidth*2 >= bboxWidth - 50) {
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
    
    var r = document.getElementById("paddle");
    var widthRect = parseFloat(r.getAttribute("width"));

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);
    var rightBBox = parseFloat(bbox.right);
    var leftBBox = parseFloat(bbox.left);

    if (xMouse + widthRect/2 >= rightBBox) {
        r.setAttribute("x", widthBBox - widthRect);
    }
    else if (xMouse - widthRect/2 <= leftBBox) {
        r.setAttribute("x", 0);
    }
    else {
        r.setAttribute("x", xMouse - widthRect*3/2 + 20);
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
    var ball = document.getElementById("ball"); 

    var paddle = document.getElementById("paddle");

}

function rectCollision(bbox) {

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