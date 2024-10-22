import json
from random import choice, choices, sample


class Generator:
    def __init__(self) -> None:
        """Base class for all generators."""
        ...

    @staticmethod
    def load_json(file_name: str) -> list[str]:
        """Load a JSON file"""
        with open(file_name) as file:
            return json.load(file)

    @staticmethod
    def get_choice(data: list) -> str:
        """Get a single item from the data"""
        return str(choice(data))

    @staticmethod
    def get_choices(data: list[str], num_options: int = 2) -> list[str]:
        """Get a list of `num_options` items from the data (with replacement)"""
        return choices(data, k=num_options)

    @staticmethod
    def get_unique_choices(data: list[str], num_options: int = 2) -> list[str]:
        """Get a list of unique items from the data (without replacement)"""
        # if requested number of options is greater than the number of items in the data, return the data
        if num_options > len(data):
            return data
            # raise ValueError("The number of options requested is greater than the number of items in the data.")

        return sample(data, num_options)
