from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Tuple

from call_charges_api.domain.entities.call_record import CallRecord


@dataclass
class PhoneBillRecords:
    destination: str
    call_start_date: date
    call_start_time: time
    duration: str
    price: str


class PhoneBill:
    def __init__(self, phone_number: str, reference_period: str | None = None):
        self.phone_number = phone_number
        self.reference_period = reference_period
        self.total_amount: float = 0.0

    @property
    def formatted_total_amount(self) -> str:
        return f'R$ {self.total_amount:.2f}'.replace('.', ',')

    def calculate_call_records(
        self, call_records_pairs: Tuple[CallRecord, CallRecord]
    ) -> PhoneBillRecords:
        self.define_period()

        start_record, end_record = call_records_pairs

        call_duration = self._calculate_call_duration(
            start_record.timestamp, end_record.timestamp
        )
        call_price = self._calculate_call_cost(
            start_record.timestamp, end_record.timestamp
        )

        return PhoneBillRecords(
            destination=start_record.destination,
            call_start_date=start_record.timestamp.date(),
            call_start_time=start_record.timestamp.time(),
            duration=call_duration,
            price=call_price,
        )

    @staticmethod
    def _calculate_call_duration(
        start_time: datetime, end_time: datetime
    ) -> str:
        duration = end_time - start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'{int(hours)}h{int(minutes)}m{int(seconds)}s'

    @staticmethod
    def _calculate_minutes_between(
        start_time: datetime, end_time: datetime
    ) -> int:
        nighttime_start = time(22, 0)
        nighttime_end = time(6, 0)

        total_minutes = 0
        current_time = start_time

        while current_time < end_time:
            if nighttime_end <= current_time.time() < nighttime_start:
                total_minutes += 1

            current_time += timedelta(minutes=1)

        return total_minutes

    def _calculate_rate_per_call(
        self, start_time: datetime, end_time: datetime
    ) -> float:
        rate_per_call = 0.09
        minutes = self._calculate_minutes_between(start_time, end_time)

        return minutes * rate_per_call

    def _calculate_call_cost(
        self, start_time: datetime, end_time: datetime
    ) -> str:
        fixed_rate = 0.36
        rate_per_call = self._calculate_rate_per_call(start_time, end_time)

        value = fixed_rate + rate_per_call
        self.total_amount += value

        return f'R$ {value:.2f}'.replace('.', ',')

    def define_period(self):
        DECEMBER = 12

        if not self.reference_period:
            current_date = datetime.now()
            last_month = (
                current_date.month - 1 if current_date.month > 1 else DECEMBER
            )
            year = current_date.year

            if last_month == DECEMBER:
                year -= 1

            self.reference_period = f'{last_month}/{year}'
