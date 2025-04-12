# Glenn's TEST CASE
# This test case is designed to test the payment process.

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
        "SECRET_KEY": "test_key"
    })
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.mysql')
def test_payment_missing_delivery_fee(mock_mysql, client):
    response = client.post('/create-checkout-session-one-time', data={
        'delivery': 'no',  # delivery fee not agreed
        'use_credits': 'yes'
    }, follow_redirects=True)

    assert b"You must agree to the delivery fee" in response.data
    assert response.status_code == 200

@patch('server.mysql')
def test_payment_empty_cart(mock_mysql, client):
    with client.session_transaction() as sess:
        sess['credits'] = 10
        sess['cart'] = []  # empty cart
    response = client.post('/create-checkout-session-one-time', data={
        'delivery': 'yes',
        'use_credits': 'yes'
    }, follow_redirects=True)

    assert b"Your cart is empty" in response.data
    assert response.status_code == 200

@patch('server.stripe.checkout.Session.create')
@patch('server.mysql')
def test_payment_uses_stripe(mock_mysql, mock_stripe, client):
    mock_stripe.return_value.url = "http://stripe-session-url"

    with client.session_transaction() as sess:
        sess['credits'] = 0
        sess['cart'] = [{'price': '5'}]

    response = client.post('/create-checkout-session-one-time', data={
        'delivery': 'yes',
        'use_credits': 'no'
    }, follow_redirects=False)

    assert response.status_code == 303
    assert response.location == "http://stripe-session-url"
