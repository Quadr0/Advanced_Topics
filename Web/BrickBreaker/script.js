// varibles to keep track of the interval id, velocity, and position of ball.
var id, posX, posY, vx, vy;

// Keep track of who many games have been lost or won in the current session.
var gamesWon = 0, gamesLost = 0;

// Set the point where the ball will jstart checkingfor collisions against
// the bricks and paddle to be more effiecient and not always check.
var maxBlockY, minPaddleY = 500;

// List that will keep track of current visible bricks.
var bricks;

// User changeable speed that will control how fast the ball/game is.
// Default is 5.
var intervalSpeed = 5;

// Constants to ensure rectangle length/height and number of rectangles
// stays constant.
const NumRects = 20;
const RecWidth = 100, RecHeight = 35;

function setup() {

    // Referesh the bricks and make sure they are all visibile.
    bricks = getRects();

    resetBricks();
    resetBall();
    
    // Set interval so that the slider to change game speed is responsive.
    setInterval(changeSpeed, 100);
}

// Function that will be called by the start button.
function startGame() {

    // Set the game speed to what user selected at start of each new game.
    intervalSpeed = parseFloat(document.getElementById("myRange").value);

    // WIll only start the game if the previous game has been reset.
    if (id == null) {
        id = setInterval(gameActions, intervalSpeed);
    }
}

// Function that will be called to reset game/
function resetGame() {

    // Break and reset the interval if it is not reset yet.
    // Makes sure multiple presses of button do not break the page.
    if(id != null) {
        clearInterval(id);
        id = null;
    }

    // Call the setup function to formally reset game.
    setup();
}

// Function to reset the ball after every game.
function resetBall() {
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);

    // Randomly set the X and Y of the ball somewhere in between paddle
    // and bricks.
    posX = radius + Math.random() * (widthBBox - radius*2);
    posY = 300 + radius + Math.random() * (100 - radius);
    
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);

    // Randomly determine the initial x velocity of the ball 
    // using a ternary statement.
    vx = Math.random() > .5 ? -1 : 1;
    vy = 1;
}


// Function to reset the bricks.
function resetBricks() {
    
    // Set the x and y of the original bricks.
    var origX = 50.5, origY = 50;

    // Variables that will changed to determine the x and y of each brick.
    var curX = origX, curY = origY;

    var bbox = document.getElementById("container").getBoundingClientRect();
    var bboxWidth = parseFloat(bbox.width);

    // Go through each bricks annd set its attributes.
    for(var i = 0; i < NumRects; i++) {

        // If the current brick would go past the edge of the svg,
        // go to a new line.
        if(curX + RecWidth + 15 >= bboxWidth) {
            curX = origX;
            curY += RecHeight + 15;
        }

        curRect = rects[i];

        curRect.setAttribute("x", curX);
        curRect.setAttribute("y", curY);
        curRect.setAttribute("width", RecWidth);
        curRect.setAttribute("height", RecHeight);
        curRect.setAttribute("fill", getRandomPastel());
        curRect.setAttribute("stroke", "black");
        curRect.setAttribute("stroke-width", 1);


        // Update the curX do that the space between each brick in row is even.
        curX += RecWidth + 33.33;
    }
    
    // Set the maximum y of the bricks plus a little extra so that collisions
    // between bricks and the ball are not checked when absolutely no
    // collisions will occur. 
    biggestBlockY = curY + RecHeight + 20;
}

