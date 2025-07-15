import pytest

from src.processor import ScheduleProcessor
from src.dto import EmploymentScheduleDTO
from src.models import Day, Timeslot


@pytest.fixture(scope="function")
def mock_schedule() -> EmploymentScheduleDTO:
    """Фикстура для создания тестового расписания EmploymentScheduleDTO."""
    days = [
        Day(id=1, date="2024-01-01", start="09:00", end="18:00"),
        Day(id=2, date="2024-01-02", start="08:00", end="17:00")
    ]
    timeslots = [
        Timeslot(id=1, day_id=1, start="10:00", end="12:00"),
        Timeslot(id=2, day_id=1, start="14:00", end="15:00"),
        Timeslot(id=3, day_id=2, start="09:00", end="11:00")
    ]
    return EmploymentScheduleDTO(days=days, timeslots=timeslots)


class TestScheduleProcessor:
    def test_get_busy_timeslots_for_date_positive(self, monkeypatch, mock_schedule):
        """Проверка получения занятых слотов для существующей даты."""
        monkeypatch.setattr("builtins.input", lambda _: "2024-01-01")
        processor = ScheduleProcessor(action=1, schedule=mock_schedule)
        response = processor.get_response()
        expected = [
            {"start": "10:00", "end": "12:00"},
            {"start": "14:00", "end": "15:00"}
        ]
        assert response.result == expected

    def test_get_busy_timeslots_for_date_not_found(self, monkeypatch, capsys, mock_schedule):
        """Проверка поведения при запросе несуществующей даты."""
        monkeypatch.setattr("builtins.input", lambda _: "2024-01-03")
        processor = ScheduleProcessor(action=1, schedule=mock_schedule)
        with pytest.raises(SystemExit):
            processor.get_response()
        captured = capsys.readouterr()
        assert "Дата 2024-01-03 не найдена в расписании" in captured.out

    def test_get_free_timeslots_for_date_positive(self, monkeypatch, mock_schedule):
        """Проверка получения свободных слотов для существующей даты."""
        monkeypatch.setattr("builtins.input", lambda _: "2024-01-01")
        processor = ScheduleProcessor(action=2, schedule=mock_schedule)
        response = processor.get_response()
        expected = [
            {"start": "09:00", "end": "10:00"},
            {"start": "12:00", "end": "14:00"},
            {"start": "15:00", "end": "18:00"}
        ]
        assert response.result == expected

    def test_get_free_timeslots_for_date_not_found(self, monkeypatch, capsys, mock_schedule):
        """Проверка поведения при запросе несуществующей даты для свободных слотов."""
        monkeypatch.setattr("builtins.input", lambda _: "2024-01-03")
        processor = ScheduleProcessor(action=2, schedule=mock_schedule)
        with pytest.raises(SystemExit):
            processor.get_response()
        captured = capsys.readouterr()
        assert "Дата 2024-01-03 не найдена в расписании" in captured.out

    def test_timeslots_interval_access_available(self, monkeypatch, mock_schedule):
        """Проверка доступного временного интервала."""
        inputs = iter(["2024-01-01", "12:00", "13:00"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=3, schedule=mock_schedule)
        response = processor.get_response()
        assert response.result == "Данный промежуток для заданной даты доступен"

    def test_timeslots_interval_access_not_available(self, monkeypatch, mock_schedule):
        """Проверка недоступного временного интервала."""
        inputs = iter(["2024-01-01", "10:30", "11:30"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=3, schedule=mock_schedule)
        response = processor.get_response()
        assert response.result == "Промежуток для заданной даты недоступен"

    def test_timeslots_interval_access_invalid_input(self, monkeypatch, capsys, mock_schedule):
        """Проверка обработки некорректного формата времени."""
        inputs = iter(["2024-01-01", "25:00", "26:00", "12:00", "13:00"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=3, schedule=mock_schedule)
        response = processor.get_response()
        captured = capsys.readouterr()
        assert response.result == "Данный промежуток для заданной даты доступен"
        assert "Некорректный формат интервала" in captured.out

    def test_search_available_timeslots_for_duration_positive(self, monkeypatch, mock_schedule):
        """Проверка поиска слотов для заданной продолжительности."""
        inputs = iter(["2024-01-01", "60"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=4, schedule=mock_schedule)
        response = processor.get_response()
        expected = [
            {"start": "09:00", "end": "10:00"},
            {"start": "12:00", "end": "14:00"},
            {"start": "15:00", "end": "18:00"}
        ]
        assert response.result == expected

    def test_search_available_timeslots_for_duration_no_slots(self, monkeypatch, mock_schedule):
        """Проверка случая, когда нет доступных слотов для заданной продолжительности."""
        inputs = iter(["2024-01-01", "181"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=4, schedule=mock_schedule)
        response = processor.get_response()
        assert response.result == "Для заданной продолжительности заявки на указанную дату нет доступных промежутков"

    def test_search_available_timeslots_for_duration_invalid_input(self, monkeypatch, capsys, mock_schedule):
        """Проверка обработки некорректного ввода продолжительности."""
        inputs = iter(["2024-01-01", "abc", "60"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        processor = ScheduleProcessor(action=4, schedule=mock_schedule)
        response = processor.get_response()
        captured = capsys.readouterr()
        assert isinstance(response.result, list)
        assert "Некорректный формат продолжительности" in captured.out

    def test_get_response_unknown_action(self, monkeypatch, capsys, mock_schedule):
        """Проверка поведения при неизвестном действии."""
        monkeypatch.setattr("builtins.input", lambda _: "2024-01-01")
        processor = ScheduleProcessor(action=999, schedule=mock_schedule)
        with pytest.raises(SystemExit):
            processor.get_response()
        captured = capsys.readouterr()
        assert "Неизвестный запрос действия!" in captured.out
