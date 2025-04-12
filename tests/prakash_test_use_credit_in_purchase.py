#resources
#https://pytest-flask.readthedocs.io/en/latest/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/latest/testing/
#https://realpython.com/python-testing/#testing-flask-applications





import pytest
import os
import sys
import MySQLdb
from flask import session
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import after path modification
from server import app as create_app

# Test Constants
TEST_CART = [
    {"name": "Burger", "price": "10.00"},
    {"name": "Fries", "price": "5.00"}
]  # Total = 15 + 2 delivery = 17
TEST_CUSTOMER_ID = 1

@pytest.fixture
def app():
    """Configure test application with your Railway database details"""
    app = create_app
    app.config.update({
        "TESTING": True,
       
    })
    

    yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def setup_session(client, credits, cart=None):
    with client.session_transaction() as sess:
        sess['customer_id'] = 12  # Use your existing test customer
        sess['credits'] = credits
        sess['cart'] = cart or [
            {"name": "Burger", "price": "10.00"},
            {"name": "Fries", "price": "5.00"}
        ]
        sess['_fresh'] = True


def test_full_credit_payment(client):
    """Customer 12 has full credits, pays fully with credits (no Stripe)"""
    setup_session(client, credits=50.00)

    response = client.post(
        '/create-checkout-session-one-time',
        data={'delivery': 'yes', 'use_credits': 'yes'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Paid using credits" in response.data


def test_partial_credit_payment(client):
    """Customer 12 has some credits, rest goes to Stripe"""
    setup_session(client, credits=5.00)

    response = client.post(
        '/create-checkout-session-one-time',
        data={'delivery': 'yes', 'use_credits': 'yes'},
        follow_redirects=False
    )

    assert response.status_code == 303
    assert 'checkout.stripe.com' in response.headers.get('Location', '')


def test_stripe_payment_credits_notUse(client):
    """Customer 12 has credits but chooses not to use them"""
    setup_session(client, credits=20.00)

    response = client.post(
        '/create-checkout-session-one-time',
        data={'delivery': 'yes', 'use_credits': 'no'},
        follow_redirects=False
    )

    assert response.status_code == 303
    assert 'checkout.stripe.com' in response.headers.get('Location', '')


def test_useStripe_zero_credits(client):
    """Customer 12 has zero credits, full amount goes to Stripe"""
    setup_session(client, credits=0.00)

    response = client.post(
        '/create-checkout-session-one-time',
        data={'delivery': 'yes'},
        follow_redirects=False
    )

    assert response.status_code == 303
    assert 'checkout.stripe.com' in response.headers.get('Location', '')

def clear_test_orders(customer_id=12):
    """Delete test orders for a specific customer (ID: 12)"""
    db = MySQLdb.connect(
        host="viaduct.proxy.rlwy.net",
        user="root",
        password="WrwOIlogTwAShYIOsHGKQveeLHfVNxwy",
        db="railway",
        port=13847
    )
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM Orders WHERE customer_id = %s", (customer_id,))
        db.commit()
    finally:
        cursor.close()
        db.close()