from re import fullmatch, Match
from typing import Optional
from datetime import datetime

from src.common.regex import VALIDATE_ACTION_PATTERN, VALIDATE_TIMESLOTS_DURATION_PATTERN
from src.parsers import time_to_minutes


class ArgsValidator:

    @staticmethod
    def validate_action(action: str) -> int:
        match: Optional[Match[str]] = fullmatch(pattern=VALIDATE_ACTION_PATTERN, string=action)

        if not match:
            raise ValueError("Некорректный выбор действия, введите цифру от 1 до 4")

        return int(action)

    @staticmethod
    def validate_date(date: str) -> None:
        try:
            datetime.strptime(date, "%Y-%m-%d")

        except Exception:
            raise ValueError("Некорректный формат даты")

    @staticmethod
    def validate_timeslots_intervals(start: str, end: str):
        try:
            datetime.strptime(start, "%H:%M")
            datetime.strptime(end, "%H:%M")

        except Exception:
            raise ValueError("Некорректный формат интервала")

        if time_to_minutes(start) >= time_to_minutes(end):
            raise ValueError("Начало промежутка не может быть >= его концу")

    @staticmethod
    def validate_available_timeslots_duration(duration: str) -> int:
        match: Optional[Match[str]] = fullmatch(pattern=VALIDATE_TIMESLOTS_DURATION_PATTERN, string=duration)

        if not match:
            raise ValueError(
                "Некорректный формат продолжительности заявки\n"
                "Заявка не может начинаться с нуля или быть больше 1440 минут (24 часов)"
            )

        return int(duration)
