from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class RecordInput:
    call_id: int
    call_type: str
    timestamp: str
    source: str
    destination: str


@dataclass
class RecordOutput:
    id: UUID
    call_id: int
    call_type: str
    timestamp: str
    source: str
    destination: str


class CallRecordRepository(ABC):
    @abstractmethod
    def save(self, record: RecordInput) -> RecordOutput:
        pass

    @abstractmethod
    def get_by_call_id(self, call_id: int) -> RecordOutput:
        pass

    @abstractmethod
    def has_start_record(self, call_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, record: RecordOutput, call_record_db: RecordOutput):
        pass
