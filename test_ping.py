import requests

def test_Ping_check(base_url):
    response = requests.get(
        f'{base_url}/Ping')
    assert response.status_code == 201