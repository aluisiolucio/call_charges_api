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


def test_create_start_record(client, token, valid_start_record):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')


def test_create_pair(client, token, valid_start_record, valid_end_record):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')


def test_create_end_record_without_start(client, token, valid_end_record):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get('detail').get('message') == (
        'Start call record with ID 1 was not found.'
    )


def test_invalid_record_missing_fields(client, token):
    invalid_record = {'id': 1, 'type': 'start'}
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=invalid_record,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_record_with_wrong_data_types(client, token):
    invalid_record = {
        'call_id': 'not-an-integer',
        'type': 'start',
        'timestamp': 'not-a-timestamp',
        'source': 1234567890,
        'destination': '0987654321',
    }
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=invalid_record,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_invalid_record_with_wrong_call_type(client, token):
    invalid_record = {
        'call_id': 1,
        'type': 'wrong-type',
        'timestamp': '2023-11-01T10:00:00',
        'source': '1234567890',
        'destination': '0987654321',
    }
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=invalid_record,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_repeated_start_record(client, token, valid_start_record):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    id = response.json().get('id')

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
        'id': id,
        'call_id': 1,
        'type': 'start',
        'timestamp': '2023-11-01T10:40:00',
        'source': '0987654321',
        'destination': '1234567890',
    }

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record_repeated,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == id
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == valid_start_record_repeated.get(
        'timestamp'
    )
    assert response.json().get('source') == valid_start_record.get('source')
    assert response.json().get('destination') == valid_start_record.get(
        'destination'
    )


def test_create_repeated_end_record(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
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

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == valid_end_record.get(
        'timestamp'
    )

    valid_end_record_repeated = {
        'id': id,
        'call_id': 1,
        'type': 'end',
        'timestamp': '2023-11-01T11:00:00',
    }

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record_repeated,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == id
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == valid_end_record_repeated.get(
        'timestamp'
    )


def test_create_multiple_records_to_subscriber(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')

    valid_start_record['call_id'] = 2
    valid_end_record['call_id'] = 2

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')


def test_create_multiple_records_to_subscriber_out_of_order(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    valid_start_record['call_id'] = 2

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')

    valid_end_record['call_id'] = 2

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')


def test_update_start_record(client, token, valid_start_record):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    valid_start_record['id'] = id
    valid_start_record['timestamp'] = '2023-11-01T10:40:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == id
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == '2023-11-01T10:40:00'


def test_update_end_record(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')

    valid_end_record['id'] = id
    valid_end_record['timestamp'] = '2023-11-01T11:00:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == id
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == '2023-11-01T11:00:00'


def test_update_end_record_with_wrong_id(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    start_id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')

    valid_end_record['id'] = start_id
    valid_end_record['timestamp'] = '2023-11-01T11:00:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == id
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == '2023-11-01T11:00:00'


def test_update_record_without_id(
    client, token, valid_start_record, valid_end_record
):
    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    start_id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')

    valid_start_record['timestamp'] = '2023-11-01T10:40:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_start_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == start_id
    assert response.json().get('call_id') == valid_start_record.get('call_id')
    assert response.json().get('type') == valid_start_record.get('type')
    assert response.json().get('timestamp') == '2023-11-01T10:40:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    end_id = response.json().get('id')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')

    valid_end_record['timestamp'] = '2023-11-01T11:00:00'

    response = client.put(
        'api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json=valid_end_record,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('id') == end_id
    assert response.json().get('call_id') == valid_end_record.get('call_id')
    assert response.json().get('type') == valid_end_record.get('type')
    assert response.json().get('timestamp') == '2023-11-01T11:00:00'
