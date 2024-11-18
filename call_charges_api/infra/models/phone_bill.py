from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from call_charges_api.infra.models.base import table_registry
from call_charges_api.infra.models.call_record import CallRecordModel


@table_registry.mapped_as_dataclass
class PhoneBillModel:
    __tablename__ = 'phone_bills'

    phone_number: Mapped[str] = mapped_column(nullable=False)
    reference_period: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)

    call_records: Mapped[List['CallRecordModel']] = relationship()
