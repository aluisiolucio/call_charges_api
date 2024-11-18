from http import HTTPStatus

import pytest


@pytest.fixture
def valid_start_record():
    return {
        'call_id': 1,
        'type': 'start',
        'timestamp': '2023-11-01T10:00:00',
        'source': '1234567890',
        'destination': '0987654321',
    }


@pytest.fixture
def valid_end_record():
    return {'call_id': 1, 'type': 'end', 'timestamp': '2023-11-01T10:30:00'}


@pytest.fixture
def mock_phone_bill_response():
    return {
        'bills': [
            {
                "phone_number": "1234567890",
                "reference_period": "11/2023",
                "total_amount": "R$ 3,06",
                "call_records": [
                    {
                        "destination": "0987654321",
                        "call_start_date": "2023-11-01",
                        "call_start_time": "10:00:00",
                        "call_duration": "0h30m0s",
                        "call_price": "R$ 3,06",
                    }
                ],
            }
        ]
    }


def test_get_phone_bill_success(
    client,
    mock_phone_bill_response,
    valid_start_record,
    valid_end_record,
):
    response = client.put('api/v1/call_records', json=valid_start_record)
    assert response.status_code == HTTPStatus.CREATED

    response = client.put('api/v1/call_records', json=valid_end_record)
    assert response.status_code == HTTPStatus.CREATED

    response = client.get(
        'api/v1/phone_bill',
        params={'phone_number': '1234567890', 'reference_period': '11/2023'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == mock_phone_bill_response


def test_get_phone_bill_invalid_phone_number(client):
    response = client.get(
        'api/v1/phone_bill',
        params={'phone_number': '123456789', 'reference_period': '11/2023'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'bills': []}


def test_get_phone_bill_invalid_reference_period(client):
    response = client.get(
        'api/v1/phone_bill',
        params={'phone_number': '1234567890', 'reference_period': '11'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'bills': []}


def test_get_phone_bill_without_reference_period(client):
    response = client.get(
        'api/v1/phone_bill', params={'phone_number': '1234567890'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'bills': []}


def test_get_phone_bill_without_phone_number(client):
    response = client.get(
        'api/v1/phone_bill', params={'reference_period': '11/2023'}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
