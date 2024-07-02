from .data_paths import ADVENTURE_PATHS
from generators.base_generator import Generator

class AdventureGenerator(Generator):
    def __init__(self, adventure_seed = None, hex_details = None) -> None:
        pass

    def _get_seed_data(self) -> tuple[str, str, str]:
        data = self._get_json_data(ADVENTURE_PATHS['adventure_seeds'])

        creature = self._get_choice(data['Creature'])
        problem = self._get_choice(data['Problem'])
        complication = self._get_choice(data['Complication'])

        return creature, problem, complication

    def get_adventure_seed(self):
        creature, problem, complication = self._get_seed_data()
        seed_data = f"There is a {creature}\n"\
                    f"that has a problem: {problem},\n"\
                    f"but it's complicated by: {complication}"
        return seed_data

    def _get_hex_data(self) -> tuple:
        pass

    def get_hex_details(self) -> str:
        pass

    def get_three_word_story(self) -> str:
        pass
