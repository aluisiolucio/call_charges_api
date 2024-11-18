from uuid import uuid4

from sqlalchemy import select

from call_charges_api.infra.models.call_record import CallRecordModel
from call_charges_api.infra.models.phone_bill import PhoneBillModel
from call_charges_api.repositories.phone_bill_repository import (
    CallRecordOutput,
    PhoneBillInput,
    PhoneBillOutput,
    PhoneBillRepository,
)


class SQLAlchemyPhoneBillRepository(PhoneBillRepository):
    def __init__(self, session):
        self.session = session

    def get(
        self, phone_number: str, reference_period: str
    ) -> PhoneBillOutput | None:
        bill = self.session.scalar(
            select(PhoneBillModel)
            .where(PhoneBillModel.phone_number == phone_number)
            .filter(PhoneBillModel.reference_period == reference_period)
        )

        if not bill:
            return None

        records = self.session.scalars(
            select(CallRecordModel).where(
                CallRecordModel.phone_bill_id == bill.id
            )
        ).all()

        pairs = []
        for record in records:
            if record.type == 'start':
                pairs.append({
                    'start': CallRecordOutput(
                        id=record.id,
                        call_id=record.call_id,
                        call_type=record.type,
                        timestamp=record.timestamp,
                        source=record.source,
                        destination=record.destination,
                        status=record.status,
                    ),
                    'end': None,
                })
            else:
                for pair in pairs:
                    if pair['start'].call_id == record.call_id:
                        pair['end'] = CallRecordOutput(
                            id=record.id,
                            call_id=record.call_id,
                            call_type=record.type,
                            timestamp=record.timestamp,
                            source=record.source,
                            destination=record.destination,
                            status=record.status,
                        )
                        break

        result_as_tuples = [(pair['start'], pair['end']) for pair in pairs]

        return PhoneBillOutput(
            id=bill.id,
            phone_number=bill.phone_number,
            reference_period=bill.reference_period,
            call_records=result_as_tuples,
        )

    def get_by_phone_number_and_reference_period(
        self, phone_number: str, reference_period: str
    ) -> PhoneBillOutput:
        bill = self.session.scalar(
            select(PhoneBillModel)
            .where(PhoneBillModel.phone_number == phone_number)
            .where(PhoneBillModel.reference_period == reference_period)
        )

        if not bill:
            return None

        return PhoneBillOutput(
            id=bill.id,
            phone_number=bill.phone_number,
            reference_period=bill.reference_period,
            call_records=[],
        )

    def save(self, phone_bill: PhoneBillInput) -> PhoneBillOutput:
        model = PhoneBillModel(
            id=uuid4(),
            phone_number=phone_bill.phone_number,
            reference_period=phone_bill.reference_period,
            call_records=[],
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return PhoneBillOutput(
            id=model.id,
            phone_number=model.phone_number,
            reference_period=model.reference_period,
            call_records=[],
        )

    def phone_bill_exists(
        self, reference_period: str, phone_number: str
    ) -> bool:
        bill = self.session.scalar(
            select(PhoneBillModel)
            .filter(PhoneBillModel.reference_period == reference_period)
            .filter(PhoneBillModel.phone_number == phone_number)
        )

        return bill is not None
