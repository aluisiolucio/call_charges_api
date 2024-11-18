from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel


class FiltersSchema(BaseModel):
    phone_number: str
    reference_period: Optional[str] = None


class CallRecordsSchema(BaseModel):
    destination: str
    call_start_date: date
    call_start_time: time
    call_duration: str
    call_price: str


class PhoneBillResponseSchema(BaseModel):
    phone_number: str
    reference_period: str
    total_amount: str
    call_records: List[CallRecordsSchema]


class PhoneBillListSchema(BaseModel):
    bills: List[PhoneBillResponseSchema]
