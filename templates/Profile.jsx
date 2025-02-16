import "./Profile.css";

export default function Profile() {
  return (
    <div className="profile-container">
      <h1>Your Profile</h1>
      <p>Manage your account details and preferences.</p>

      <div className="profile-card">
        <div className="profile-image">
          {/* Profile Image from my Public Folder */}
          <img src="/profile.jpg" alt="Profile" />
        </div>
        <div className="profile-details">
          <form>
            <label>Full Name</label>
            <input type="text" placeholder="Your name" disabled />

            <label>Email Address</label>
            <input type="email" placeholder="Your email" disabled />

            <label>Phone Number</label>
            <input type="text" placeholder="Your phone" disabled />

            <label>Address</label>
            <textarea placeholder="Your address" disabled></textarea>

            <button className="edit-btn">Edit Profile</button>
          </form>
        </div>
      </div>

      <div className="order-history">
        <h2>Order History</h2>
        <p>You haven't placed any orders yet.</p>
      </div>
    </div>
  );
}