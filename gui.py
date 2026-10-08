import tkinter as tk
import os

# other files import

import storage
import game_manager


class GameLauncher:

    def __init__(self):

        self.games = storage.load_games()

        # main window
        self.root = tk.Tk()
        self.root.title("Game Launcher")
        self.root.geometry("1000x700")
        self.root.config(bg="#515953")


        # big three widgets
        self.game_frames = {}
        self.game_buttons = {}
        self.launch_labels = {}

        self.make_main()

        for game_name in self.games:
            self.create_game_buttons(game_name)

    def make_main(self):
        self.title_label = tk.Label(
            self.root,
            text="MY GAME LAUNCHER",
            bg="#6d756f",
        )
        self.title_label.pack(pady=2)

        self.add_button()

    def add_game(self):
        game_manager.add(self.games, self.create_game_buttons)

    def add_button(self):
        self.button = tk.Button(
        self.root,
        text = "Add",
        command=self.add_game,
        bg="#00f531",
        height=2,
        width=6,
    )
        self.button.pack(pady=10)

    def create_game_buttons(self, game_name):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        frame.config(bg="#515953")

        button = tk.Button(
            frame,
            text=game_name,
            command= lambda: self.launch_game(game_name),
            width=40,
            height=4,
            bg="#4e5859",
        )
        button.pack(side=tk.LEFT)

        self.game_frames[game_name] = frame
        self.game_buttons[game_name] = button

        self.remove_game_button(frame, game_name)
        self.launched_count(frame, game_name)
        self.edit_buttons(frame, game_name)


    def remove_game_button(self, frame, game_name):
        button = tk.Button(
            frame,
            text="❌",
            fg="red",
            command= lambda: game_manager.remove_game(
                game_name,
                self.games,
                self.game_frames,
                self.game_buttons,
                self.launch_labels,
            )
        )
        button.pack(side=tk.RIGHT, padx=5)

    def launch_game(self, game_name):
        path = self.games[game_name]["path"]

        try:
            os.startfile(path)

            # increase launch count
            self.games[game_name]["launched_count"] = (
                self.games[game_name].get("launched_count", 0) + 1
            )

            # update label
            self.launch_labels[game_name].config(
                text=f"Launched Count: {self.games[game_name]['launched_count']}"
            )

            storage.save_games(self.games)

        except OSError as e:
            print(f"Could not launch {game_name}: {e}")

    def launched_count(self, frame, game_name):

        label_launch = tk.Label(
            frame,
            text=f"Launched Count: {self.games[game_name].get('launched_count', 0)}",
            width=15,
            height=1,
            bg="#869191",
        )
        label_launch.pack(side=tk.LEFT)

        self.launch_labels[game_name] = label_launch

    def edit_ok(self, box, game_name, popup):
        value = box.get().strip()

        self.game_buttons[game_name].config(bg=value)
        self.games[game_name]["color"] = value

        popup.destroy()
        storage.save_games(self.games)

    def edit(self, game_name):
        popup = tk.Toplevel(self.root)
        popup.title("Color")
        popup.geometry("200x100")

        hex_label = tk.Label(popup, text="Hexcode color:", fg="gray")
        hex_label.pack(pady=2, padx=2)

        input_box = tk.Entry(popup)
        input_box.pack(pady=2, padx=2)

        ok_button = tk.Button(
            popup,
            text="OK",
            command=lambda box=input_box, game=game_name, pop_up=popup: self.edit_ok(box, game, pop_up)
        )
        ok_button.pack(pady=2, padx=2)

    def edit_buttons(self, frame, game_name):

        # making pencil infront of game

        edit_button = tk.Button(
            frame,
            text="✏️",
            bg="#3998ad",
            command=lambda game=game_name: self.edit(game),
        )
        edit_button.pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop()