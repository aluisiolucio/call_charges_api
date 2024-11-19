from http import HTTPStatus


def test_sign_up(client):
    response = client.post(
        '/register',
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
        '/register',
        json={
            'username': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/token',
        data={'username': 'alice@example.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
