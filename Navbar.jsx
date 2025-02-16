import { Link } from "react-router-dom";
import { FaShoppingBasket, FaRecycle } from "react-icons/fa"; 
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">Can & Dash</Link>
      </div>

      <ul className="nav-links">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/recycle">
            <FaRecycle className="nav-icon" /> Recycle
          </Link>
        </li>
        <li>
          <Link to="/profile">Profile</Link>
        </li>
        <li>
          <Link to="/basket">
            <FaShoppingBasket className="nav-icon" />
          </Link>
        </li>
      </ul>

      <div className="auth-buttons">
        <Link to="/login" className="btn login">Login</Link>
        <Link to="/signup" className="btn signup">Sign Up</Link>
      </div>
    </nav>
  );
}
