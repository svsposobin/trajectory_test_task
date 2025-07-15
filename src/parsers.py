from typing import Any, Dict

from src.dto import EmploymentScheduleDTO
from src.models import Day, Timeslot


def employment_schedule_parser(data: Dict[str, Any]) -> EmploymentScheduleDTO:
    result: EmploymentScheduleDTO = EmploymentScheduleDTO()

    result.days = [Day(**day) for day in data['days']]
    result.timeslots = [Timeslot(**timeslot) for timeslot in data['timeslots']]

    return result


def time_to_minutes(time_str: str) -> int:
    hours, minutes = map(int, time_str.split(':'))

    return hours * 60 + minutes


def minutes_to_time(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)

    return f"{hours:02d}:{mins:02d}"
