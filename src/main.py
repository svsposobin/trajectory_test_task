import sys
import os

# Adding ./src to python path for running from console purpose:
sys.path.append(os.getcwd())

from src.logic import run
from src.dto import ProcessorResponse
from src.common.read_args import get_action

if __name__ == "__main__":
    action_id: int = get_action()

    result: ProcessorResponse = run(action_id=action_id)

    print(result.result)
