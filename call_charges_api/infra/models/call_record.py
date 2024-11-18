from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from call_charges_api.infra.models.base import table_registry


@table_registry.mapped_as_dataclass
class CallRecordModel:
    __tablename__ = 'call_records'

    status: Mapped[str] = mapped_column(nullable=False)
    destination: Mapped[str] = mapped_column(nullable=True)
    source: Mapped[str] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    call_id: Mapped[int] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)

    phone_bill_id: Mapped[UUID] = mapped_column(
        ForeignKey('phone_bills.id'), nullable=True
    )
