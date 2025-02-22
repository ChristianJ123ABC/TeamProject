const images = [
    "static/delivery.jpg",
    "static/making-order.jpg",
    "static/packing-order.jpg",
    "static/recycle-image.jpg",
    "static/takeaway.jpg"
  ];
  
  let currentImage = 0;
  
  function changeImage() {
    document.querySelector(".hero").style.backgroundImage = `url(${images[currentImage]})`;
    currentImage = (currentImage + 1) % images.length;
  }
  
  setInterval(changeImage, 4000); // Change image every 4 seconds
  changeImage(); 
  

  