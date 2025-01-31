from datetime import datetime, time

import pytest

from call_charges_api.domain.entities.call_record import CallRecord, CallType
from call_charges_api.domain.entities.phone_bill import (
    PhoneBill,
    PhoneBillRecords,
)


@pytest.fixture
def start_call_record():
    return CallRecord(
        call_id=1,
        call_type=CallType.START,
        timestamp=datetime(2023, 11, 1, 10, 0),
        source='1234567890',
        destination='0987654321',
    )


@pytest.fixture
def end_call_record():
    return CallRecord(
        call_id=1,
        call_type=CallType.END,
        timestamp=datetime(2023, 11, 1, 10, 30),
    )


@pytest.fixture
def phone_bill():
    return PhoneBill(phone_number='1234567890')


def test_calculate_call_duration(phone_bill):
    start_time = datetime(2023, 11, 1, 10, 0)
    end_time = datetime(2023, 11, 1, 10, 45)
    duration = phone_bill._PhoneBill__calculate_call_duration(
        start_time, end_time
    )
    assert duration == '0h45m0s'


def test_calculate_call_cost(phone_bill):
    start_time = datetime(2023, 11, 1, 21, 57)
    end_time = datetime(2023, 11, 1, 22, 5)
    cost = phone_bill._PhoneBill__calculate_call_cost(start_time, end_time)
    assert cost == 'R$ 0,54'


def test_calculate_call_records(
    phone_bill, start_call_record, end_call_record
):
    call_records_pair = (start_call_record, end_call_record)
    record = phone_bill.calculate_call_records(call_records_pair)

    assert isinstance(record, PhoneBillRecords)
    assert record.destination == '0987654321'
    assert record.call_start_date == datetime(2023, 11, 1).date()
    assert record.call_start_time == time(10, 0)
    assert record.duration == '0h30m0s'
    assert record.price == 'R$ 3,06'


def test_formatted_total_amount(phone_bill):
    phone_bill.total_amount = 123.45
    formatted = phone_bill.formatted_total_amount
    assert formatted == 'R$ 123,45'


def test_define_period(phone_bill):
    phone_bill.reference_period = None
    phone_bill.define_period()
    current_date = datetime.now()
    DECEMBER = 12
    last_month = current_date.month - 1 if current_date.month > 1 else DECEMBER
    year = (
        current_date.year if last_month != DECEMBER else current_date.year - 1
    )
    expected_period = f'{last_month}/{year}'
    assert phone_bill.reference_period == expected_period


def test_calculate_minutes_between(phone_bill):
    start_time = datetime(2023, 11, 1, 21, 55)
    end_time = datetime(2023, 11, 1, 22, 5)
    expected_minutes = 4
    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )
    assert minutes == expected_minutes


def test_calculate_minutes_between_trucate(phone_bill):
    start_time = datetime.fromisoformat('2017-12-11T15:07:13Z')
    end_time = datetime.fromisoformat('2017-12-11T15:14:56Z')

    expected_minutes = 7
    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )
    assert minutes == expected_minutes


def test_calculate_minutes_between_different_days(phone_bill):
    start_time = datetime.fromisoformat('2018-02-28T21:57:13Z')
    end_time = datetime.fromisoformat('2018-03-01T22:10:56Z')

    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )

    expected_minutes = 960
    assert minutes == expected_minutes


def test_single_day_fully_diurnal(phone_bill):
    start_time = datetime.fromisoformat('2023-11-01T06:00:00+00:00')
    end_time = datetime.fromisoformat('2023-11-01T22:00:00+00:00')

    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )

    expected_minutes = 958
    assert minutes == expected_minutes


def test_no_minutes_in_nighttime(phone_bill):
    start_time = datetime.fromisoformat('2023-11-01T23:00:00+00:00')
    end_time = datetime.fromisoformat('2023-11-02T05:59:59+00:00')

    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )

    expected_minutes = 0
    assert minutes == expected_minutes


def test_crossing_midnight(phone_bill):
    start_time = datetime.fromisoformat('2023-11-01T21:55:00+00:00')
    end_time = datetime.fromisoformat('2023-11-02T06:05:00+00:00')

    minutes = phone_bill._PhoneBill__calculate_minutes_between(
        start_time, end_time
    )

    expected_minutes = 8
    assert minutes == expected_minutes
