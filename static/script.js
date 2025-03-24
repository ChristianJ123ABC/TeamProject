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
     
    
      console.log(" script.js is linked and running!");

      // Function to add an item to cart
      async function addToCart(name, price) {
          console.log(` Adding to cart: ${name} - €${price}`);
      
          try {
              const response = await fetch('/add_to_cart', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ name, price })
              });
      
              const data = await response.json();
              console.log(" Cart Response:", data);
      
              alert(`${name} added to cart!`);
              await loadCart(); // Forces the cart to update after adding
          } catch (error) {
              console.error(" Error adding to cart:", error);
          }
      }
      

      //  Function to load the cart on the checkout page
      async function loadCart() {
        console.log(" Fetching cart data...");
        try {
            const response = await fetch('/get_cart');
            const data = await response.json();

            const cartList = document.getElementById('cart-items');
            const totalPriceElem = document.getElementById('total-price');

            cartList.innerHTML = "";
            let totalPrice = 0;

            if (data.cart.length === 0) {
                cartList.innerHTML = "<p>No items in cart.</p>";
            } else {
                let itemCounts = {};
                data.cart.forEach(item => {
                    if (!itemCounts[item.name]) {
                        itemCounts[item.name] = { price: item.price, quantity: 1 };
                    } else {
                        itemCounts[item.name].quantity += 1;
                    }
                });
    
                Object.keys(itemCounts).forEach(name => {
                    let item = itemCounts[name];
                    const listItem = document.createElement('li');
                    listItem.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
    
                    listItem.innerHTML = `
                        ${name} (x${item.quantity}) - €${(item.price * item.quantity).toFixed(2)}
                        <button class="btn btn-sm btn-danger" onclick="removeFromCart('${name}')">Remove</button>
                    `;
    
                    cartList.appendChild(listItem);
                    totalPrice += item.price * item.quantity;
                });
            }
    
            totalPriceElem.textContent = totalPrice.toFixed(2);
            updateTotal();
        } catch (error) {
            console.error(" Error loading cart:", error);
        }
    }

    // Start Code Prakash

    //  Remove item from cart
    async function removeFromCart(itemName) {
        try {
            const response = await fetch('/remove_from_cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: itemName })
            });

            const data = await response.json();
            console.log(" Removed:", data);
            loadCart(); // Reload the cart
        } catch (error) {
            console.error(" Error removing item:", error);
        }
    }

      
      //  Load user credits
      async function loadCredits() {
        try {
            const response = await fetch('/get_user_credit');
            const data = await response.json();
            document.getElementById('user-credit').textContent = parseFloat(data.credit).toFixed(2);
            updateTotal();
        } catch (error) {
            console.error(" Error loading credits:", error);
        }
    }
      
    // Update total payment amount
    function updateTotal() {
        let total = parseFloat(document.getElementById('total-price').textContent) || 0;
        let deliveryFeeChecked = document.getElementById('delivery').checked;
        let deliveryFee = deliveryFeeChecked ? 2 : 0;
        let useCredits = document.getElementById('use-credits').checked;
        let userCredit = parseFloat(document.getElementById('user-credit').textContent) || 0;

        let finalAmount = total + deliveryFee; // Base price including delivery
        if (useCredits) {
            finalAmount = Math.max(0, finalAmount - userCredit); // Deduct user credits if checked
        }

        document.getElementById('final-amount').textContent = finalAmount.toFixed(2);

        // Update hidden delivery field for form submission
        document.getElementById('delivery-hidden').value = deliveryFeeChecked ? "yes" : "no";
    }

        // Checkout Process
    async function checkout() {
        let useCredits = document.getElementById('use-credits').checked;
        let deliveryFeeChecked = document.getElementById('delivery').checked;
        
        if (!deliveryFeeChecked) {
            alert("Please select the delivery fee option to proceed.");
            return;
        }

        try {
            const response = await fetch('/create-checkout-session-one-time', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ use_credits: useCredits, delivery: "yes" }) // Ensure delivery is always "yes"
            });

            const data = await response.json();

            if (data.url) {
                window.location.href = data.url; // Redirect to Stripe payment
            } else if (data.message) {
                alert(data.message); // Show success message (if paid via credits)
                window.location.reload(); // Refresh page
            } else {
                alert("Error processing payment!");
                console.error("Payment Error:", data);
            }
        } catch (error) {
            console.error("Error during checkout:", error);
            alert("An error occurred. Please try again.");
        }
    }

        // Initialize checkout page
        document.addEventListener("DOMContentLoaded", function () {
            console.log("Initializing checkout page...");
            loadCart();
            loadCredits();

            //Attach event listners
            document.getElementById('delivery').addEventListener("change", updateTotal);
            document.getElementById('use-credits').addEventListener("change", updateTotal);

            // Select the form explicitly and prevent submission if delivery is unchecked
            const checkoutForm = document.querySelector("form");

            checkoutForm.addEventListener("submit", function (event) {
                let deliveryCheckbox = document.getElementById('delivery');

                if (!deliveryCheckbox.checked) {
                    event.preventDefault(); // Stop form submission
                    alert("Please select the 'Include Delivery' option to proceed!");
                } else {
                    document.getElementById('delivery-hidden').value = "yes"; // Ensure delivery fee is passed
                }
            });

            updateTotal(); // Ensure values update on page load

                });
      
        //End Code Prakash


      
      //  Ensure "Add" buttons work even after page load
      document.addEventListener("DOMContentLoaded", function () {
          console.log(" Initializing cart and credits...");
      
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
      
