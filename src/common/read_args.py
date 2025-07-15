from sys import exit as sys_exit
from src.constants import EMPLOYMENT_SCHEDULE_URL
from src.common.validator import ArgsValidator


def get_action() -> int:
    print(
        f"Утилита получает график занятости работника по 'ендпоинту': {EMPLOYMENT_SCHEDULE_URL}\n"
        "Не использует CLI-Инструменты\n"
        "------------------------------------------------------------------------------\n"
        "Доступные действия:\n"
        "1. Найти все занятые промежутки для указанной даты\n"
        "2. Найти свободное время для заданной даты\n"
        "3. Доступен ли указанный промежуток времени для заданной даты\n"
        "4. Найти для указанной продолжительности заявки свободное время в графике\n"
        "5. Выход\n"
        "------------------------------------------------------------------------------"
    )

    while True:
        action = str(input("Выберите действие: "))

        try:
            parsed_action: int = ArgsValidator.validate_action(action)

            if parsed_action == 5:
                sys_exit(1)

            return parsed_action

        except Exception as error:
            print(error)
