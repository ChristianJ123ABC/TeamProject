
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

@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_create_customer_account(client):
    response = client.post("/register", data={
        "full_name": "cj",
        "password": "123",
        "email": "customertest@gmail.com",
        "role": "customer",
        "phone_number": "0831029322",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Customer account" in response.data
    assert response.request.path == '/register'

@pytest.mark.xfail(reason="not customer account")
def test_is_not_customer_account(client):
    response = client.post("/register", data={
        "full_name": "cj",
        "password": "123",
        "email": "foodtest@gmail.com",
        "role": "food_owner",
        "phone_number": "0831029322",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Customer account" in response.data
    assert response.request.path == '/register'


def test_invalid_email_format(client):
    response = client.post("/register", data={
        "full_name": "cj",
        "password": "123",
        "email": "invalidemail",
        "role": "customer",
        "phone_number": "0831029322",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Email is in an invalid format" in response.data
    assert response.request.path == '/register'


def test_email_already_exists(client):
    response = client.post("/register", data={
        "full_name": "cj",
        "password": "123",
        "email": "geh@gmail.com",
        "role": "customer",
        "phone_number": "0831029322",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Email is already registered" in response.data
    assert response.request.path == '/register'


def test_phone_number_already_exists(client):
    response = client.post("/register", data={
        "full_name": "cj2",
        "password": "123",
        "email": "customertest1@gmail.com",
        "role": "customer",
        "phone_number": "0851064159",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"An account with this phone number already exists" in response.data
    assert response.request.path == '/register'

def test_phone_number_out_of_range(client):
    response = client.post("/register", data={
        "full_name": "cj2",
        "password": "123",
        "email": "customertest2@gmail.com",
        "role": "customer",
        "phone_number": "123",
        "address": "my house"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Phone number out of range" in response.data
    assert response.request.path == '/register'





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

    
    cursor.execute("DELETE FROM Users WHERE email = %s", ("customertest@gmail.com",))
    cursor.execute("DELETE FROM Users WHERE email = %s", ("customertest1@gmail.com",))
    cursor.execute("DELETE FROM Users WHERE email = %s", ("customertest2@gmail.com",))
    cursor.execute("DELETE FROM Users WHERE email = %s", ("foodtest@gmail.com",))

    cursor.execute("DELETE FROM Users WHERE email = %s", ("drivertest@gmail.com",))
    cursor.execute("DELETE FROM Customers WHERE phone_number = %s", ("831029322",))

    
    cursor.connection.commit()  
    cursor.close()  