// Function that gets called eveytime the mouse is moved to move the paddle.
function mousePosition(e) {
    var xMouse = parseFloat(e.clientX);
    
    var paddle = document.getElementById("paddle");
    var widthPaddle = parseFloat(paddle.getAttribute("width"));

    var bbox = document.getElementById("container").getBoundingClientRect();
    var widthBBox = parseFloat(bbox.width);
    var rightBBox = parseFloat(bbox.right);
    var leftBBox = parseFloat(bbox.left);

    // Set the paddle to be touching the right edge of the 
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
        gamesWon++;
        document.getElementById("games-won").innerHTML= ("You have won " + gamesWon + " game(s) :)");

        alert("You have won the game");
        clearInterval(id);
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

    var ballCornerDist = radius / Math.sqrt(2);



    // Check if ball bounces of top of paddle.
    if(posX >= xPaddle && posX <= xPaddle + widthPaddle && inRange(posY + radius, yPaddle, 1)) {
        vy = -1;
    }

    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX - radius, xPaddle + widthPaddle, 1)) {
        vy = -1;
        vx = 1;
    }

    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX + radius, xPaddle, 1)) {
        vy = -1;
        vx = -1;
    }

    // bottom-left of ball
    else if(inRange(distance(posX - ballCornerDist, posY + ballCornerDist, xPaddle + widthPaddle, yPaddle), 2, 2)){
        vy = -1;
        vx = 1;
    }

    // bottom-right of ball
    else if(inRange(distance(posX + ballCornerDist, posY + ballCornerDist, xPaddle, yPaddle), 2, 2)) {
        vy = -1;
        vx = -1;
    }

}

function brickCollisions() {
    
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));

    if(posY >= maxBlockY) return;

    for(var i = bricks.length-1; i >= 0; i--) {

        var curBrick = bricks[i];
        var xBlock = parseFloat(curBrick.getAttribute("x"));
        var yBlock = parseFloat(curBrick.getAttribute("y"));
        var widthBlock = parseFloat(curBrick.getAttribute("width"));
        var heightBlock = parseFloat(curBrick.getAttribute("height"));

        var ballCornerDist = radius / Math.sqrt(2);


        // bottom of brick
        if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY - radius, yBlock + heightBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            return;
        }

        // top of brick
        else if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY + radius, yBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            return;
        }

        //right of brick
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX - radius , xBlock + widthBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vx = 1;
            return;
        }

        //left of brick
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX + radius, xBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vx = -1;
            return;
        }


        //check top-left corner of ball
        else if (inRange(distance(posX - ballCornerDist, posY - ballCornerDist, xBlock + widthBlock, yBlock + heightBlock), 2, 2)){
        //if (inRange(posX - ballCornerDist, xBlock + widthBlock, 3) && inRange(posY - ballCornerDist, yBlock + heightBlock, 3)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            vx = 1;
            return;
        }

        // top-right corner of ball
        else if (inRange(distance(posX + ballCornerDist, posY - ballCornerDist, xBlock, yBlock + heightBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            vx = -1;
            return;
        }
        
        // bottom-left of corner
        else if (inRange(distance(posX - ballCornerDist, posY + ballCornerDist, xBlock + widthBlock, yBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            vx = 1;
            return;
        }

        // bottom-right of corner
        else if (inRange(distance(posX + ballCornerDist, posY + ballCornerDist, xBlock, yBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            vx = 1;
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
  
    }
    else if (radius >= posX){
        vx = 1;
    }

    // If you hit the bottom wall, you lose the game. 
    if (posY + radius  >= svgHeight) { 
        vy = -1;

        gamesLost++;
        document.getElementById("games-lost").innerHTML = ("You have lost " + gamesLost + " game(s) :(");

        clearInterval(id); 
        alert("You lost the game");
        
    }
    else if (radius >= posY){
        vy = 1;
    }
}

function changeSpeed() {
    var slider = document.getElementById("myRange");
    var output = document.getElementById("slider-text");
    output.innerHTML = ("The current slide setting is " + slider.value); 
}

function distance(x1, y1, x2, y2) {
    return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}

function inRange(val, comp, dif) {
    if (val >= comp-dif && val <= comp+dif) return true;
    else return false;
}

function getRandomPastel() {
    return "hsl(" + 360 * Math.random() + ',' +
    (25 + 70 * Math.random()) + '%,' + 
    (80 + 2 * Math.random()) + '%)'
}

function getRects() {
    rects = [];

    for(var i = 0; i < NumRects; i++) {
        var curRect = document.getElementById("r"+i.toString());
        curRect.style.visibility = "visible";
        rects.push(curRect);
    }

    return rects;
}