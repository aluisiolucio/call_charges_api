from datetime import datetime

import pytest

from call_charges_api.domain.entities.call_record import CallRecord, CallType
from call_charges_api.domain.errors.exceptions import (
    BusinessException,
    InvalidPhoneNumberException,
)


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
    record = CallRecord(
        call_id=3,
        call_type=CallType.START,
        timestamp=datetime.now(),
        source='1234567890',
    )

    with pytest.raises(
        BusinessException,
        match='Source and destination are required for a start call record.',
    ):
        record.validate_call_record()


def test_end_record_with_source_or_destination():
    record = CallRecord(
        call_id=4,
        call_type=CallType.END,
        timestamp=datetime.now(),
        source='1234567890',
        destination='0987654321',
    )

    record.validate_call_record()

    assert record.is_end()
    assert record.source is None
    assert record.destination is None


def test_invalid_source_phone_number_raises_error():
    record = CallRecord(
        call_id=5,
        call_type=CallType.START,
        timestamp=datetime.now(),
        source='123456789',
        destination='19996917471',
    )
    record.validate_call_record()

    with pytest.raises(
        InvalidPhoneNumberException,
        match="The phone number '123456789' is invalid.",
    ):
        record.validate_phone_numbers()


def test_invalid_destination_phone_number_raises_error():
    record = CallRecord(
        call_id=6,
        call_type=CallType.START,
        timestamp=datetime.now(),
        source='19996917471',
        destination='098765432',
    )
    record.validate_call_record()

    with pytest.raises(
        InvalidPhoneNumberException,
        match="The phone number '098765432' is invalid.",
    ):
        record.validate_phone_numbers()
