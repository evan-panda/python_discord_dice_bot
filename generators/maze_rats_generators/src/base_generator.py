import json
from random import choice, choices, sample


class Generator:
    def __init__(self):
        pass

    @staticmethod
    def load_json(file_name: str):
        with open(file_name) as file:
            return json.load(file)

    @staticmethod
    def get_choice(data: list) -> str:
        """Get a single item from the data"""
        return str(choice(data))

    @staticmethod
    def get_choices(data: list, num_options: int = 2) -> list:
        """Get a list of `num_options` items from the data"""
        return choices(data, k=num_options)

    @staticmethod
    def get_unique_choices(data: list, num_options: int = 2) -> list:
        """Get a list of unique items from the data"""
        # if requested number of options is greater than the number of items in the data, return the data
        if num_options > len(data):
            return data
            # raise ValueError("The number of options requested is greater than the number of items in the data.")

        return sample(data, num_options)
