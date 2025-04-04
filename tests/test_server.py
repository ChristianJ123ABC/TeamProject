
from flask import session
from server import app  # make sure to import your actual app
from werkzeug.security import generate_password_hash
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # If you’re using CSRF protection
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login_valid_user(monkeypatch, client):
    test_email = "test@example.com"
    test_password = "password123"
    hashed_password = generate_password_hash(test_password)

    # Mock the database call to return a fake user
    def mock_fetchone_user():
        return {
            "user_id": 1,
            "full_name": "Test User",
            "email": test_email,
            "password": hashed_password,
            "role": "customer",
            "phone_number": "1234567890",
            "address": "Test Address"
        }

    def mock_fetchone_customer():
        return {
            "customer_id": 1,
            "credits": 50,
            "status": "active",
            "pending_credits": 10
        }

    # Monkeypatch the database cursor execute & fetchone
    class MockCursor:
        def execute(self, query, params):
            self.query = query
            self.params = params

        def fetchone(self):
            if "FROM Users" in self.query:
                return mock_fetchone_user()
            elif "FROM Customers" in self.query:
                return mock_fetchone_customer()

        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()

    monkeypatch.setattr("server.mysql", type("MockMySQL", (), {"connection": MockConnection()}))

    response = client.post("/login", data={
        "email": test_email,
        "password": test_password
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"customer" in response.data  # assuming "customer" appears in the HTML of the customer page
    assert session.get("user_id") == 1