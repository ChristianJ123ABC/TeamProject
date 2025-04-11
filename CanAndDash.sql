<!--Start -code by prakash-->

/* creade Can&Dash database*/
-- Create Database
CREATE DATABASE CanAndDash;
USE CanAndDash;

-- Table for Users (Generalized Table for All User Types) --
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'driver', 'food_owner') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Customers (Extends Users) --
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    address VARCHAR(255),
    credits DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Table for Drivers (Extends Users)--
CREATE TABLE Drivers (
    driver_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    vehicle_type VARCHAR(50),
    History VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (driver_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Table for Food Owners (Extends Users)--
CREATE TABLE FoodOwners (
    promoter_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    business_name VARCHAR(100),
    FOREIGN KEY (food_owner_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Table for Pickups--
CREATE TABLE Pickups (
    pickup_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    driver_id INT,
    pickup_date DATE NOT NULL,
    pickup_time TIME NOT NULL,
    status ENUM('pending', 'accepted', 'completed') DEFAULT 'pending',
    credits_earned DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id) ON DELETE SET NULL
);

-- Table for Food Listings--
CREATE TABLE FoodListings (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    promoter_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    discounted_price DECIMAL(10, 2),
    promotion_end_date DATE,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (food_owner_id) REFERENCES FoodOwners(food_owner_id) ON DELETE CASCADE
);

-- Table for Orders--
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    food_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'delivered') DEFAULT 'pending',
    credits_used DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES FoodListings(food_id) ON DELETE CASCADE
);

-- Table for Subscriptions--
CREATE TABLE Subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    promoter_id INT NOT NULL,
    stripe_subscription_id VARCHAR(255) NOT NULL,
    subscription_start_date DATETIME NOT NULL,
    subscription_end_date DATETIME NOT NULL,
    next_due_date DATETIME NOT NULL,
    status ENUM('active', 'canceled', 'incomplete') DEFAULT 'active',
    FOREIGN KEY (promoter_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


-- Table for Payments--
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_type ENUM('subscription', 'joining_fee', 'delivery_fee') NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('success', 'failed') DEFAULT 'success',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Deposits (
    deposit_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    deposited_credits DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'verified') DEFAULT 'pending',
    deposit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);


