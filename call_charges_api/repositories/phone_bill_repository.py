from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from uuid import UUID


@dataclass
class PhoneBillInput:
    phone_number: str
    reference_period: str


@dataclass
class CallRecordOutput:
    id: int
    call_id: int
    call_type: str
    timestamp: str
    source: str
    destination: str
    status: str


@dataclass
class PhoneBillOutput:
    id: UUID
    phone_number: str
    reference_period: str
    call_records: Optional[List[Tuple[CallRecordOutput, CallRecordOutput]]] = (
        None
    )


class PhoneBillRepository(ABC):
    @abstractmethod
    def get(
        self, phone_number: str, reference_period: str
    ) -> PhoneBillOutput | None:
        pass

    @abstractmethod
    def get_by_phone_number_and_reference_period(
        self, phone_number: str, reference_period: str
    ) -> PhoneBillOutput:
        pass

    @abstractmethod
    def save(self, phone_bill: PhoneBillInput) -> PhoneBillOutput:
        pass

    @abstractmethod
    def phone_bill_exists(
        self, reference_period: str, phone_number: str
    ) -> bool:
        pass
