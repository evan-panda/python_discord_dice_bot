from enum import Enum
import random

from generators.base_generator import Generator
from .datasets import MAGIC_TABLES


class MagicType(Enum):
    PHYS_EFFECT = "PHYS_EFFECT"
    PHYS_ELEMENT = "PHYS_ELEMENT"
    PHYS_FORM = "PHYS_FORM"
    ETH_EFFECT = "ETH_EFFECT"
    ETH_ELEMENT = "ETH_ELEMENT"
    ETH_FORM = "ETH_FORM"


class RandomMagic(Generator):
    def __init__(self) -> None:
        """Class for generating random magic spell names"""
        super().__init__()

    def _get_spell_formula(self, by_the_book: bool = True) -> tuple[MagicType, MagicType]:
        """Get the spell formula"""
        # get completely random combination for spell name
        if not by_the_book:
            return tuple(random.choices(population=list(MagicType), k=2))

        # get spell name in the format provided by the book
        spell_types = [
            # 1-3 results, Maze Rats pg.3
            (MagicType.PHYS_EFFECT, MagicType.PHYS_FORM),
            (MagicType.PHYS_EFFECT, MagicType.ETH_FORM),
            (MagicType.ETH_EFFECT, MagicType.PHYS_FORM),
            (MagicType.ETH_EFFECT, MagicType.ETH_FORM),
            (MagicType.PHYS_ELEMENT, MagicType.PHYS_FORM),
            (MagicType.PHYS_ELEMENT, MagicType.ETH_FORM),
            # 4-6 results, Maze Rats pg.3
            (MagicType.ETH_ELEMENT, MagicType.PHYS_FORM),
            (MagicType.ETH_ELEMENT, MagicType.ETH_FORM),
            (MagicType.PHYS_EFFECT, MagicType.PHYS_ELEMENT),
            (MagicType.PHYS_EFFECT, MagicType.ETH_ELEMENT),
            (MagicType.ETH_EFFECT, MagicType.PHYS_ELEMENT),
            (MagicType.ETH_EFFECT, MagicType.ETH_ELEMENT),
        ]

        return random.choice(spell_types)

    def get_random_spell(self, by_the_book: bool = True) -> str:
        """
        Get a spell with a random name

        :param by_the_book: bool, if True, the spell name will be generated according to the book
        """
        effect, form = self._get_spell_formula(by_the_book)

        # effect.name == effect.value
        # print(f"spell formula: {effect.name=} {effect.value=} {form.value=}")

        effect_data = self.load_json(MAGIC_TABLES[effect.value])
        form_data = self.load_json(MAGIC_TABLES[form.value])

        spell_name = (
            self.get_choice(effect_data),
            self.get_choice(form_data),
        )

        return ' '.join(spell_name).title()


if __name__ == '__main__':
    rand_mag = RandomMagic()
    for t in [True, True, False, False]:
        if t:
            print('By the book:')
        else:
            print('Random:')
        spell_name = rand_mag.get_random_spell(t)
        print(f'--- {spell_name}')
