
def test_ping_check(base_url,api_session):
    response = api_session.get(
        f'{base_url}/Ping')
    assert response.status_code == 201