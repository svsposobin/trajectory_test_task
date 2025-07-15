from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException

from src.utils import get_employment_schedule


class TestAPIs:
    @patch('src.utils.requests_get')
    def test_get_employment_schedule_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        result = get_employment_schedule("http://test.url")

        assert result.result == {"key": "value"}
        assert result.error is None

    @patch('src.utils.requests_get')
    def test_get_employment_schedule_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_employment_schedule("http://test.url")

        assert result.result is None
        assert "код ответа -> 404" in result.error  # type: ignore[operator]

    @patch('src.utils.requests_get')
    def test_get_employment_schedule_exception(self, mock_get):
        mock_get.side_effect = RequestException("Connection error")

        result = get_employment_schedule("http://test.url")

        assert result.result is None
        assert "Connection error" in result.error  # type: ignore[operator]

    @patch('src.utils.requests_get')
    def test_get_employment_schedule_json_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.side_effect = ValueError("JSON decode error")
        mock_get.return_value = mock_response

        result = get_employment_schedule("http://test.url")

        assert result.result is None
        assert "JSON decode error" in result.error  # type: ignore[operator]
