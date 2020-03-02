function changeColor() {
    var c = document.getElementById("circle");
    var randColor = getRandomColor();
    c.setAttribute("fill", randColor);
}

function changeRadius() {
    var c = document.getElementById("circle");
    var randRad = 10 + Math.random() * 220;
    c.setAttribute("r", randRad);
}

function changeCenter() {
    var c = document.getElementById("circle");
    var randomX = Math.random() * 500;
    var randomY = Math.random() * 500;
    c.setAttribute("cx", randomX);
    c.setAttribute("cy", randomY);
}

function changeOpacity() {
    var c = document.getElementById("circle");
    var opacity = Math.random();
    c.setAttribute("opacity", opacity);
}

function reset() {
    var c = document.getElementById("circle");
    c.setAttribute("cx", 250);
    c.setAttribute("cy", 250);
    c.setAttribute("fill", "blue");
    c.setAttribute("opacity", 1);
    c.setAttribute("r", 100);
}

function getRandomColor() {
    return '#' + (Math.random().toString(16) + "000000").substring(2,8);
}