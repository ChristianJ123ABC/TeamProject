
const images = [
    "images/delivery.jpg",
    "images/making-order.jpg",
    "images/packing-order.jpg",
    "images/recycle-image.jpg",
    "images/takeaway.jpg"
];

let currentImageIndex = 0;


function changeBackgroundImage() {
    const heroSection = document.getElementById("hero");
    heroSection.style.backgroundImage = `url(${images[currentImageIndex]})`;

    
    currentImageIndex = (currentImageIndex + 1) % images.length;
}


setInterval(changeBackgroundImage, 4000);


document.addEventListener("DOMContentLoaded", changeBackgroundImage);
