console.log("✅ script.js is linked and running!");


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
     
    
      console.log("✅ script.js is linked and running!");

      // 🛒 Function to add an item to cart
      async function addToCart(name, price) {
          console.log(`🛒 Adding to cart: ${name} - €${price}`);
      
          try {
              const response = await fetch('/add_to_cart', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ name, price })
              });
      
              const data = await response.json();
              console.log("✅ Cart Response:", data);
      
              alert(`${name} added to cart!`);
              await loadCart(); // 🔥 Forces the cart to update after adding
          } catch (error) {
              console.error("❌ Error adding to cart:", error);
          }
      }
      
      // 🛍️ Function to load the cart on the checkout page
      async function loadCart() {
          console.log("🔄 Fetching cart data...");
      
          try {
              const response = await fetch('/get_cart');
              const data = await response.json();
              console.log("✅ Loaded Cart Data:", data);
      
              const cartList = document.getElementById('cart-items');
              const totalPriceElem = document.getElementById('total-price');
      
              if (!cartList || !totalPriceElem) {
                  console.warn("⚠️ Cart elements not found in the DOM.");
                  return;
              }
      
              cartList.innerHTML = "";
              let totalPrice = 0;
      
              if (data.cart.length === 0) {
                  cartList.innerHTML = "<p>No items in cart.</p>";
              } else {
                  data.cart.forEach(item => {
                      const listItem = document.createElement('li');
                      listItem.textContent = `${item.name} - €${item.price}`;
                      cartList.appendChild(listItem);
                      totalPrice += item.price;
                  });
              }
      
              totalPriceElem.textContent = totalPrice.toFixed(2);
              updateTotal();
          } catch (error) {
              console.error("❌ Error loading cart:", error);
          }
      }
      
      // 💳 Load user credits
      async function loadCredits() {
          try {
              const response = await fetch('/get_user_credit');
              const data = await response.json();
              document.getElementById('user-credit').textContent = data.credit;
          } catch (error) {
              console.error("❌ Error loading credits:", error);
          }
      }
      
      // 🏷️ Update total payment amount
      function updateTotal() {
          let total = parseFloat(document.getElementById('total-price').textContent) || 0;
          let deliveryFee = document.getElementById('delivery').checked ? 2 : 0;
          let userCredit = parseFloat(document.getElementById('user-credit').textContent) || 0;
          let finalAmount = Math.max(0, total + deliveryFee - userCredit);
      
          document.getElementById('final-amount').textContent = finalAmount.toFixed(2);
          document.getElementById('delivery-hidden').value = deliveryFee;
      }
      
      // ✅ Ensure "Add" buttons work even after page load
      document.addEventListener("DOMContentLoaded", function () {
          console.log("🔄 Initializing cart and credits...");
      
          loadCart();
          loadCredits();
      
          document.getElementById('delivery')?.addEventListener("change", updateTotal);
      
          document.querySelectorAll(".btn-success").forEach(button => {
              button.addEventListener("click", function () {
                  const mealName = this.getAttribute("data-name");
                  const mealPrice = parseFloat(this.getAttribute("data-price"));
                  addToCart(mealName, mealPrice);
              });
          });
      });
      
      // 🛍️ Auto-load cart when navigating to checkout page
      document.addEventListener("DOMContentLoaded", async function () {
          console.log("🔄 Fetching cart data...");
          
          await loadCart(); // 🔥 Forces the cart to load on page load
          loadCredits(); // ⬅️ Load user credits too
      });
      