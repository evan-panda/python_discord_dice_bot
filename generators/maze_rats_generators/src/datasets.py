from pathlib import Path

current_file_path = Path(__file__)
src_folder = current_file_path.parent
DATA_PATH = str(src_folder.parent) + "/data"

magic_tables_path = DATA_PATH + "/magic_tables"
MAGIC_TABLES = {
    "PHYS_EFFECT": magic_tables_path + "/physical_effects.json",
    "PHYS_ELEMENT": magic_tables_path + "/physical_elements.json",
    "PHYS_FORM": magic_tables_path + "/physical_forms.json",
    "ETH_EFFECT": magic_tables_path + "/ethereal_effects.json",
    "ETH_ELEMENT": magic_tables_path + "/ethereal_elements.json",
    "ETH_FORM": magic_tables_path + "/ethereal_forms.json",
}

monster_tables_path = DATA_PATH + "/monster_tables"
MONSTER_TABLES = {
    "MONSTER_AERIAL": monster_tables_path + "/animal_aerial.json",
    "MONSTER_AQUATIC": monster_tables_path + "/animal_aquatic.json",
    "MONSTER_TERRESTRIAL": monster_tables_path + "/animal_terrestrial.json",
}

npc_tables_path = DATA_PATH + "/npc_tables"
NPC_TABLES = {
    "NAME_FEMALE": npc_tables_path + "/name_female.json",
    "NAME_MALE": npc_tables_path + "/name_male.json",
    "NAME_SURNAME_LOWER": npc_tables_path + "/surname_lower.json",
    "NAME_SURNAME_UPPER": npc_tables_path + "/surname_upper.json",
}

pc_tables_path = DATA_PATH + "/pc_tables"
PC_TABLES = {
    "APPEARANCE": pc_tables_path + "/appearance.json",
    "BACKGROUND": pc_tables_path + "/background.json",
    "CLOTHING": pc_tables_path + "/clothing.json",
    "ITEM": pc_tables_path + "/item.json",
    "MANNERISM": pc_tables_path + "/mannerism.json",
    "PERSONALITY": pc_tables_path + "/personality.json",
    "PYSICAL_DETAIL": pc_tables_path + "/physical_detail.json",
    "WEAPON": pc_tables_path + "/weapon.json",
    "RANGED_WEAPON": pc_tables_path + "/ranged_weapon.json",
}
