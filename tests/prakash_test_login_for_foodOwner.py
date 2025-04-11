#resources
#https://pytest-flask.readthedocs.io/en/latest/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/latest/testing/
#https://realpython.com/python-testing/#testing-flask-applications


import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


def test_login_is_foodOwner(client):
    response = client.post("/login", data={
        "email": "3456@gmail.com",
        "password": "1234",

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert response.request.path == '/foodOwner'


def test_login_is_not_foodOwner(client):
    response = client.post("/login", data={
        "email": "1234@gmail.com",
        "password": "1234",

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/customer' or '/driver'