#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python

#CHRISTIAN'S TEST CASE
#
#

import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb


@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_deposit_more_than_100_bottles(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 #Customer test id
        session["pending_credits"] = 0.00
        session["credits"] = 0.00
        session["status"] = ""
    response = client.post("/deposit", data={
        "bottles": "111"


    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert b"Please deposit 100 bottles or less at a time" in response.data
    assert response.request.path == '/deposit'


def test_deposit_valid_num_of_bottles(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 
        session["pending_credits"] = 0.00
        session["credits"] = 0.00
        session["status"] = ""
    response = client.post("/deposit", data={
        "bottles": "99"


    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert b"They must be verified first in order to use them" in response.data
    assert response.request.path == '/deposit'

def test_deposit_less_than_1_bottle(client):
    with client.session_transaction() as session:
        session["customer_id"] = 12 
        session["pending_credits"] = 0.00
        session["credits"] = 0.00
        session["status"] = ""
    response = client.post("/deposit", data={
        "bottles": "-10"


    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert b"You cannot enter less than 1 bottle" in response.data
    assert response.request.path == '/deposit'



@pytest.fixture(scope="session", autouse=True)
def wipe_db():
    yield #Executes the function
    database = MySQLdb.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='WrwOIlogTwAShYIOsHGKQveeLHfVNxwy',
        db='railway',
        port=13847
    )
    cursor = database.cursor()

    
    cursor.execute("UPDATE Customers SET pending_credits = 0  WHERE customer_id = 12")
    cursor.execute("UPDATE Customers SET status = ''  WHERE customer_id = 12")
    cursor.connection.commit()  
    cursor.close()  

