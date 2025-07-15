from sys import exit as sys_exit
from typing import Dict, Any, List, Optional

from src.dto import EmploymentScheduleDTO, ProcessorResponse
from src.common.validator import ArgsValidator
from src.models import Timeslot
from src.parsers import time_to_minutes, minutes_to_time


class ScheduleProcessor:
    def __init__(self, action: int, schedule: EmploymentScheduleDTO):
        self.action: int = action
        self._schedule: EmploymentScheduleDTO = schedule

    def get_response(self) -> ProcessorResponse:
        result: ProcessorResponse = ProcessorResponse()
        date, day_id = self._correct_date()

        match self.action:
            case 1:
                result.result = self._get_busy_timeslots_for_date(day_id=day_id)
            case 2:
                result.result = self._get_free_timeslots_for_date(date=date, day_id=day_id)
            case 3:
                result.result = self._timeslots_interval_access(date=date, day_id=day_id)
            case 4:
                result.result = self._search_available_timeslots_for_duration(date=date, day_id=day_id)
            case _:
                print("Неизвестный запрос действия!")
                sys_exit(1)

        if result.result is None:
            print("По запросу ничего не найдено")
            sys_exit(1)

        return result

    def _get_busy_timeslots_for_date(self, day_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if day_id is None:
            day_id = self._correct_date()[1]

        day_timeslots: List[Timeslot] = [
            timeslot for timeslot in self._schedule.timeslots if timeslot.day_id == day_id  # type: ignore[union-attr]
        ]

        busy_timeslots: List[Dict[str, Any]] = [
            {"start": timeslot.start, "end": timeslot.end} for timeslot in day_timeslots
        ]

        return sorted(busy_timeslots, key=lambda timeslot: time_to_minutes(time_str=timeslot["start"]))

    def _get_free_timeslots_for_date(self, date: str, day_id: int) -> List[Dict[str, Any]]:
        found_day = next(day for day in self._schedule.days if day.date == date)  # type: ignore[union-attr]
        busy_timeslots: List[Dict[str, Any]] = self._get_busy_timeslots_for_date(day_id)

        free_slots: List[Dict[str, Any]] = []
        current_start: int = time_to_minutes(found_day.start)  # Начало рабочего дня

        for slot in busy_timeslots:
            slot_start: int = time_to_minutes(slot['start'])
            slot_end: int = time_to_minutes(slot['end'])

            if current_start < slot_start:
                free_slots.append({
                    "start": minutes_to_time(current_start),
                    "end": minutes_to_time(slot_start)
                })

            current_start = max(current_start, slot_end)

        if current_start < time_to_minutes(found_day.end):
            free_slots.append({
                "start": minutes_to_time(current_start),
                "end": found_day.end
            })

        return free_slots

    def _timeslots_interval_access(self, date: str, day_id: int) -> str:
        print(
            "Введите начало и конец нужного временного промежутка в виде ЧЧ:ММ (ЧАСЫ:МИНУТЫ)\n"
            "Пример: Начало: 15:30 ; Конец: 16:45\n"
            "------------------------------------------------------------------------------"
        )
        while True:
            start_interval: str = input("Начало промежутка: ")
            end_interval: str = input("Конец промежутка: ")

            try:
                ArgsValidator.validate_timeslots_intervals(start=start_interval, end=end_interval)

                free_slots: List[Dict[str, Any]] = self._get_free_timeslots_for_date(date, day_id)

                for slot in free_slots:
                    slot_start: int = time_to_minutes(slot['start'])
                    slot_end: int = time_to_minutes(slot['end'])

                    if slot_start <= time_to_minutes(start_interval) and time_to_minutes(end_interval) <= slot_end:
                        return "Данный промежуток для заданной даты доступен"

                return "Промежуток для заданной даты недоступен"

            except Exception as error:
                print(error)

    def _search_available_timeslots_for_duration(self, date: str, day_id: int):
        print(
            "Необходимо ввести продолжительность заявки в минутах\n"
            "Предупреждение!\n"
            "1. Продолжительность заявки не может начинаться с 0\n"
            "2. Продолжительность заявки не может быть больше продолжительности рабочего дня"
        )
        while True:
            duration: str = input("Необходимая продолжительность: ")

            try:
                minutes: int = ArgsValidator.validate_available_timeslots_duration(duration=duration)
                free_slots: List[Dict[str, Any]] = self._get_free_timeslots_for_date(date, day_id)

                suitable_slots: List[Dict[str, Any]] = []

                for slot in free_slots:
                    slot_start: int = time_to_minutes(slot['start'])
                    slot_end: int = time_to_minutes(slot['end'])

                    if (slot_end - slot_start) >= minutes:
                        suitable_slots.append(slot)

                if not suitable_slots:
                    return "Для заданной продолжительности заявки на указанную дату нет доступных промежутков"

                return suitable_slots

            except Exception as error:
                print(error)

    def _correct_date(self) -> List[Any]:
        while True:
            date: str = input("Введите дату в формате ГГГГ-ММ-ДД: ")

            try:
                ArgsValidator.validate_date(date)

                found_day = next(
                    (day for day in self._schedule.days if day.date == date),  # type: ignore[union-attr]
                    None
                )
                if found_day is None:
                    print(f"Дата {date} не найдена в расписании.")
                    sys_exit(1)

                return [date, found_day.id]

            except ValueError as error:
                print(error)
