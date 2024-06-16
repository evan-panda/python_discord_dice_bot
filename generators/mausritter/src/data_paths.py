from pathlib import Path


# Establish a path to this file
PATH_TO_DATASETS_FILE = Path(__file__)
# Path to SRC directory
SRC_DIRECTORY = PATH_TO_DATASETS_FILE.parent
# Path to project Root
MAUSRITTER_ROOT = SRC_DIRECTORY.parent
# Path to data folder
DATA_DIRECTORY = MAUSRITTER_ROOT / "data"

ADVENTUR_PATHS = {
    "adventure_seeds": DATA_DIRECTORY / "adventure/adventure_seeds.json",
    "hex_details": DATA_DIRECTORY / "adventure/hex_details.json"
}

MICE_PATH = {
    "non_player_mice": DATA_DIRECTORY / "mice/non_player_mice.json",
    "player_mice": DATA_DIRECTORY / "mice/player_mice.json"
}
