from sys import exit as sys_exit

from src.processor import ScheduleProcessor
from src.dto import EmploymentScheduleDTO, APIResponse, ProcessorResponse
from src.parsers import employment_schedule_parser
from src.utils import get_employment_schedule
from src.constants import EMPLOYMENT_SCHEDULE_URL


def run(action_id: int) -> ProcessorResponse:
    api_response: APIResponse = get_employment_schedule(
        url=EMPLOYMENT_SCHEDULE_URL,
    )
    if api_response.error:
        print(api_response.error)
        sys_exit(1)

    assert api_response.result is not None

    parsed_api_response: EmploymentScheduleDTO = employment_schedule_parser(
        data=api_response.result
    )

    processor: ScheduleProcessor = ScheduleProcessor(
        action=action_id,
        schedule=parsed_api_response
    )
    response: ProcessorResponse = processor.get_response()

    return response
