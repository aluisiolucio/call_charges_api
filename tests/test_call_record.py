from datetime import datetime

import pytest

from call_charges_api.domain.entities.call_record import CallRecord, CallType


def test_create_start_record_with_valid_data():
    record = CallRecord(
        call_id=1,
        call_type=CallType.START,
        timestamp=datetime.now(),
        source='1234567890',
        destination='0987654321',
    )
    assert record.is_start()
    assert record.source == '1234567890'
    assert record.destination == '0987654321'


def test_create_end_record_with_valid_data():
    record = CallRecord(
        call_id=2, call_type=CallType.END, timestamp=datetime.now()
    )
    assert record.is_end()
    assert record.source is None
    assert record.destination is None


def test_start_record_missing_source_or_destination_raises_error():
    with pytest.raises(
        ValueError,
        match='Source and destination are required for a start call record.',
    ):
        CallRecord(
            call_id=3,
            call_type=CallType.START,
            timestamp=datetime.now(),
            source='1234567890',
        )


def test_end_record_with_source_or_destination_raises_error():
    with pytest.raises(
        ValueError,
        match='Source and destination should not '
        'be provided for an end call record.',
    ):
        CallRecord(
            call_id=4,
            call_type=CallType.END,
            timestamp=datetime.now(),
            source='1234567890',
            destination='0987654321',
        )
