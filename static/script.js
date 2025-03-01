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
  

        function searchRestaurants() {
            let input = document.getElementById("searchInput").value.toLowerCase();
            let restaurants = document.querySelectorAll(".restaurant-card");

            restaurants.forEach(card => {
                let title = card.querySelector(".card-title").innerText.toLowerCase();
                card.style.display = title.includes(input) ? "block" : "none";
            });
        }
 
        

        function claimOffer() {
          alert("✅ You have claimed this offer! Enjoy your discount.");
      }

     