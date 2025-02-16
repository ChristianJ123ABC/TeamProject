import { useState, useEffect } from "react";
import "./Home.css";

const images = [
  "/delivery.jpg",
  "/making-order.jpg",
  "/packing-order.jpg",
  "/recycle-image.jpg",
  "/takeaway.jpg"
  
];

export default function Home() {
  const [currentImage, setCurrentImage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 4000); // this to Change image every 4 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="home-container">
      {/* hero Section with Dynamic Background */}
      <header
        className="hero"
        style={{ backgroundImage: `url(${images[currentImage]})` }}
      >
        <div className="hero-content">
          <h1>Recycle & Enjoy Discounted Food</h1>
          <p>Turn your cans and bottles into rewards for delicious meals!</p>
          <button className="explore-btn">Explore Restaurants</button>
        </div>
      </header>

      {/*the Searxh Bar */}
      <div className="search-bar">
        <input type="text" placeholder="Search for restaurants..." />
        <button>Search</button>
      </div>

    {/* featured Restaurants box */}
      <section className="featured">
  <h2>Featured Restaurants</h2>
  <div className="restaurant-grid">
    <div className="restaurant-card">
      <img src="/burger.jpg" alt="Joe's Burger Bar" />
      <h3>Joe's Burger Bar</h3>
      <p>Discounts up to 50% on selected meals</p>
    </div>
    <div className="restaurant-card">
      <img src="/pizzeria.jpg" alt="Papa's Pizzeria" />
      <h3>Papa's Pizzeria</h3>
      <p>Special offers on all pizzas</p>
    </div>
    <div className="restaurant-card">
      <img src="/sushi.jpg" alt="Sushi Express" />
      <h3>Sushi Express</h3>
      <p>Fresh sushi at amazing discounts</p>
    </div>
  </div>
</section>



      {/* How It Works box */}
      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <h3>1. Recycle</h3>
            <p>Deposit your cans and bottles in our partnered machines.</p>
          </div>
          <div className="step">
            <h3>2. Earn Credits</h3>
            <p>Receive credits that you can use for discounts on food.</p>
          </div>
          <div className="step">
            <h3>3. Enjoy Food</h3>
            <p>Redeem your credits at partnered restaurants and eat for less!</p>
          </div>
        </div>
      </section>
    </div>
   
   
    
  );
}
