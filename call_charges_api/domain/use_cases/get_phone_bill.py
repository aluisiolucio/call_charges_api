from dataclasses import dataclass
from typing import List, Optional

from call_charges_api.domain.entities.call_record import CallRecord
from call_charges_api.domain.entities.phone_bill import PhoneBill
from call_charges_api.repositories.phone_bill_repository import (
    PhoneBillRepository,
)


@dataclass
class Input:
    phone_number: str
    reference_period: Optional[str] = None


@dataclass
class Output:
    id: str
    phone_number: str
    reference_period: str
    total_amount: str
    call_records: List[dict]


class GetPhoneBillUseCase:
    def __init__(self, repository: PhoneBillRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        input.phone_number = (
            input.phone_number.replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
            .replace('+55', '')
        )

        phone_bill_entity = PhoneBill(
            phone_number=input.phone_number,
            reference_period=input.reference_period,
        )
        phone_bill_entity.define_period()

        phone_bill = self.repository.get(
            phone_number=phone_bill_entity.phone_number,
            reference_period=phone_bill_entity.reference_period,
        )

        if not phone_bill:
            return None

        bill = Output(
            id=phone_bill.id,
            phone_number=phone_bill.phone_number,
            reference_period=phone_bill.reference_period,
            total_amount='',
            call_records=[],
        )

        for record in phone_bill.call_records:
            start_record = record[0]
            end_record = record[1]

            start_call_record = CallRecord(
                call_id=start_record.call_id,
                call_type=start_record.call_type,
                timestamp=start_record.timestamp,
                source=start_record.source,
                destination=start_record.destination,
            )
            end_call_record = CallRecord(
                call_id=end_record.call_id,
                call_type=end_record.call_type,
                timestamp=end_record.timestamp,
                source=end_record.source,
                destination=end_record.destination,
            )

            phone_bill_record = phone_bill_entity.calculate_call_records((
                start_call_record,
                end_call_record,
            ))

            bill.call_records.append({
                'destination': phone_bill_record.destination,
                'call_start_date': phone_bill_record.call_start_date,
                'call_start_time': phone_bill_record.call_start_time,
                'call_duration': phone_bill_record.duration,
                'call_price': phone_bill_record.price,
            })

        bill.total_amount = phone_bill_entity.formatted_total_amount

        return bill
