from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from call_charges_api.domain.entities.call_record import CallType


class CallRecordRequestSchema(BaseModel):
    type: CallType
    timestamp: str
    call_id: int
    source: Optional[str] = None
    destination: Optional[str] = None
    id: Optional[UUID] = None


class CallRecordResponseSchema(BaseModel):
    id: UUID
    type: str
    timestamp: datetime
    call_id: int
    source: Optional[str] = None
    destination: Optional[str] = None
