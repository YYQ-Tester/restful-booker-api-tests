from functools import partial
import pytest
import requests


BASE_URL='https://restful-booker.herokuapp.com'
TIMEOUT = 10

@pytest.fixture(scope = "session")
def base_url():
    return BASE_URL

@pytest.fixture(scope = "session")
def auth_token():
    response=requests.post(
        f'{BASE_URL}/auth',timeout=TIMEOUT,
        json={
            "username": "admin",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    token=response.json()['token']
    return token

# @pytest.fixture
# def auth_headers(auth_token):
#     return {"Cookie": f"token={auth_token}"}

#encapsulate headers and timeout
@pytest.fixture
def api_session(auth_token):
    # wrap it with headers and timeout
    session = requests.session()
    session.headers.update({"Cookie": f"token={auth_token}"})
    # add timeout to every request function
    session.get = partial(session.get,timeout=TIMEOUT)
    session.put = partial(session.put, timeout = TIMEOUT)
    session.post = partial(session.post, timeout = TIMEOUT)
    session.patch = partial(session.patch, timeout = TIMEOUT)
    session.delete = partial(session.delete, timeout = TIMEOUT)
    return session

@pytest.fixture()
def create_book(api_session):
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

    response = api_session.post(
        f'{BASE_URL}/booking',
        json=new_book
    )
    assert response.status_code == 200

    body=response.json()
    booking_id=body['bookingid']
    yield body
    del_response=api_session.delete(
        f'{BASE_URL}/booking/{booking_id}'
    )
    assert del_response.status_code==201
