# handles the save and load features

from pathlib import Path
import json
import os


DATA_DIR = Path(os.getenv("APPDATA")) / "GameLauncher"
DATA_DIR.mkdir(parents=True, exist_ok=True)
GAMES_FILE = DATA_DIR / "games.json"


def save_games(games):

    with open(GAMES_FILE, "w") as file:
        json.dump(games, file, indent=4)


def load_games():

    try:
        with open(GAMES_FILE, "r") as file:
           data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}