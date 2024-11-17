from dataclasses import dataclass
from datetime import datetime

from call_charges_api.domain.entities.call_record import CallRecord, CallType
from call_charges_api.domain.errors.exceptions import (
    StartRecordNotFoundException,
)
from call_charges_api.repositories.call_record_repository import (
    CallRecordRepository,
    RecordInput,
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
    def __init__(self, repository: CallRecordRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        call_record = CallRecord(
            call_id=input.call_id,
            call_type=input.call_type,
            timestamp=datetime.fromisoformat(input.timestamp),
            source=input.source,
            destination=input.destination,
        )
        call_record.validate_call_record()
        call_record.validate_phone_numbers()

        call_record_db = self.repository.get_by_call_id(call_record.call_id)

        if call_record.call_type == CallType.END and not call_record_db:
            raise StartRecordNotFoundException(call_record.call_id)

        if (
            call_record_db
            and call_record_db.call_type == call_record.call_type
        ):
            self.repository.update(
                RecordInput(
                    call_id=call_record.call_id,
                    call_type=call_record.call_type.value,
                    timestamp=call_record.timestamp,
                    source=call_record.source,
                    destination=call_record.destination,
                ),
                call_record_db,
            )
        else:
            record = self.repository.save(
                RecordInput(
                    call_id=call_record.call_id,
                    call_type=call_record.call_type.value,
                    timestamp=call_record.timestamp,
                    source=call_record.source,
                    destination=call_record.destination,
                )
            )

        return Output(
            id=str(record.id),
            call_type=record.call_type,
            timestamp=record.timestamp,
            call_id=record.call_id,
            source=record.source,
            destination=record.destination,
        )
