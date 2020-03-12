
// Variables to keep track of the interval id, velocity, and position of ball.
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
    resetBricks();

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


function resetBricks() {
    // Set bricks to equal an empty array.
    bricks = [];

    // Set the x and y of the original bricks.
    var origX = 50.5, origY = 50;

    // Variables that will changed to determine the x and y of each brick.
    var curX = origX, curY = origY;

    var bbox = document.getElementById("container").getBoundingClientRect();
    var bboxWidth = parseFloat(bbox.width);

    for(var i = 0; i < NumRects; i++) {
        var curRect = document.getElementById("r"+i.toString());

        // If the current brick would go past the edge of the svg,
        // go to a new line.
        if(curX + RecWidth + 15 >= bboxWidth) {
            curX = origX;
            curY += RecHeight + 15;
        }

        // Set the attributes of the bricks at the start of the game.
        curRect.setAttribute("x", curX);
        curRect.setAttribute("y", curY);
        curRect.setAttribute("width", RecWidth);
        curRect.setAttribute("height", RecHeight);
        curRect.setAttribute("fill", getRandomPastel());
        curRect.setAttribute("stroke", "black");
        curRect.setAttribute("stroke-width", 1);


        // Update the curX do that the space between each brick in row is even.
        curX += RecWidth + 33.33;

        // Make sure the brick is visible and add it to the list of bricks.
        curRect.style.visibility = "visible";
        bricks.push(curRect);
    }

    // Set the maximum y of the bricks plus a little extra.
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

    // The mouse is controlling the center of the paddle.

    // Set the paddle to be touching the right edge of the svg if the paddle
    // would move past the right edge.
    if (xMouse + widthPaddle/2 >= rightBBox) {
        paddle.setAttribute("x", widthBBox - widthPaddle);
    }

    // Set the paddle to be touching the left edge of the svg if the paddle
    // would move past the left edge.
    else if (xMouse - widthPaddle/2 <= leftBBox) {
        paddle.setAttribute("x", 0);
    }

    // If the paddle would not break out of the svg, keep the mouse controlling
    // the middle of the paddle. 
    else {
        paddle.setAttribute("x", xMouse - leftBBox - widthPaddle/2);
    }
}

// Function that will be repeated to update game.
function gameActions() {
    
    // Call the three functions of what must be checked everytime the ball moves
    wallCollisions();
    brickCollisions();
    paddleCollision();


    var ball = document.getElementById("ball"); 

    // Update the position by adding the velocities so that the ball moves by
    // one pixel in the specified directions every time this function is called. 
    posX += vx;
    posY += vy;
    ball.setAttribute("cx", posX);
    ball.setAttribute("cy", posY);

    // Check if all the bricks are hidden, which means the player has won.
    if(bricks.length == 0) {
        gamesWon++;

        // Update the text saying how many times the user has currently won.
        document.getElementById("games-won").innerHTML= ("You have won " + gamesWon + " game(s) :)");

        // Give the player a pop up alert and stop the game from continuing. 
        alert("You have won the game");
        clearInterval(id);
    }
    
}

