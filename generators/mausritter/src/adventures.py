from .data_paths import ADVENTUR_PATHS
from .generator import Generator

class AdventureGenerator(Generator):
    def __init__(self, adventure_seed = None, hex_details = None) -> None:
        pass

    def _get_seed_data(self) -> tuple[str, str, str]:
        data = self._get_json_data()
        creature = self._get_choice(data['Creature'])
        problem = self._get_choice(data['Problem'])
        complication = self._get_choice(data['Complication'])
    
        return creature, problem, complication

    def get_adventure_seed(self):
        seed_data = self._get_seed_data()
        seed_data = f"There is a {seed_data[0]} that/that's {seed_data[1]}, but/and {seed_data[2]}"
        return seed_data
