# Glenn's TEST CASE
# This test is to verify deposits from customers as a driver

# root directory import
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import session
from server import app

@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_key"  # Needed for session usage
    })
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.mysql')
def test_verify_deposit_success(mock_mysql, client):
    # Setup mock cursor
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    # POST to the verification route
    response = client.post('/verify-deposit/1', follow_redirects=True)

    # Check that the 3 DB updates and commit were called
    assert mock_cursor.execute.call_count == 6
    assert mock_mysql.connection.commit.call_count == 3

    # Check that the user is redirected
    assert response.status_code == 200
    assert b"Pickup" in response.data or b"Dashboard" in response.data

@patch('server.mysql')
def test_verify_deposit_invalid_customer(mock_mysql, client):
    # Simulate database still running even if customer doesn't exist
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    # POST to route with a customer ID unlikely to exist
    response = client.post('/verify-deposit/9999', follow_redirects=True)

    # Still expect all commands to execute safely
    assert mock_cursor.execute.call_count == 6
    assert mock_mysql.connection.commit.call_count == 3

    # redirect
    assert response.status_code == 200
