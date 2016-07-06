import json


def authenticate(client, user):
    payload = {'email': user.email, 'password': 'testpassword'}
    login = client.post(
        '/api/login', data=json.dumps(payload),
        content_type='application/json',
    )
    assert(login.status_code == 200), 'LOGIN FAILURE'
