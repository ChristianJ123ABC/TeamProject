# tests/test_server.py
import pytest
from flask import session
from werkzeug.security import generate_password_hash
from server import app  # import your app

# Mocking the database calls
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client

# Mock data for testing
@pytest.fixture
def mock_user_data():
    return {
        "user_id": 1,
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": generate_password_hash("password123"),
        "role": "customer",
        "phone_number": "1234567890",
        "address": "123 Main St"
    }

@pytest.fixture
def mock_customer_data():
    return {
        "customer_id": 1,
        "credits": 100,
        "status": "active",
        "pending_credits": 20
    }

def test_login_valid_user(client, mock_user_data, mock_customer_data, monkeypatch):
    # Mock the database interactions
    def mock_execute(query, params):
        if "FROM Users" in query:
            return mock_user_data
        elif "FROM Customers" in query:
            return mock_customer_data
        return None

    class MockCursor:
        def execute(self, query, params):
            return mock_execute(query, params)
        def fetchone(self):
            return mock_execute(self.query, self.params)
        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()

    monkeypatch.setattr("server.mysql.connection", MockConnection())

    # Simulate a POST request to the login route with valid credentials
    response = client.post("/login", data={
        "email": mock_user_data["email"],
        "password": "password123"
    }, follow_redirects=True)

    # Check the session is set correctly
    assert response.status_code == 200
    assert session["user_id"] == mock_user_data["user_id"]
    assert session["role"] == mock_user_data["role"]
    assert session["full_name"] == mock_user_data["full_name"]
    assert session["email"] == mock_user_data["email"]
    assert session["phone_number"] == mock_user_data["phone_number"]
    assert session["address"] == mock_user_data["address"]
    assert "customer_id" in session  # customer details are loaded

    # Check that the user is redirected to the "customer" page
    assert response.request.path == '/customer'
