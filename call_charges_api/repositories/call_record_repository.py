from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
from uuid import UUID


class Status(Enum):
    PENDDING = 'pendding'
    COMPLETED = 'completed'


@dataclass
class RecordInput:
    call_id: int
    call_type: str
    timestamp: str
    source: str
    destination: str
    status: Status


@dataclass
class RecordOutput:
    id: UUID
    call_id: int
    call_type: str
    timestamp: str
    source: str
    destination: str
    status: str


class CallRecordRepository(ABC):
    @abstractmethod
    def save(self, record: RecordInput) -> RecordOutput:
        pass

    @abstractmethod
    def record_exists(self, call_id: int, call_type: str) -> bool:
        pass

    @abstractmethod
    def record_exists_by_id(
        self, id: UUID, call_id: int, call_type: str
    ) -> bool:
        pass

    @abstractmethod
    def record_start_exists(self, call_id: int) -> bool:
        pass

    @abstractmethod
    def update(
        self, call_id: int, call_type: str, timestamp: str
    ) -> RecordOutput:
        pass

    @abstractmethod
    def update_status(self, call_id: int, status: Status) -> None:
        pass

    @abstractmethod
    def get_pair_by_call_id(
        self, call_id: int
    ) -> Tuple[RecordOutput, RecordOutput]:
        pass

    @abstractmethod
    def update_phone_bill_id(
        self, call_start_id: int, call_end_id: int, phone_bill_id: UUID
    ) -> None:
        pass
