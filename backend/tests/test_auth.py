import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import decode_access_token

client = TestClient(app)

def test_login_and_decode():
    # ensure demo creds
    os.environ['DEMO_USER'] = 'testuser'
    os.environ['DEMO_PASS'] = 'testpass'
    resp = client.post('/api/v1/login', json={'username': 'testuser', 'password': 'testpass'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'access_token' in data
    token = data['access_token']
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get('sub') == 'testuser'
