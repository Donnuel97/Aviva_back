let btnOpen = document.querySelector(".btn");
let box = document.querySelector(".box");
let body = document.querySelector("body");
let close = document.querySelector(".close");
let image = document.querySelector(".image");
let content = document.querySelector(".content");

btnOpen.addEventListener("click", () => {
    btnOpen.style.display = "none";
    box.style.display = "block";
    image.style.display = "none";
    content.style.display = "none";
    body.style.backgroundColor = "#222";
});

close.addEventListener("click", () => {
    btnOpen.style.display = "block";
    box.style.display = "none";
    image.style.display = "block"; // Display the header again when closing
    content.style.display = "block";
    body.style.backgroundColor = "#fff";
});