function paddleCollision() {
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));

    // If the ball is not close the paddle, skip the rest of the function to be
    // more effienceint. 
    if(posY + radius <= minPaddleY) return;

    var paddle = document.getElementById("paddle");
    var xPaddle = parseFloat(paddle.getAttribute("x"));
    var yPaddle = parseFloat(paddle.getAttribute("y"));
    var widthPaddle = parseFloat(paddle.getAttribute("width"));
    var heightPaddle = parseFloat(paddle.getAttribute("height"));

    // Math to figure out how far away each corner of the ball is in terms of x and y.
    var ballCornerDist = radius / Math.sqrt(2);

    // Check if ball bounces of the top of paddle and update its 
    // velocity to go up.
    if(posX >= xPaddle && posX <= xPaddle + widthPaddle && inRange(posY + radius, yPaddle, 1)) {
        vy = -1;
    }

    // Check if ball bounces of the right of paddle and update its 
    // velocity to go up and right.
    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX - radius, xPaddle + widthPaddle, 1)) {
        vy = -1;
        vx = 1;
    }

    // Check if ball bounces of the left of paddle and update its 
    // velocity to go up and left.
    else if(posY >= yPaddle && posY <= yPaddle + heightPaddle && inRange(posX + radius, xPaddle, 1)) {
        vy = -1;
        vx = -1;
    }

    // Check if the ball bounces of the top-left corner of the paddle and 
    // adjust the ball's velocity to go up and right.
    else if(inRange(distance(posX - ballCornerDist, posY + ballCornerDist, xPaddle + widthPaddle, yPaddle), 2, 2)){
        vy = -1;
        vx = 1;
    }

      // Check if the ball bounces of the top-left corner of the paddle and 
    // adjust the ball's velocity to go up and left.
    else if(inRange(distance(posX + ballCornerDist, posY + ballCornerDist, xPaddle, yPaddle), 2, 2)) {
        vy = -1;
        vx = -1;
    }

}

