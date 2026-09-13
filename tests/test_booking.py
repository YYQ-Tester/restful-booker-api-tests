import pytest
from jsonschema import validate

from tests.schemas import BOOKING_SCHEMA,BOOK_ID_SCHEMAS


def test_get_all_booking_id(base_url,api_session):
    response = api_session.get(
        f'{base_url}/booking')
    body = response.json()
    print(body)
    assert response.status_code == 200
    #assert isinstance(body, list), f'expect a list, got a {type(body)}'
    validate(instance = body, schema = BOOK_ID_SCHEMAS)

    assert len(body) > 0, f'expect at least one book, got empty list'
    #assert 'bookingid' in body[0], f'expect "bookingid" key, got {body[0]}'
    #assert isinstance(body[0]['bookingid'], int), f"expect bookingid to be integer, got{type(body[0]['bookingid'])}"


@pytest.mark.parametrize('params', [
    {"firstname": "dljnfnd", "lastname": "fdsmpfn"},  # false name
    {"firstname": "1122", "lastname": "!@$"},  # special charactor
    {"firstname": " ", "lastname": " "}    # empty name
])  # decorator for multi similar cases
def test_get_by_name_not_found(base_url,params,api_session):
    response = api_session.get(
        f'{base_url}/booking',
        params = params
    )
    body = response.json()
    assert response.status_code == 200
    #assert isinstance(body, list) , f'expect a list, got a {type(body)}'
    validate(instance = body, schema = BOOK_ID_SCHEMAS)
    assert len(body) == 0, f'expect a empty list, got {len(body)} data'


def test_get_by_check_date(base_url,api_session):
    response = api_session.get(
        f'{base_url}/booking?checkin=2004-03-13&checkout=2014-05-21'
    )
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body, list), f'expect a list, got a {type(body)}'


def test_get_by_booking_id(base_url,create_book,api_session):
    body = create_book
    book_id = body['bookingid']
    response = api_session.get(
        f'{base_url}/booking/{book_id}')
    body = response.json()
    assert response.status_code == 200
    #assert isinstance(body, dict), f'expect a dictionary, got a {type(body)}'
    validate(instance = body, schema = BOOKING_SCHEMA)
    # assert 'firstname' in body
    # assert 'bookingdates' in body
    # assert isinstance(body['totalprice'], (int, float))
    # assert isinstance(body['depositpaid'], bool)


def test_get_by_booking_nonexistence_id(base_url,api_session):
    response = api_session.get(
        f'{base_url}/booking/888888888')
    assert response.status_code == 404
    assert 'Not Found' in response.text


def test_create_book(base_url,api_session,create_book):
    body = create_book
    booking_id = body['bookingid']
    #assert isinstance(body, dict), f'expect a dictionary, got a {type(body)}'
    validate(instance = body["booking"], schema = BOOKING_SCHEMA)
    create_response = api_session.get(
        f'{base_url}/booking/{booking_id}'
    )
    assert create_response.json()['firstname'] == 'James'


def test_update_book(base_url, api_session, create_book):
    body = create_book
    booking_id = body['bookingid']
    update_book = {
        "firstname": "Jerry",
        "lastname": "Black",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = api_session.put(
        f'{base_url}/booking/{booking_id}',
        json = update_book
    )
    assert response.status_code == 200
    assert response.json()['firstname'] == 'Jerry'


def test_partial_update_book(base_url, api_session, create_book):
    body = create_book
    booking_id = body['bookingid']
    update_book = {
        "firstname": "Jenny",
        "lastname": "Pink"
    }
    response = api_session.patch(
        f'{base_url}/booking/{booking_id}',
        json = update_book
    )
    assert response.status_code == 200
    assert response.json()['firstname'] == 'Jenny'
    assert response.json()['lastname'] == 'Pink'


def test_delete_book(base_url, api_session):
    new_book = {
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
        f'{base_url}/booking',
        json = new_book
    )
    assert response.status_code == 200
    booking_id=response.json()['bookingid']

    response = api_session.delete(
        f'{base_url}/booking/{booking_id}'
    )
    assert response.status_code == 201

    #query after deleting to confirm deleted
    query_response = api_session.get(
        f'{base_url}/booking/{booking_id}'
    )
    assert query_response.status_code == 404
    assert 'Not Found' in query_response.text
