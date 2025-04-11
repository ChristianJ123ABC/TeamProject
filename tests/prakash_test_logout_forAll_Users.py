#resources
#https://pytest-flask.readthedocs.io/en/latest/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/latest/testing/
#https://www.youtube.com/watch?v=1aHNs1aEATg
#https://realpython.com/python-testing/#testing-flask-applications






import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import session
from server import app as create_app



@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()

# Test data for different user roles
Test_Users = {
    "foodOwner": {"email": "3456@gmail.com", "password": "1234", "expected_redirect": "/foodOwner"},
    "customer": {"email": "1234@gmail.com", "password": "1234", "expected_redirect": "/customer"},
    "driver": {"email": "2345@gmail.com", "password": "1234", "expected_redirect": "/driver"}
}

@pytest.mark.parametrize("role", ["foodOwner", "customer", "driver"])
def test_logout_for_All_roles(client, role):
    # First login the user
    credentials = Test_Users[role]
    login_response = client.post("/login", data={
        "email": credentials["email"],
        "password": credentials["password"]
    }, follow_redirects=True)
    
    assert login_response.status_code == 200
    assert login_response.request.path == credentials["expected_redirect"]
    
    # Check session exists before logout
    with client.session_transaction() as sess:
        assert "user_id" in sess
        assert "email" in sess
        assert "role" in sess
    
    # Perform logout
    logout_response = client.get("/logout", follow_redirects=True)
    
    assert logout_response.status_code == 200
    assert logout_response.request.path == "/login"  # logout redirects to login page
    
    # Verify session is cleared
    with client.session_transaction() as sess:
        assert "user_id" not in sess
        assert "email" not in sess
        assert "role" not in sess
    
    # Verify flash message if applicable
    # assert b"You have been logged out" in logout_response.data

def test_logout_without_login(client):
    # Ensure no session exists
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"  # Should still redirect to login

