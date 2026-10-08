# handles the adding and removing part

from tkinter import filedialog
from pathlib import Path

# other file imports

import storage

# adding

def add(games, create_game_button):
    path = filedialog.askopenfilename( # ask for path of game
        title="Choose a game",

        # file types (exe, lnk, ...)
        filetypes=[
            ("Executable files", "*.exe"),
            ("Shortcut files", "*.lnk"),
            ("All files", "*.*"),
        ]
    )

    # checking if path exists
    if path:

        game_name = Path(path).stem # getting name of path

        if game_name in games:
            print("No Duplicates Allowed")
            return

        games[game_name] = {
        "path": path,
        "color": "#666460",
        "launched_count": 0,
        }

        create_game_button(game_name)

        storage.save_games(games) # call saving func

        print(f"Added: {game_name}")
        print(f"Path: {path}")


# removing

def remove_game(game_name, games, game_frames, game_buttons, launch_labels):

    if game_name not in games:
        return

    del games[game_name]
    game_frames.pop(game_name).destroy()
    game_buttons.pop(game_name, None)
    launch_labels.pop(game_name, None)



    storage.save_games(games)

    print(f"Removed {game_name}")

