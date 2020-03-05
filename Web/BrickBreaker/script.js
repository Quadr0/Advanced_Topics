var id, posX, posY, vx, vy;

const NumRects = 20;
const RecWidth = 80, RecLength = 30;

function setup() {
    rects = getRects();

    var curX = 50, curY = 60;
    //console.log(NumRects);

    var bbox = document.getElementById("container").getBoundingClientRect();
    var bboxWidth = parseFloat(bbox.right);
    for(var i = 0; i < NumRects; i++) {

        if(curX + RecWidth >= bboxWidth - 10) {
            curX = 50;
            curY += RecLength + 20;
        }
        //console.log(i);
        rects[i].setAttribute("x", curX);
        rects[i].setAttribute("y", curY);
        rects[i].setAttribute("width", RecWidth);
        rects[i].setAttribute("height", RecLength);
        rects[i].setAttribute("fill", getRandomColor());

        curX += RecWidth + 20
        //console.log(i);
    }
    
    //console.log(rects.length);

}

function getRects() {
    rects = [];

    for(var i = 0; i < NumRects; i++) {
        var curRect = document.getElementById("r"+i.toString(10));
        rects.push(curRect);
    }
    //console.log(rects.length);
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

    if (xMouse + widthRect/2 + 20 >= rightBBox) {
        r.setAttribute("x", widthBBox - widthRect);
    }
    else if (xMouse - widthRect/2 + 20 <= leftBBox) {
        r.setAttribute("x", 0);
    }
    else {
        r.setAttribute("x", xMouse - widthRect/2);
    }
}

function getRandomColor() {
    return '#' + (Math.random().toString(16) + "000000").substring(2,8);
}