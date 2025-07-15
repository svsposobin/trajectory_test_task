from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.models import Day, Timeslot


@dataclass
class APIResponse:
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class EmploymentScheduleDTO:
    days: Optional[List[Day]] = None
    timeslots: Optional[List[Timeslot]] = None


@dataclass
class ProcessorResponse:
    result: Optional[Any] = None
