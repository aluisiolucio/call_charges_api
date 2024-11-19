from dataclasses import dataclass
from datetime import datetime

from call_charges_api.domain.entities.call_record import CallRecord, CallType
from call_charges_api.domain.errors.exceptions import (
    InvalidPhoneNumberException,
    StartRecordNotFoundException,
)
from call_charges_api.domain.use_cases.save_phone_bill import (
    SavePhoneBillUseCase,
)
from call_charges_api.repositories.call_record_repository import (
    CallRecordRepository,
    RecordInput,
    Status,
)
from call_charges_api.repositories.phone_bill_repository import (
    PhoneBillRepository,
)


@dataclass
class Input:
    call_type: CallType
    timestamp: datetime
    call_id: int
    source: str
    destination: str


@dataclass
class Output:
    id: str
    call_type: CallType
    timestamp: datetime
    call_id: int
    source: str
    destination: str


class RegisterCallUseCase:
    def __init__(
        self,
        call_record_repository: CallRecordRepository,
        phone_bill_repository: PhoneBillRepository,
    ):
        self.call_record_repository = call_record_repository
        self.phone_bill_repository = phone_bill_repository

    def execute(self, input: Input) -> Output:
        if input.source:
            input.source = (
                input.source.replace(' ', '')
                .replace('-', '')
                .replace('(', '')
                .replace(')', '')
                .replace('+55', '')
            )
        if input.destination:
            input.destination = (
                input.destination.replace(' ', '')
                .replace('-', '')
                .replace('(', '')
                .replace(')', '')
                .replace('+55', '')
            )

        if input.source and input.source == input.destination:
            raise InvalidPhoneNumberException(input.source)

        call_record = CallRecord(
            call_id=input.call_id,
            call_type=input.call_type,
            timestamp=datetime.fromisoformat(input.timestamp),
            source=input.source,
            destination=input.destination,
        )
        call_record.validate_call_record()
        call_record.validate_phone_numbers()

        contains_start_record = (
            self.call_record_repository.record_start_exists(
                call_id=call_record.call_id
            )
        )

        if not contains_start_record and call_record.is_end():
            raise StartRecordNotFoundException(call_record.call_id)

        record_exists = self.call_record_repository.record_exists(
            call_id=call_record.call_id, call_type=call_record.call_type.value
        )

        if record_exists:
            record = self.call_record_repository.update(
                call_id=call_record.call_id,
                call_type=call_record.call_type.value,
                timestamp=call_record.timestamp,
            )
        else:
            if call_record.is_start():
                status = Status.PENDDING
            elif call_record.is_end() and contains_start_record:
                status = Status.COMPLETED

                self.call_record_repository.update_status(
                    call_id=call_record.call_id, status=status
                )

            record = self.call_record_repository.save(
                RecordInput(
                    call_id=call_record.call_id,
                    call_type=call_record.call_type.value,
                    timestamp=call_record.timestamp,
                    source=call_record.source,
                    destination=call_record.destination,
                    status=status,
                )
            )

        call_pair = self.call_record_repository.get_pair_by_call_id(
            call_id=record.call_id
        )

        if call_pair[0] and call_pair[1]:
            call_record_start = CallRecord(
                call_id=call_pair[0].call_id,
                call_type=CallType(call_pair[0].call_type),
                timestamp=call_pair[0].timestamp,
                source=call_pair[0].source,
                destination=call_pair[0].destination,
            )
            call_record_end = CallRecord(
                call_id=call_pair[1].call_id,
                call_type=CallType(call_pair[1].call_type),
                timestamp=call_pair[1].timestamp,
                source=call_pair[1].source,
                destination=call_pair[1].destination,
            )
            phone_use_case = SavePhoneBillUseCase(self.phone_bill_repository)
            phone_bill_id = phone_use_case.execute((
                call_record_start,
                call_record_end,
            ))

            self.call_record_repository.update_phone_bill_id(
                call_start_id=call_pair[0].id,
                call_end_id=call_pair[1].id,
                phone_bill_id=phone_bill_id,
            )

        return Output(
            id=str(record.id),
            call_type=record.call_type,
            timestamp=record.timestamp,
            call_id=record.call_id,
            source=record.source,
            destination=record.destination,
        )
