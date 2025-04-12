# Glenn's TEST CASE
# Login tests for driver functionality

# root directory import
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app  

# Pytest fixture to create a test client for simulating HTTP requests
@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    yield app.test_client()

def test_blank_email_password(client):
    response = client.post('/login', data={
        'email': '',
        'password': ''
    }, follow_redirects=True)
    assert b"You must type in an email AND a password" in response.data

def test_invalid_email(client):
    response = client.post('/login', data={
        'email': 'nonexist@gmail.com',
        'password': 'somepass'
    }, follow_redirects=True)
    assert b"Invalid email address" in response.data

def test_wrong_password(client):
    response = client.post('/login', data={
        'email': 'abc@gmail.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b"Invalid password" in response.data

def test_successful_driver_login(client):
    response = client.post('/login', data={
        'email': 'abc@gmail.com',
        'password': '123'
    }, follow_redirects=True)
    assert b"Driver Dashboard" in response.data  

