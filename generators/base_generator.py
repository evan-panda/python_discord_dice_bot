import json
from random import choice

class Generator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _get_json_data(file_path: str) -> dict:
        with open(file_path, mode='r') as f:
            return json.load(f)

    @staticmethod
    def _get_choice(data: list) -> str:
        return choice(data)

    @staticmethod
    def _get_choice_options(data: list, choices: int = 2) -> tuple[str, str]:
        return (choice(data) for _ in range(choices))