// Function that checks if the ball has hit a brick. 
function brickCollisions() {
    
    var ball = document.getElementById("ball");
    var radius = parseFloat(ball.getAttribute("r"));

    // If the ball is not close to any of the blocks, hidden or visible, skip
    // the rest of the function. 
    if(posY - radius >= maxBlockY) return;

    // Iterate through every brick and check if the ball collided with it. 
    // Iterating backwards is more efficient as the bricks lower down will
    // be later in the list due to how it is created. 
    for(var i = bricks.length-1; i >= 0; i--) {

        var curBrick = bricks[i];
        var xBlock = parseFloat(curBrick.getAttribute("x"));
        var yBlock = parseFloat(curBrick.getAttribute("y"));
        var widthBlock = parseFloat(curBrick.getAttribute("width"));
        var heightBlock = parseFloat(curBrick.getAttribute("height"));

        // Math to figure out how far away each corner of the ball is in terms of x and y.
        var ballCornerDist = radius / Math.sqrt(2);


        // the "inrange()" function is used since exact differnces are
        // imposible to calculate due to floating point numbers as well
        // having the bricks appear more responsive and work with less bugs.


        // Check if the ball has hit the bottom of the current brick and if it
        // has, hide the brick, remove it from the bricks array, change the 
        // velocity of the ball so it goes downwards, and skip the rest of the
        // function as it can not hit any other bricks this iteration.
        if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY - radius, yBlock + heightBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            return;
        }

        // Check if the ball has hit the top of the current brick and if it
        // has, hide the brick, remove it from the bricks array, change the 
        // velocity of the ball so it goes upwards, and skip the rest of the
        // function as it can not hit any other bricks this iteration.
        else if(posX >= xBlock && posX <= xBlock + widthBlock && inRange(posY + radius, yBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            return;
        }

        // Check if the ball has hit the right of the current brick and if it
        // has, hide the brick, remove it from the bricks array, change the 
        // velocity of the ball so it goes to the right, and skip the rest of
        // the function as it can not hit any other bricks this iteration.
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX - radius , xBlock + widthBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vx = 1;
            return;
        }

        // Check if the ball has hit the left of the current brick and if it
        // has, hide the brick, remove it from the bricks array, change the 
        // velocity of the ball so it goes to the left, and skip the rest of
        // the function as it can not hit any other bricks this iteration.
        else if(posY >= yBlock && posY <= yBlock + heightBlock && inRange(posX + radius, xBlock, 1)) {
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vx = -1;
            return;
        }


        // Check if the ball has hit the bottom-right corner of the current 
        // brick by using the distance formula and if it has, hide the brick, 
        // remove it from the bricks array, change the velocity of the ball so
        // it goes to the bottom and right, and skip the rest of the function
        // as it can not hit any other bricks this iteration.
        else if (inRange(distance(posX - ballCornerDist, posY - ballCornerDist, xBlock + widthBlock, yBlock + heightBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            vx = 1;
            return;
        }

        // top-right corner of ball
        // Check if the ball has hit the bottom-left corner of the current 
        // brick by using the distance formula and if it has, hide the brick, 
        // remove it from the bricks array, change the velocity of the ball so
        // it goes to the bottom and left, and skip the rest of the function 
        // as it can not hit any other bricks this iteration.
        else if (inRange(distance(posX + ballCornerDist, posY - ballCornerDist, xBlock, yBlock + heightBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = 1;
            vx = -1;
            return;
        }
        
        // Check if the ball has hit the top-right corner of the current 
        // brick by using the distance formula and if it has, hide the brick, 
        // remove it from the bricks array, change the velocity of the ball so
        // it goes to the top and right, and skip the rest of the function 
        // as it can not hit any other bricks this iteration.
        else if (inRange(distance(posX - ballCornerDist, posY + ballCornerDist, xBlock + widthBlock, yBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            vx = 1;
            return;
        }

        // Check if the ball has hit the top-left corner of the current 
        // brick by using the distance formula and if it has, hide the brick, 
        // remove it from the bricks array, change the velocity of the ball so
        // it goes to the top and left, and skip the rest of the function 
        // as it can not hit any other bricks this iteration.
        else if (inRange(distance(posX + ballCornerDist, posY + ballCornerDist, xBlock, yBlock), 2, 2)){
            curBrick.style.visibility = "hidden";
            bricks.splice(i, 1);
            vy = -1;
            vx = -1;
            return;
        }   
    }
}

// Function that detects if the ball has hit the wall and takes the appropriate
// steps after. 
function wallCollisions() {
    var ball = document.getElementById("ball"); 
    var radius = parseFloat(ball.getAttribute("r")); 
    var svgWidth = parseFloat(document.getElementById("container").getAttribute("width"));
    var svgHeight = parseFloat(document.getElementById("container").getAttribute("height"))


    // If the ball hits the right wall, make the ball go left.
    if (posX + radius  >= svgWidth) { 
        vx = -1;
    }

    // If the ball hits the left wall, make the ball go right.
    else if (radius >= posX){
        vx = 1;
    }

    // If the ball hits the top wall, make the ball go down.
    else if (radius >= posY){
        vy = 1;
    }

    // If the ball hits the bottom wall, the player loses the game.
    else if (posY + radius  >= svgHeight) { 

        // Increase the number of games lost and display to the user the
        // number of games they have currently won or lost on the web page.
        gamesLost++;
        document.getElementById("games-lost").innerHTML = ("You have lost " + gamesLost + " game(s) :(");

        // Stop the gam animation and display a pop up to the player to show
        // them that they have lost. 
        // The id is not set to null here to make sure the game does not break
        // if the player starts another round without reseting the game. 
        clearInterval(id); 
        alert("You lost the game");
    }
}

// HELPER METHODS

// Function that is conuntually called so the user knows what speed setting
// is currently active. A citation for this is on the home page.
function changeSpeed() {
    var slider = document.getElementById("myRange");
    var output = document.getElementById("slider-text");
    output.innerHTML = ("The current speed setting is " + slider.value); 
}


// Standard Euclidian distance formula used for corner collision detection.
function distance(x1, y1, x2, y2) {
    return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}

// Function to make sure values used when detecting collisions are not too 
// picky to ensure that the game plays smoothly.
function inRange(val, comp, dif) {
    if (val >= comp-dif && val <= comp+dif) return true;
    else return false;
}

// Function that generates a pastel color, citation for this is on home page. 
function getRandomPastel() {
    return "hsl(" + 360 * Math.random() + ',' +
    (25 + 70 * Math.random()) + '%,' + 
    (80 + 2 * Math.random()) + '%)'
}