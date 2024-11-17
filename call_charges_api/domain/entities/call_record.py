import re
from datetime import datetime
from enum import Enum
from typing import Optional

from call_charges_api.domain.errors.exceptions import (
    BusinessException,
    InvalidPhoneNumberException,
)


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

    def validate_call_record(self):
        if self.call_type == CallType.START:
            if not self.source or not self.destination:
                raise BusinessException(
                    'Source and destination are required '
                    'for a start call record.'
                )
        elif self.call_type == CallType.END:
            self.source = None
            self.destination = None

    def validate_phone_numbers(self) -> bool:
        pattern = r'^\d{2}(?:\d{8}|\d{9})$'

        if self.source and not re.match(pattern, self.source):
            raise InvalidPhoneNumberException(self.source)

        if self.destination and not re.match(pattern, self.destination):
            raise InvalidPhoneNumberException(self.destination)

    def is_start(self) -> bool:
        return self.call_type == CallType.START

    def is_end(self) -> bool:
        return self.call_type == CallType.END
