from pathlib import Path

# Establish a path to this file
PATH_TO_DATASETS_FILE = Path(__file__)
# Path to SRC directory
SRC_DIRECTORY = PATH_TO_DATASETS_FILE.parent
# Path to project Root
MAUSRITTER_ROOT = SRC_DIRECTORY.parent
# Path to data folder
DATA_DIRECTORY = MAUSRITTER_ROOT / "data"

adventure_path: Path = DATA_DIRECTORY / "adventure"
ADVENTURE_PATHS = {
    "adventure_seeds": adventure_path / "adventure_seeds.json",
    "adventure_site": adventure_path / "adventure_site.json",
    "hex_details": adventure_path / "hex_details.json",
    "hex_type": adventure_path / "hex_type.json",
    "landmark_details": adventure_path / "landmark_details.json",
    "mouse_settlement": adventure_path / "mouse_settlement.json",
    "three_word_story": adventure_path / "three_word_story.json"
}

mice_path: Path = DATA_DIRECTORY / "mice"
MICE_PATHS = {
    "non_player_mice": mice_path / "non_player_mice.json",
    "player_mice": mice_path / "player_mice.json"
}
