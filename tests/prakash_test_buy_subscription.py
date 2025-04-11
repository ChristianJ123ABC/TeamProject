#resources
#https://pytest-flask.readthedocs.io/en/latest/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/latest/testing/
#https://realpython.com/python-testing/#testing-flask-applications





import pytest
import sys
import os
import MySQLdb
from datetime import datetime, timedelta
from server import app as create_app  # Make sure this matches your Flask app file name

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_key"
    })
    yield create_app


#assigning values to login as foodOwner/promoter
@pytest.fixture()
def client_with_logged_in_promoter(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["user_id"] = 10
            sess["email"] = "3456@gmail.com"
            sess["role"] = "food_owner"
        yield client

#checks if the foodOwner is logged in 
def test_promoter_session(client_with_logged_in_promoter):
    with client_with_logged_in_promoter.session_transaction() as sess:
        assert sess["user_id"] == 10
        assert sess["email"] == "3456@gmail.com"
        assert sess["role"] == "food_owner"

def test_promoter_buys_subscription(client_with_logged_in_promoter):

    # Manually insert a fake Stripe checkout session into DB like the app would do
    db = MySQLdb.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='WrwOIlogTwAShYIOsHGKQveeLHfVNxwy',
        db='railway',
        port=13847
    )
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Subscriptions 
        (promoter_id, stripe_subscription_id, subscription_start_date, subscription_end_date, next_due_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        10,
        'test_checkout_session_id',
        datetime.now(),
        datetime.now() + timedelta(days=30),
        datetime.now() + timedelta(days=30),
        'active'
    ))
    db.commit()
    cursor.close()
    db.close()

    # Access the subscription page to verify that the subscription appears
    response = client_with_logged_in_promoter.get('/Subscribe')
    
    assert response.status_code == 200
    assert b'test_checkout_session_id' in response.data  # Check if subscription shows in HTML

# Clean up any inserted test subscriptions after test session
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_subscriptions():
    yield  # Run the test(s) first
    db = MySQLdb.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='WrwOIlogTwAShYIOsHGKQveeLHfVNxwy',
        db='railway',
        port=13847
    )
    cursor = db.cursor()
    cursor.execute("DELETE FROM Subscriptions WHERE promoter_id = %s", (10,))
    db.commit()
    cursor.close()
    db.close()