from datetime import datetime
from enum import Enum
from typing import Optional


class CallType(Enum):
    START = 'start'
    END = 'end'


class CallRecord:
    def __init__(
        self,
        call_id: int,
        call_type: CallType,
        timestamp: datetime,
        source: Optional[str] = None,
        destination: Optional[str] = None,
    ):
        self.call_id = call_id
        self.call_type = call_type
        self.timestamp = timestamp
        self.source = source
        self.destination = destination

        self._validate()

    def _validate(self):
        if self.call_type == CallType.START:
            if not self.source or not self.destination:
                raise ValueError(
                    'Source and destination are required '
                    'for a start call record.'
                )
        elif self.call_type == CallType.END:
            if self.source or self.destination:
                raise ValueError(
                    'Source and destination should not '
                    'be provided for an end call record.'
                )

    def is_start(self) -> bool:
        return self.call_type == CallType.START

    def is_end(self) -> bool:
        return self.call_type == CallType.END
