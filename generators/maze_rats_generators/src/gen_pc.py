from random import randint

from generators.base_generator import Generator
from .datasets import PC_TABLES


class RandomPC(Generator):
    def __init__(self) -> None:
        super().__init__()

    def _select_pc_items(self) -> list:
        """Get a list of items"""
        item_data = self.load_json(PC_TABLES['ITEM'])
        return self.get_unique_choices(item_data, num_options=6)

    def describe_pc_items(self) -> str:
        """Get the items as a string"""
        return ', '.join(self._select_pc_items())

    def _select_pc_weapons(self) -> list:
        """Get the list of weapons for the PC"""
        weapon_data = self.load_json(PC_TABLES['WEAPON'])
        weapons = []

        # 50% chance of having a ranged weapon
        if randint(0, 1):
            range_weapon_data = self.load_json(PC_TABLES['RANGED_WEAPON'])
            weapons.append(self.get_choice(range_weapon_data))
            weapons.append(self.get_choice(weapon_data))
        else:
            weapons = (self.get_unique_choices(weapon_data, num_options=2))

        return weapons

    def describe_pc_weapons(self) -> str:
        """Get the weapons of the PC"""
        return ', '.join(self._select_pc_weapons())

    def _generate_pc_details(self) -> dict:
        """Get the details of the PC"""
        pc_details = {
            'items': self.describe_pc_items(),
            'appearance': self.get_choice(self.load_json(PC_TABLES['APPEARANCE'])),
            'physical_detail': self.get_choice(self.load_json(PC_TABLES['PYSICAL_DETAIL'])),
            'background': self.get_choice(self.load_json(PC_TABLES['BACKGROUND'])),
            'clothing': self.get_choice(self.load_json(PC_TABLES['CLOTHING'])),
            'personality': self.get_choice(self.load_json(PC_TABLES['PERSONALITY'])),
            'mannerism': self.get_choice(self.load_json(PC_TABLES['MANNERISM'])),
            'weapons': self.describe_pc_weapons(),
            'armor': 'shield, light armor',
        }

        return pc_details

    def describe_pc(self) -> str:
        """Get a description of the PC"""
        return '\n'.join(f'{k}: {v}' for k, v in self._generate_pc_details().items())


if __name__ == '__main__':
    pc = RandomPC()
    print(pc._select_pc_items(), end='\n\n')
    pc1 = pc._generate_pc_details()
    print(pc1, end='\n\n')
    print(pc.describe_pc())
