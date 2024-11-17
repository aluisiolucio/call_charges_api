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


def test_create_start_record(client, valid_start_record):
    response = client.put('api/v1/call_records', json=valid_start_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')


def test_create_pair(client, valid_start_record, valid_end_record):
    response = client.put('api/v1/call_records', json=valid_start_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put('api/v1/call_records', json=valid_end_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')


def test_create_end_record_without_start(client, valid_end_record):
    response = client.put('api/v1/call_records', json=valid_end_record)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail').get('message') == (
        'Start call record with ID 1 was not found.'
    )


def test_invalid_record_missing_fields(client):
    invalid_record = {'id': 1, 'type': 'start'}
    response = client.put('api/v1/call_records', json=invalid_record)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_record_with_wrong_data_types(client):
    invalid_record = {
        'call_id': 'not-an-integer',
        'type': 'start',
        'timestamp': 'not-a-timestamp',
        'source': 1234567890,
        'destination': '0987654321',
    }
    response = client.put('api/v1/call_records', json=invalid_record)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_record_with_wrong_call_type(client):
    invalid_record = {
        'call_id': 1,
        'type': 'wrong-type',
        'timestamp': '2023-11-01T10:00:00',
        'source': '1234567890',
        'destination': '0987654321',
    }
    response = client.put('api/v1/call_records', json=invalid_record)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_repeated_start_record(client, valid_start_record):
    response = client.put('api/v1/call_records', json=valid_start_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == valid_start_record.get(
        'timestamp'
    )
    assert response.json().get('source') == valid_start_record.get('source')
    assert response.json().get('destination') == valid_start_record.get(
        'destination'
    )

    valid_start_record_repeated = {
        'call_id': 1,
        'type': 'start',
        'timestamp': '2023-11-01T10:40:00',
        'source': '0987654321',
        'destination': '0987654321',
    }

    response = client.put(
        'api/v1/call_records', json=valid_start_record_repeated
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == valid_start_record_repeated.get(
        'timestamp'
    )
    assert response.json().get('source') == valid_start_record_repeated.get(
        'source'
    )
    assert response.json().get(
        'destination'
    ) == valid_start_record_repeated.get('destination')


def test_create_repeated_end_record(
    client, valid_start_record, valid_end_record
):
    response = client.put('api/v1/call_records', json=valid_start_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == valid_start_record.get(
        'timestamp'
    )
    assert response.json().get('source') == valid_start_record.get('source')
    assert response.json().get('destination') == valid_start_record.get(
        'destination'
    )

    response = client.put('api/v1/call_records', json=valid_end_record)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == valid_end_record.get(
        'timestamp'
    )

    valid_end_record_repeated = {
        'call_id': 1,
        'type': 'end',
        'timestamp': '2023-11-01T11:00:00',
    }

    response = client.put(
        'api/v1/call_records', json=valid_end_record_repeated
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == valid_end_record_repeated.get(
        'timestamp'
    )
