from random import randint, shuffle

from generators.base_generator import Generator
from .datasets import NPC_TABLES, PC_TABLES


class RandomPC(Generator):
    def __init__(self) -> None:
        """Class for generating random PC details"""
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

    def _generate_pc_stats(self) -> list[int]:
        """Get the stats of the PC"""
        stats = [0, 1, 2]
        shuffle(stats)
        return stats

    def describe_pc_stats(self) -> str:
        """Create the stats str for the PC"""
        stats = self._generate_pc_stats()
        return f'STR: {stats[0]}, DEX: {stats[1]}, WIL: {stats[2]}'

    def _generate_pc_names(self) -> list[str]:
        """Get the name options for the PC"""
        m_name = self.load_json(NPC_TABLES['NAME_MALE'])
        f_name = self.load_json(NPC_TABLES['NAME_FEMALE'])
        u_name = self.load_json(NPC_TABLES['NAME_SURNAME_UPPER'])
        l_name = self.load_json(NPC_TABLES['NAME_SURNAME_LOWER'])

        m_name = self.get_choice(m_name)
        f_name = self.get_choice(f_name)
        u_name = self.get_choice(u_name)
        l_name = self.get_choice(l_name)

        return m_name, f_name, u_name, l_name

    def describe_pc_names(self) -> str:
        """Create the names str for the PC"""
        m_name, f_name, u_name, l_name = self._generate_pc_names()
        return f'{m_name} (m) / {f_name} (f) | {u_name} / {l_name}'

    def _generate_pc_details(self) -> dict:
        """Get the details of the PC"""
        pc_details = {
            'stats': self.describe_pc_stats(),
            'items': self.describe_pc_items(),
            'appearance': self.get_choice(self.load_json(PC_TABLES['APPEARANCE'])),
            'physical detail': self.get_choice(self.load_json(PC_TABLES['PYSICAL_DETAIL'])),
            'clothing': self.get_choice(self.load_json(PC_TABLES['CLOTHING'])),
            'background': self.get_choice(self.load_json(PC_TABLES['BACKGROUND'])),
            'personality': self.get_choice(self.load_json(PC_TABLES['PERSONALITY'])),
            'mannerism': self.get_choice(self.load_json(PC_TABLES['MANNERISM'])),
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
