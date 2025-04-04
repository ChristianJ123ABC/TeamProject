#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/

import pytest
from flask import session
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


def test_login_is_customer(client):
    response = client.post("/login", data={
        "email": "geh@gmail.com",
        "password": "123",

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/customer'

def test_login_is_not_customer(client):
    response = client.post("/login", data={
        "email": "boy@gmail.com",
        "password": "123",

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/driver' or '/foodOwner'