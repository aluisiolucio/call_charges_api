from typing import Tuple
from uuid import UUID, uuid4

from sqlalchemy import select

from call_charges_api.infra.models.call_record import CallRecordModel
from call_charges_api.repositories.call_record_repository import (
    CallRecordRepository,
    RecordInput,
    RecordOutput,
    Status,
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
            status=call_record.status.value,
            phone_bill_id=None,
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
            status=model.status,
        )

    def record_exists(self, call_id: int, call_type: str) -> bool:
        model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .filter(CallRecordModel.type == call_type)
        )

        return model is not None

    def record_start_exists(self, call_id: int) -> bool:
        model = self.session.scalar(
            select(CallRecordModel).where(
                CallRecordModel.call_id == call_id
                and CallRecordModel.type == 'start'
            )
        )

        return model is not None

    def update(
        self, call_id: int, call_type: str, timestamp: str
    ) -> RecordOutput:
        model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .filter(CallRecordModel.type == call_type)
        )

        model.timestamp = timestamp
        self.session.commit()
        self.session.refresh(model)

        return RecordOutput(
            id=model.id,
            call_id=model.call_id,
            call_type=model.type,
            timestamp=model.timestamp,
            source=model.source,
            destination=model.destination,
            status=model.status,
        )

    def update_status(self, call_id: int, status: Status) -> None:
        model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .filter(CallRecordModel.type == 'start')
        )

        model.status = status.value
        self.session.commit()

    def get_pair_by_call_id(
        self, call_id: int
    ) -> Tuple[RecordOutput, RecordOutput]:
        start_model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .filter(CallRecordModel.type == 'start')
            .filter(CallRecordModel.status == 'completed')
        )

        end_model = self.session.scalar(
            select(CallRecordModel)
            .where(CallRecordModel.call_id == call_id)
            .filter(CallRecordModel.type == 'end')
            .filter(CallRecordModel.status == 'completed')
        )

        if not start_model or not end_model:
            return None, None

        return RecordOutput(
            id=start_model.id,
            call_id=start_model.call_id,
            call_type=start_model.type,
            timestamp=start_model.timestamp,
            source=start_model.source,
            destination=start_model.destination,
            status=start_model.status,
        ), RecordOutput(
            id=end_model.id,
            call_id=end_model.call_id,
            call_type=end_model.type,
            timestamp=end_model.timestamp,
            source=end_model.source,
            destination=end_model.destination,
            status=end_model.status,
        )

    def update_phone_bill_id(
        self, call_start_id: int, call_end_id: int, phone_bill_id: UUID
    ) -> None:
        start_model = self.session.scalar(
            select(CallRecordModel).where(CallRecordModel.id == call_start_id)
        )

        end_model = self.session.scalar(
            select(CallRecordModel).where(CallRecordModel.id == call_end_id)
        )

        if start_model and end_model:
            if not start_model.phone_bill_id and not end_model.phone_bill_id:
                start_model.phone_bill_id = phone_bill_id
                end_model.phone_bill_id = phone_bill_id

                self.session.commit()
