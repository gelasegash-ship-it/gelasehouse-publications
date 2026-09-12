import os
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_auth_publication_flow():
    email = 'test-' + os.urandom(4).hex() + '@example.com'
    registered = client.post('/api/auth/register', json={'name':'Test User','email':email,'password':'password123'})
    assert registered.status_code == 201
    login = client.post('/api/auth/login', json={'email':email,'password':'password123'})
    assert login.status_code == 200
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    created = client.post('/api/publications', headers=headers, json={'title':'Publication test','description':'Contenu','category':'Essai'})
    assert created.status_code == 201
    assert client.get('/api/publications').status_code == 200
