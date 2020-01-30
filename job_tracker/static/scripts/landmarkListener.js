let modal = document.getElementById("landmark-form");

let btn = document.getElementById("landmark-btn");

let span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
};

span.onclick = function() {
    modal.style.display = "none";
};

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

let modal1 = document.getElementById("contact-form");

let btn1 = document.getElementById("contact-btn");

let span1 = document.getElementsByClassName("close")[1];

btn1.onclick = function() {
    modal1.style.display = "block";
};

span1.onclick = function() {
    modal1.style.display = "none";
};

window.onclick = function(event) {
    if (event.target == modal) {
        modal1.style.display = "none";
    }
};
