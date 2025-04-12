# Glenn's TEST CASE
# This test case is for the decline-pickup endpoint.

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
        "SECRET_KEY": "test_key"  # Needed for session and flash
    })
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.mysql')
def test_decline_pickup_success(mock_mysql, client):
    # Setup mock cursor
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    # Simulate a POST request to decline a valid pickup
    response = client.post('/decline-pickup/12', follow_redirects=True)

    # Confirm DELETE query was issued (even if other queries followed)
    mock_cursor.execute.assert_any_call("DELETE FROM Pickups WHERE pickup_id = %s", (12,))
    assert mock_mysql.connection.commit.call_count >= 1
    assert response.status_code == 200
    assert b"declined" in response.data  # Adjust if needed

@patch('server.mysql')
def test_decline_pickup_invalid_id(mock_mysql, client):
    # Simulate deleting a non-existent pickup ID
    mock_cursor = MagicMock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    response = client.post('/decline-pickup/9999', follow_redirects=True)

    # Still expects an attempt to delete and commit
    mock_cursor.execute.assert_any_call("DELETE FROM Pickups WHERE pickup_id = %s", (9999,))
    assert mock_mysql.connection.commit.call_count >= 1
    assert response.status_code == 200