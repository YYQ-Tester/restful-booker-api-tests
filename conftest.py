import pytest
import requests

BASE_URL='https://restful-booker.herokuapp.com'

@pytest.fixture(scope = "session")
def base_url():
    return BASE_URL

@pytest.fixture(scope = "session")
def auth_token():
    response=requests.post(
        f'{BASE_URL}/auth',timeout=10,
        json={
            "username": "admin",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    token=response.json()['token']
    return token

@pytest.fixture
def auth_headers(auth_token):
    return {"Cookie": f"token={auth_token}"}


@pytest.fixture()
def create_book(auth_token,auth_headers):
    new_book={
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(
        f'{BASE_URL}/booking',
        json=new_book
    )
    assert response.status_code == 200

    body=response.json()
    booking_id=body['bookingid']
    yield body
    del_response=requests.delete(
        f'{BASE_URL}/booking/{booking_id}',
        headers = auth_headers
    )
    assert del_response.status_code==201
