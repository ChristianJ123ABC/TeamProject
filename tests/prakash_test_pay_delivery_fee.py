#resources
#https://pytest-flask.readthedocs.io/en/latest/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/latest/testing/
#https://realpython.com/python-testing/#testing-flask-applications


import pytest
import os
import sys
from server import mysql
# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import after path modification
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


@pytest.fixture
def client_with_cart(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['cart'] = [
                {"name": "Item A", "price": "10.00"},
                {"name": "Item B", "price": "5.00"},
            ]
            sess['credits'] = 0.0
            sess['customer_id'] = 12
        yield client




def test_user_declines_delivery_fee(client):
    with client.session_transaction() as sess:
        sess['cart'] = [{'name': 'Bread', 'price': 3.5}]
    
    response = client.post('/create-checkout-session-one-time', data={'delivery': 'no'})
    
    assert response.status_code == 302  # Redirect
    assert '/Cpayment' in response.location

def test_user_has_empty_cart(client):
    with client.session_transaction() as sess:
        sess['cart'] = []
    
    response = client.post('/create-checkout-session-one-time', data={'delivery': 'yes'})
    
    assert response.status_code == 302
    assert '/Cpayment' in response.location

def test_user_accepts_delivery_fee_and_has_cart(client):
    with client.session_transaction() as sess:
        sess['cart'] = [{'name': 'Milk', 'price': 2.0}]
    
    response = client.post('/create-checkout-session-one-time', data={'delivery': 'yes'})
    
    # Should redirect to Stripe (3xx)
    assert response.status_code == 303
    assert "https://checkout.stripe.com/" in response.location


def cleanup_test_data(customer_id):
    cursor = mysql.connection.cursor()

    # Delete test orders
    cursor.execute("DELETE FROM Orders WHERE customer_id = %s", (customer_id,))
    
    # Reset user credits and status
    cursor.execute("UPDATE Customers SET credits = 0, status = '' WHERE customer_id = %s", (customer_id,))
    
    mysql.connection.commit()
    cursor.close()
