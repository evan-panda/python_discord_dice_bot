from pathlib import Path

current_file_path = Path(__file__)
src_dir = current_file_path.parent
generator_dir = src_dir.parent
DATA_PATH = str(generator_dir) + "/data/"

equipment_tables_path = DATA_PATH + "equipment_tables/"
EQUIPMENT_TABLES = {
    "WEAPON": equipment_tables_path + "weapon_items.json",
}

magic_tables_path = DATA_PATH + "magic_tables/"
MAGIC_TABLES = {
    "PHYS_EFFECT": magic_tables_path + "physical_effects.json",
    "PHYS_ELEMENT": magic_tables_path + "physical_elements.json",
    "PHYS_FORM": magic_tables_path + "physical_forms.json",
    "ETH_EFFECT": magic_tables_path + "ethereal_effects.json",
    "ETH_ELEMENT": magic_tables_path + "ethereal_elements.json",
    "ETH_FORM": magic_tables_path + "ethereal_forms.json",
    "INSANITY": magic_tables_path + "insantities.json",
    "MUTATION": magic_tables_path + "mutations.json",
    "OMEN_CATASTROPHY": magic_tables_path + "omens_magic_catastrophes.json",
}

monster_tables_path = DATA_PATH + "monster_tables/"
MONSTER_TABLES = {
    "MONSTER_AERIAL": monster_tables_path + "animal_aerial.json",
    "MONSTER_AQUATIC": monster_tables_path + "animal_aquatic.json",
    "MONSTER_TERRESTRIAL": monster_tables_path + "animal_terrestrial.json",
    "MONSTER_ABILITY": monster_tables_path + "monster_abilities.json",
    "MONSTER_FEATURE": monster_tables_path + "monster_features.json",
    "MONSTER_PERSONALITY": monster_tables_path + "monster_personality.json",
    "MONSTER_TACTIC": monster_tables_path + "monster_tactics.json",
    "MONSTER_TRAIT": monster_tables_path + "monster_traits.json",
    "MONSTER_WEAKNESS": monster_tables_path + "monster_weakness.json",
}

npc_tables_path = DATA_PATH + "npc_tables/"
NPC_TABLES = {
    "AFTER_PARTY": npc_tables_path + "after_the_party.json",
    "ASSET": npc_tables_path + "assets.json",
    "GOAL": npc_tables_path + "goals.json",
    "HOBBY": npc_tables_path + "hobbies.json",
    "LIABILITY": npc_tables_path + "liabilities.json",
    "METHOD": npc_tables_path + "methods.json",
    "MISFORTUNE": npc_tables_path + "misfortunes.json",
    "MISSION": npc_tables_path + "missions.json",
    "NAME_FEMALE": npc_tables_path + "name_female.json",
    "NAME_MALE": npc_tables_path + "name_male.json",
    "NAME_SURNAME_LOWER": npc_tables_path + "surname_lower.json",
    "NAME_SURNAME_UPPER": npc_tables_path + "surname_upper.json",
    "NPC_CIVILIZED": npc_tables_path + "npc_civilized.json",
    "NPC_UNDERWORLD": npc_tables_path + "npc_underworld.json",
    "NPC_WILDERNESS": npc_tables_path + "npc_wilderness.json",
    "RELATIONSHIP": npc_tables_path + "relationships.json",
    "REPUTATION": npc_tables_path + "reputations.json",
    "SECRET": npc_tables_path + "secrets.json",
}

pc_tables_path = DATA_PATH + "pc_tables/"
PC_TABLES = {
    "APPEARANCE": pc_tables_path + "appearance.json",
    "BACKGROUND": pc_tables_path + "background.json",
    "CLOTHING": pc_tables_path + "clothing.json",
    "ITEM": pc_tables_path + "item.json",
    "MANNERISM": pc_tables_path + "mannerism.json",
    "PERSONALITY": pc_tables_path + "personality.json",
    "PYSICAL_DETAIL": pc_tables_path + "physical_detail.json",
    "WEAPON": pc_tables_path + "weapon.json",
    "RANGED_WEAPON": pc_tables_path + "ranged_weapon.json",
}
