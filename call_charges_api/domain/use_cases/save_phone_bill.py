from typing import Tuple
from uuid import UUID

from call_charges_api.domain.entities.call_record import CallRecord
from call_charges_api.domain.entities.phone_bill import PhoneBill
from call_charges_api.repositories.phone_bill_repository import (
    PhoneBillInput,
    PhoneBillRepository,
)


class SavePhoneBillUseCase:
    def __init__(self, repository: PhoneBillRepository):
        self.repository = repository

    def execute(self, call_pair: Tuple[CallRecord, CallRecord]) -> UUID:
        reference_period = call_pair[1].timestamp.strftime('%m/%Y')
        phone_bill_exists = self.repository.phone_bill_exists(
            reference_period, call_pair[0].source
        )

        if phone_bill_exists:
            phone_bill = (
                self.repository.get_by_phone_number_and_reference_period(
                    call_pair[0].source, reference_period
                )
            )
        else:
            phone_bill_entity = PhoneBill(
                phone_number=call_pair[0].source,
                reference_period=reference_period,
            )

            phone_bill = self.repository.save(
                PhoneBillInput(
                    phone_number=phone_bill_entity.phone_number,
                    reference_period=phone_bill_entity.reference_period,
                )
            )

        return phone_bill.id
