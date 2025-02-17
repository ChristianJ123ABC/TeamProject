const images = [
    "../images/delivery.jpg",
    "../images/making-order.jpg",
    "../images/packing-order.jpg",
    "../images/recycle-image.jpg",
    "../images/takeaway.jpg"
  ];
  
  let currentImage = 0;
  
  function changeImage() {
    document.querySelector(".hero").style.backgroundImage = `url(${images[currentImage]})`;
    currentImage = (currentImage + 1) % images.length;
  }
  
  setInterval(changeImage, 4000); // Change image every 4 seconds
  changeImage(); // Set the first image immediately
  