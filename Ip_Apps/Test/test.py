import requests

data = {
    'student': {'age': 32, 'name': 'ali', 'grades': [14, 18]}
}
client_ip = {'client_ip': '127.0.0.1'}
resp_test_with_json = data | client_ip
resp_test_empty_json = client_ip
resp_test_empty_body = client_ip


def test_with_json():
    try:
        resp = requests.post(url='http://127.0.0.1/api/', json=data)
        assert resp.json() == resp_test_with_json
        assert resp.status_code == 200
    except:
        assert resp.status_code == 502


def test_empty_json():
    try:
        resp = requests.post(url='http://127.0.0.1/api/', json=dict())
        assert resp.json() == resp_test_empty_json
        assert resp.status_code == 200
    except:
        assert resp.status_code == 502


def test_empty_body():
    try:
        resp = requests.post(url='http://127.0.0.1/api/')
        assert resp.json() == resp_test_empty_body
        assert resp.status_code == 200
    except:
        assert resp.status_code == 502


def test_get():
    try:
        resp = requests.get(url="http://127.0.0.1/api/")
        assert resp.status_code == 405
    except:
        assert resp.status_code == 502
