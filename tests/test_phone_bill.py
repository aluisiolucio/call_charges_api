from datetime import datetime

import pytest

from call_charges_api.domain.entities.call_record import CallRecord, CallType
from call_charges_api.domain.entities.phone_bill import PhoneBill


@pytest.fixture
def phone_bill():
    """Configura uma instância de PhoneBill para os testes."""
    return PhoneBill(phone_number="1234567890", reference_period="11/2023")


def test_calculate_call_duration(phone_bill):
    """Testa o cálculo da duração de chamadas."""
    start_time = datetime(2023, 11, 1, 10, 0)
    end_time = datetime(2023, 11, 1, 10, 45)
    duration = phone_bill._calculate_call_duration(start_time, end_time)
    assert duration == "0h45m0s"


def test_calculate_call_cost_in_standard_rate(phone_bill):
    """Testa o cálculo do custo de uma chamada
    inteiramente no horário padrão."""
    start_time = datetime(2023, 11, 1, 8, 0)
    end_time = datetime(2023, 11, 1, 8, 30)
    cost = phone_bill._calculate_call_cost(start_time, end_time)
    assert cost == pytest.approx(0.36 + (30 * 0.09), rel=1e-2)


def test_calculate_call_cost_in_reduced_rate(phone_bill):
    """Testa o cálculo do custo de uma chamada
    inteiramente no horário reduzido."""
    start_time = datetime(2023, 11, 1, 23, 0)
    end_time = datetime(2023, 11, 1, 23, 30)
    cost = phone_bill._calculate_call_cost(start_time, end_time)
    assert cost == pytest.approx(0.36, rel=1e-2)


def test_calculate_call_cost_crossing_midnight(phone_bill):
    """Testa o cálculo do custo de uma chamada que cruza a meia-noite."""
    start_time = datetime(2023, 11, 1, 21, 30)
    end_time = datetime(2023, 11, 2, 0, 30)
    cost = phone_bill._calculate_call_cost(start_time, end_time)

    expected_cost = 0.36 + (30 * 0.09)
    assert cost == pytest.approx(expected_cost, rel=1e-2)


def test_add_call_record_pair(phone_bill):
    """Testa a adição de um par completo de registros de chamadas."""
    start_record = CallRecord(
        call_id=1,
        call_type=CallType.START,
        timestamp=datetime(2023, 11, 1, 10, 0),
        source="1234567890",
        destination="0987654321"
    )
    end_record = CallRecord(
        call_id=1,
        call_type=CallType.END,
        timestamp=datetime(2023, 11, 1, 10, 30)
    )

    phone_bill.add_call_record(start_record)
    result = phone_bill.add_call_record(end_record)
    assert result == "Call record pair added."
    assert len(phone_bill.call_records) == 1


def test_add_end_record_without_start(phone_bill):
    """Testa a tentativa de adicionar um registro de
    fim sem um correspondente registro de início."""
    end_record = CallRecord(
        call_id=2,
        call_type=CallType.END,
        timestamp=datetime(2023, 11, 1, 10, 30)
    )

    result = phone_bill.add_call_record(end_record)
    assert result == "Error: End record received without start record."
    assert len(phone_bill.call_records) == 0


def test_get_calls_summary(phone_bill):
    """Testa o resumo das chamadas, incluindo duração e custo."""
    start_record = CallRecord(
        call_id=3,
        call_type=CallType.START,
        timestamp=datetime(2023, 11, 1, 8, 0),
        source="1234567890",
        destination="0987654321"
    )
    end_record = CallRecord(
        call_id=3,
        call_type=CallType.END,
        timestamp=datetime(2023, 11, 1, 8, 30)
    )

    phone_bill.add_call_record(start_record)
    phone_bill.add_call_record(end_record)

    calls = phone_bill.get_calls()
    assert len(calls) == 1
    call = calls[0]
    assert call["destination"] == "0987654321"
    assert call["duration"] == "0h30m0s"
    assert call["price"] == pytest.approx(0.36 + (30 * 0.09), rel=1e-2)
