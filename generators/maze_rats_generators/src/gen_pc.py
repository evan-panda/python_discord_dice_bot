from random import choice, shuffle

from generators.base_generator import Generator
from .datasets import NPC_TABLES, PC_TABLES


class RandomPC(Generator):
    NUM_UNIQUE: int = 4
    last_x_appearance: list = []
    last_x_backgrounds: list = []
    last_x_clothing: list = []
    last_x_mannerisms: list = []
    last_x_names_female: list = []
    last_x_names_last: list = []
    last_x_names_male: list = []
    last_x_personality: list = []
    last_x_physical_details: list = []

    def __init__(self) -> None:
        """Class for generating random PC details"""
        super().__init__()

    def _select_pc_items(self) -> list[str]:
        """Get a list of items"""
        item_data = self.load_json(PC_TABLES['ITEM'])
        return self.get_unique_choices(item_data, num_options=6)

    def describe_pc_items(self) -> str:
        """Get the items as a string"""
        return ', '.join(self._select_pc_items())

    def _select_pc_weapons(self) -> list[str]:
        """Get the list of weapons for the PC"""
        weapon_data = self.load_json(PC_TABLES['WEAPON'])
        weapons = []

        # 50% chance of having a ranged weapon
        if choice([True, False]):
            range_weapon_data = self.load_json(PC_TABLES['RANGED_WEAPON'])
            weapons.append(self.get_choice(range_weapon_data))
            weapons.append(self.get_choice(weapon_data))
        else:
            weapons = (self.get_unique_choices(weapon_data, num_options=2))

        return weapons

    def describe_pc_weapons(self) -> str:
        """Get the weapons of the PC"""
        return ', '.join(self._select_pc_weapons())

    def _generate_pc_stats(self) -> list[int]:
        """Get the stats of the PC"""
        stats = [0, 1, 2]
        shuffle(stats)
        return stats

    def describe_pc_stats(self) -> str:
        """Create the stats str for the PC"""
        stats = self._generate_pc_stats()
        return f'STR: {stats[0]}, DEX: {stats[1]}, WIL: {stats[2]}'

    def _get_unique_choice(self, choices: list[str], last_x: list[str]) -> str:
        """Returns an item that isn't already in the given list"""
        item = self.get_choice(choices)
        while (item in last_x):
            item = self.get_choice(choices)

        if len(last_x) == self.NUM_UNIQUE:
            last_x.pop(0)

        last_x.append(item)

        return item

    def _generate_pc_names(self) -> list[str]:
        """Get the name options for the PC"""
        m_names = self.load_json(NPC_TABLES['NAME_MALE'])
        f_names = self.load_json(NPC_TABLES['NAME_FEMALE'])
        u_names = self.load_json(NPC_TABLES['NAME_SURNAME_UPPER'])
        l_names = self.load_json(NPC_TABLES['NAME_SURNAME_LOWER'])

        m_name = self._get_unique_choice(m_names, self.last_x_names_male)
        f_name = self._get_unique_choice(f_names, self.last_x_names_female)
        u_name = self._get_unique_choice(u_names, self.last_x_names_last)
        l_name = self._get_unique_choice(l_names, self.last_x_names_last)

        return m_name, f_name, u_name, l_name

    def describe_pc_names(self) -> str:
        """Create the names str for the PC"""
        m_name, f_name, u_name, l_name = self._generate_pc_names()
        return f'{m_name} (m) / {f_name} (f) | {u_name} / {l_name}'

    def _generate_pc_details(self) -> dict[str, str]:
        """Get the details of the PC"""
        pc_details = {
            'stats': self.describe_pc_stats(),
            'items': self.describe_pc_items(),
            'appearance': self._get_unique_choice(self.load_json(PC_TABLES['APPEARANCE']), self.last_x_appearance),
            'physical detail': self._get_unique_choice(self.load_json(PC_TABLES['PYSICAL_DETAIL']), self.last_x_physical_details),  # noqa: E501
            'clothing': self._get_unique_choice(self.load_json(PC_TABLES['CLOTHING']), self.last_x_clothing),
            'background': self._get_unique_choice(self.load_json(PC_TABLES['BACKGROUND']), self.last_x_backgrounds),
            'personality': self._get_unique_choice(self.load_json(PC_TABLES['PERSONALITY']), self.last_x_personality),
            'mannerism': self._get_unique_choice(self.load_json(PC_TABLES['MANNERISM']), self.last_x_mannerisms),
            'weapons': self.describe_pc_weapons(),
            'armor': 'shield, light armor',
            'hp': '4',
            'name': self.describe_pc_names(),
        }

        return pc_details

    def describe_pc(self) -> str:
        """Get a description of the PC"""
        return '\n'.join(f'**{k.upper()}:** {v}' for k, v in self._generate_pc_details().items())


if __name__ == '__main__':
    pc = RandomPC()
    print(pc._select_pc_items(), end='\n\n')
    pc1 = pc._generate_pc_details()
    print(pc1, end='\n\n')
    print(pc.describe_pc())
