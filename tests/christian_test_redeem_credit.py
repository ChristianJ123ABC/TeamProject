#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
##https://docs.pytest.org/en/7.1.x/how-to/skipping.html

#CHRISTIAN'S TEST CASE
#
#

import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb
resources = Path(__file__).parent.parent / "tests" / "resources" #Folder with designated files to test

@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app



@pytest.fixture()
def client(app):
    return app.test_client()

def test_redeem_verified_credits(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 #Customer test id
        session["pending_credits"] = 0.00
        session["credits"] = 10.00
        session["status"] = "verified"
    response = client.get("/redeemCredits", follow_redirects = True)
    assert response.status_code == 200

    assert b"3-5 business days" in response.data

    with client.session_transaction() as session:
        session["customer_id"] = 12 #Customer test id
        session["pending_credits"] = 0.00
        session["credits"] = 0.00
        session["status"] = ""



def test_redeem_unverified_credits(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 #Customer test id
        session["pending_credits"] = 10.00
        session["credits"] = 0.00
        session["status"] = "pending"
    response = client.get("/redeemCredits", follow_redirects = True)

    assert response.status_code == 200
    assert b"You cannot use your credits until they are verified" in response.data

def test_redeem_no_credits(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 #Customer test id
        session["pending_credits"] = 0.00
        session["credits"] = 0.00
        session["status"] = ""
    response = client.get("/redeemCredits", follow_redirects = True)

    assert response.status_code == 200
    assert b"You cannot redeem any credits since you do not have any" in response.data



    
