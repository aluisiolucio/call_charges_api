from uuid import uuid4

from sqlalchemy import select

from call_charges_api.infra.models.call_record import CallRecordModel
from call_charges_api.repositories.call_record_repository import (
    CallRecordRepository,
    RecordInput,
    RecordOutput,
)


class SQLAlchemyCallRecordRepository(CallRecordRepository):
    def __init__(self, session):
        self.session = session

    def save(self, call_record: RecordInput) -> RecordOutput:
        model = CallRecordModel(
            id=uuid4(),
            destination=call_record.destination,
            source=call_record.source,
            timestamp=call_record.timestamp,
            type=call_record.call_type,
            call_id=call_record.call_id,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return RecordOutput(
            id=model.id,
            call_id=model.call_id,
            call_type=model.type,
            timestamp=model.timestamp,
            source=model.source,
            destination=model.destination,
        )

    def get_by_call_id(self, call_id: int) -> RecordOutput:
        model = self.session.scalar(
            select(CallRecordModel).where(CallRecordModel.call_id == call_id)
        )

        if not model:
            return None

        return RecordOutput(
            id=model.id,
            call_id=model.call_id,
            call_type=model.type,
            timestamp=model.timestamp,
            source=model.source,
            destination=model.destination,
        )

    def has_start_record(self, call_id: int) -> bool:
        model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .where(CallRecordModel.type == 'start')
        )

        return model is not None

    def update(self, record: RecordOutput, call_record_db: RecordOutput):
        call_record_db.source = record.source
        call_record_db.destination = record.destination
        call_record_db.timestamp = record.timestamp

        self.session.commit()
        self.session.refresh(call_record_db)

        return RecordOutput(
            id=call_record_db.id,
            call_id=call_record_db.call_id,
            call_type=call_record_db.type,
            timestamp=call_record_db.timestamp,
            source=call_record_db.source,
            destination=call_record_db.destination,
        )
