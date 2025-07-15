from requests import get as requests_get, Response
from requests.exceptions import RequestException

from src.dto import APIResponse


def get_employment_schedule(url: str) -> APIResponse:
    result: APIResponse = APIResponse()

    try:
        response: Response = requests_get(url=url)

        if not response.ok:
            raise RequestException(f"Возникла проблема при запросе к URL, код ответа -> {response.status_code}.")

        result.result = response.json()

    except Exception as error:
        result.error = str(error)

    return result
