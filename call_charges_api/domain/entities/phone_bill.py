from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Tuple

from call_charges_api.domain.entities.call_record import CallRecord


class PhoneBill:
    def __init__(self, phone_number: str, reference_period: str):
        self.phone_number = phone_number
        self.reference_period = reference_period
        self.call_records: List[Tuple[CallRecord, CallRecord]] = []
        self._pending_records: Dict[int, CallRecord] = {}

    def get_calls(self) -> List[dict]:
        results = []
        for start_record, end_record in self.call_records:
            duration = self._calculate_call_duration(
                start_record.timestamp, end_record.timestamp
            )
            price = self._calculate_call_cost(
                start_record.timestamp, end_record.timestamp
            )

            results.append({
                'destination': start_record.destination,
                'start_time': start_record.timestamp,
                'end_time': end_record.timestamp,
                'duration': duration,
                'price': price,
            })

        return results

    def add_call_record(self, call_record: CallRecord) -> Optional[str]:
        if call_record.is_start():
            self._pending_records[call_record.call_id] = call_record
            return 'Start record added.'
        elif call_record.is_end():
            start_record = self._pending_records.pop(call_record.call_id, None)
            if start_record:
                self.call_records.append((start_record, call_record))
                return 'Call record pair added.'
            else:
                return 'Error: End record received without start record.'

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
    ) -> float:
        fixed_rate = 0.36
        rate_per_call = self._calculate_rate_per_call(start_time, end_time)

        return fixed_rate + rate_per_call
