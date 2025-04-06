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


def test_promotion_is_valid_image(client):
    with client.session_transaction() as session:
        session["user_id"] = 6 #Food Promoter ID with a subscription

    response = client.post("/postPromotion", data={
        "image": (resources / "pizza.jpg").open("rb"),
        "caption": "123",

    },follow_redirects = True) #Used to implement redirect responses

    
    assert response.status_code == 200
    assert b"Image uploaded successfully" in response.data
    assert response.request.path == '/postPromotion'
    



def test_promotion_is_invalid_image(client):
    with client.session_transaction() as session:
        session["user_id"] = 6 #Food Promoter ID with a subscription

    response = client.post("/postPromotion", data={
        "image": (resources / "false.txt").open("rb"),
        "caption": "123",

    },follow_redirects = True) #Used to implement redirect responses

    
    assert response.status_code == 200
    assert b"Invalid image type, use the following image extensions: .JPG, .PNG or .JPEG" in response.data
    assert response.request.path == '/postPromotion'



def test_promotion_image_not_uploaded(client):
    with client.session_transaction() as session:
        session["user_id"] = 6 #Food Promoter ID with a subscription

    response = client.post("/postPromotion", data={ 
        "image": "",
        "caption": "123",

    },follow_redirects = True) #Used to implement redirect responses

    
    assert response.status_code == 400
    assert response.request.path == '/postPromotion'

    
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

    
    cursor.execute("DELETE FROM Promotions WHERE caption = %s", ('123',))
    cursor.connection.commit()  
    cursor.close()  

