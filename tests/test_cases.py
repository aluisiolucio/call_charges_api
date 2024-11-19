from http import HTTPStatus

import pytest

call_records = [
    {
        'call_id': 70,
        'start': '2016-02-29T12:00:00Z',
        'end': '2016-02-29T14:00:00Z',
    },
    {
        'call_id': 71,
        'start': '2017-12-11T15:07:13Z',
        'end': '2017-12-11T15:14:56Z',
    },
    {
        'call_id': 72,
        'start': '2017-12-12T22:47:56Z',
        'end': '2017-12-12T22:50:56Z',
    },
    {
        'call_id': 73,
        'start': '2017-12-12T21:57:13Z',
        'end': '2017-12-12T22:10:56Z',
    },
    {
        'call_id': 74,
        'start': '2017-12-12T04:57:13Z',
        'end': '2017-12-12T06:10:56Z',
    },
    {
        'call_id': 75,
        'start': '2017-12-13T21:57:13Z',
        'end': '2017-12-14T22:10:56Z',
    },
    {
        'call_id': 76,
        'start': '2017-12-12T15:07:58Z',
        'end': '2017-12-12T15:12:56Z',
    },
    {
        'call_id': 77,
        'start': '2018-02-28T21:57:13Z',
        'end': '2018-03-01T22:10:56Z',
    },
]


@pytest.mark.parametrize('record', call_records)
def test_create_call_records(client, token, record):
    start_response = client.put(
        '/api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'start',
            'timestamp': record['start'],
            'call_id': record['call_id'],
            'source': '99988526423',
            'destination': '9933468278',
        },
    )
    assert start_response.status_code == HTTPStatus.CREATED
    assert start_response.json()['type'] == 'start'
    assert start_response.json()['call_id'] == record['call_id']

    end_response = client.put(
        '/api/v1/call_records',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'end',
            'timestamp': record['end'],
            'call_id': record['call_id'],
        },
    )
    assert end_response.status_code == HTTPStatus.CREATED
    assert end_response.json()['type'] == 'end'
    assert end_response.json()['call_id'] == record['call_id']


@pytest.mark.parametrize(
    ('phone_number', 'reference_period', 'expected_calls'),
    [
        ('99988526423', '02/2016', 1),
        ('99988526423', '12/2017', 6),
        ('99988526423', '03/2018', 1),
    ],
)
def test_phone_bill(
    client, token, phone_number, reference_period, expected_calls
):
    call_records_to_create = [
        record
        for record in call_records
        if record['start'].startswith(reference_period.split('/')[1])
    ]

    for record in call_records_to_create:
        client.put(
            '/api/v1/call_records',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'type': 'start',
                'timestamp': record['start'],
                'call_id': record['call_id'],
                'source': phone_number,
                'destination': '9933468278',
            },
        )
        client.put(
            '/api/v1/call_records',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'type': 'end',
                'timestamp': record['end'],
                'call_id': record['call_id'],
            },
        )

    response = client.get(
        '/api/v1/phone_bill',
        headers={'Authorization': f'Bearer {token}'},
        params={
            'phone_number': phone_number,
            'reference_period': reference_period,
        },
    )
    assert response.status_code == HTTPStatus.OK

    json_response = response.json()
    assert 'bills' in json_response
    assert isinstance(json_response['bills'], list)
    assert len(json_response['bills'][0]['call_records']) == expected_calls
