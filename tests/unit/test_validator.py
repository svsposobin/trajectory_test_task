import pytest

from src.common.validator import ArgsValidator


class TestArgsValidator:
    @pytest.mark.parametrize(
        "action, expected_result",
        [
            ("1", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5)
        ]
    )
    def test_validate_action_valid(self, action: str, expected_result: int):
        assert ArgsValidator.validate_action(action) == expected_result

    @pytest.mark.parametrize(
        "invalid_action",
        [
            "0", "6", "a", "10", ""
        ]
    )
    def test_validate_action_invalid(self, invalid_action):
        with pytest.raises(ValueError, match="Некорректный выбор действия"):
            ArgsValidator.validate_action(invalid_action)

    @pytest.mark.parametrize(
        "valid_date",
        [
            "2024-01-01",
            "2025-12-31",
            "2000-02-29"  # Високосный год
        ]
    )
    def test_validate_date_valid(self, valid_date: str):
        ArgsValidator.validate_date(valid_date)  # Без ошибок

    @pytest.mark.parametrize(
        "invalid_date",
        [
            "2024-13-01",
            "2024-00-01",
            "2024-01-32",
            "01-01-2024",
            "2024/01/01",
            "not-a-date",
            ""
        ]
    )
    def test_validate_date_invalid(self, invalid_date: str):
        with pytest.raises(ValueError, match="Некорректный формат даты"):
            ArgsValidator.validate_date(invalid_date)

    @pytest.mark.parametrize(
        "start, end",
        [
            ("09:00", "10:00"),
            ("00:00", "23:59"),
            ("12:30", "13:45")
        ]
    )
    def test_validate_timeslots_intervals_valid(self, start, end):
        ArgsValidator.validate_timeslots_intervals(start, end)  # Без ошибок

    @pytest.mark.parametrize(
        "start, end, error_msg",
        [
            ("25:00", "26:00", "Некорректный формат интервала"),
            ("12:00", "11:00", "Начало промежутка не может быть >= его концу"),
            ("invalid", "time", "Некорректный формат интервала"),
            ("12:00", "12:00", "Начало промежутка не может быть >= его концу")
        ]
    )
    def test_validate_timeslots_intervals_invalid(self, start: str, end: str, error_msg: str):
        with pytest.raises(ValueError, match=error_msg):
            ArgsValidator.validate_timeslots_intervals(start, end)

    @pytest.mark.parametrize(
        "duration, "
        "expected_result",
        [
            ("1", 1),
            ("60", 60),
            ("1440", 1440),
            ("999", 999)
        ]
    )
    def test_validate_duration_valid(self, duration: str, expected_result: int):
        assert ArgsValidator.validate_available_timeslots_duration(duration) == expected_result

    @pytest.mark.parametrize(
        "invalid_duration",
        [
            "0", "1441", "9999", "-10", "01", "00", "001", "abc", ""
        ]
    )
    def test_validate_duration_invalid(self, invalid_duration: str):
        with pytest.raises(ValueError, match="Некорректный формат продолжительности"):
            ArgsValidator.validate_available_timeslots_duration(invalid_duration)
