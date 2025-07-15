from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Day:
    id: int
    date: str
    start: str
    end: str


@dataclass
class Timeslot:
    id: int
    day_id: int
    start: str
    end: str


@dataclass
class BusyTimeslots:
    timeslots: Optional[Dict[str, List[str]]] = None
