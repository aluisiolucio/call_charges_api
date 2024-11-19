from http import HTTPStatus


def test_sign_up(client):
    response = client.post(
        '/api/v1/auth/sign_up',
        json={
            'username': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'username' in response.json()


def test_sign_in(client):
    response = client.post(
        '/api/v1/auth/sign_up',
        json={
            'username': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/api/v1/auth/sign_in',
        data={'username': 'alice@example.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_refresh_token(client, token):
    response = client.post(
        '/api/v1/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'
