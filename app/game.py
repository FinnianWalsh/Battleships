import tkinter as tk
import tkinter.font as tk_font
from typing import Callable

from .constants import (
    grid as grid_consts,
    root as root_consts,
)
from .constants.root import ROOT_BACKGROUND_COLOR
from .grid_system import Grid, GridReferences, Cell
from .menu import Menu
from .placement_manager import PlacementManager
from .player import Player
from .util import hex_color_mut, Number, ratio_place


class Game:
    def __init__(self, root_width: Number = root_consts.DEFAULT_ROOT_WIDTH,
                 root_height: Number = root_consts.DEFAULT_ROOT_HEIGHT):
        self.player1 = Player()
        self.player2 = Player()

        root = tk.Tk()
        self.root = root

        self.root_width = root_width
        self.root_height = root_height
        self.root_size = f"{root_width}x{root_height}"

        root.title("Battleships")
        root.geometry(self.root_size)
        root.config(bg=ROOT_BACKGROUND_COLOR)
        root.resizable(False, False)

        self.turn = self.player1
        self.grid_refs = self.create_player_grids()

        self.menu = Menu(root, root_width, root_height, self.pvc_callback, self.pvp_callback)

    @staticmethod
    def game_over(other_grid: Grid) -> bool:
        for row in other_grid.cells:
            for cell in row:
                if cell.ship: return False

        return True

    @staticmethod
    def on_cell_enter(cell: Cell, _):
        cell.label.config(bg=grid_consts.CELL_DESTROY_COLOR)

    @staticmethod
    def on_cell_leave(cell: Cell, *_):
        if cell.destroyed: return

        cell.label.config(bg=grid_consts.GRID_COLOR)

    @property
    def other(self) -> Player:
        return self.player1 if self.turn == self.player2 else self.player2

    def pvc_callback(self, player_name: str):
        self.player1.name = player_name
        self.player2.name = "Computer"
        self.root.after(0, self.pvc_ship_placement_init)  # type: ignore[arg-type]

    def pvp_callback(self, player1_name: str, player2_name: str):
        self.player1.name = player1_name
        self.player2.name = player2_name
        self.root.after(0, self.pvp_ship_placement_init)  # type: ignore[arg-type]

    def create_player_grids(self) -> GridReferences:
        grid_master = tk.Frame(self.root, bg=ROOT_BACKGROUND_COLOR)

        grid_label_height = (1 - (grid_consts.RELATIVE_GRID_HEIGHT * 2 + grid_consts.RELATIVE_TURN_LABEL_HEIGHT)) / 2
        grid_color = hex_color_mut(ROOT_BACKGROUND_COLOR, lambda n: n * 1.2)

        grid_label_kwargs = {"bg": ROOT_BACKGROUND_COLOR, "font": tk_font.Font(family="TkSmallCaptionFont", size=20),
                             "fg": "#fafafa"}

        top_bar = tk.Label(grid_master, bg=ROOT_BACKGROUND_COLOR, text="Player's turn",
                           font=tk_font.Font(family="TkHeadingFont", size=24),
                           fg="#ffffff")

        top_bar.place(relwidth=1.0, relheight=grid_consts.RELATIVE_TURN_LABEL_HEIGHT, relx=0.5, rely=0, anchor="n")

        rotation_label_ratio_placement_kwargs = {"parent_width": self.root_width,
                                                 "parent_height": self.root_height,
                                                 "relwidth": grid_consts.RELATIVE_ROTATION_LABEL_SIZE,
                                                 "relheight": grid_consts.RELATIVE_ROTATION_LABEL_SIZE}

        grid1_label = tk.Label(grid_master, text=f"Player1's grid_system", **grid_label_kwargs)
        grid1_clockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)
        grid1_anticlockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)

        grid1_label_rely = grid_consts.RELATIVE_TURN_LABEL_HEIGHT

        grid1_label.place(relwidth=1.0, relheight=grid_label_height, relx=0.5,
                          rely=grid1_label_rely, anchor="n")

        ratio_place(grid1_clockwise_rotation_label, **rotation_label_ratio_placement_kwargs, relx=1,
                    rely=grid1_label_rely + grid_label_height / 2, anchor="e")
        ratio_place(grid1_anticlockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
                    rely=grid1_label_rely + grid_label_height / 2, anchor="w")

        grid2_label = tk.Label(grid_master, text="Player2's grid_system", **grid_label_kwargs)
        grid2_clockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)
        grid2_anticlockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)

        grid2_label_rely = grid_consts.RELATIVE_TURN_LABEL_HEIGHT + grid_label_height + grid_consts.RELATIVE_GRID_HEIGHT

        grid2_label.place(relwidth=1.0, relheight=grid_label_height, relx=0.5, rely=grid2_label_rely, anchor="n")

        ratio_place(grid2_clockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
                    relx=1.0, rely=grid2_label_rely + grid_label_height / 2, anchor="e")
        ratio_place(grid2_anticlockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
                    rely=grid2_label_rely + grid_label_height / 2, anchor="w")

        grid1 = Grid.create(self.root_width, self.root_height, grid_master, bg=grid_color)

        ratio_place(grid1.frame, self.root_width, self.root_height, grid_consts.RELATIVE_GRID_WIDTH,
                    grid_consts.RELATIVE_GRID_HEIGHT, anchor="n", relx=0.5,
                    rely=grid_consts.RELATIVE_TURN_LABEL_HEIGHT + grid_label_height)

        grid2 = Grid.create(self.root_width, self.root_height, grid_master, bg=grid_color)

        ratio_place(grid2.frame, self.root_width, self.root_height, grid_consts.RELATIVE_GRID_WIDTH,
                    grid_consts.RELATIVE_GRID_HEIGHT, relx=0.5,
                    rely=grid_consts.RELATIVE_TURN_LABEL_HEIGHT + grid_label_height * 2 + grid_consts.RELATIVE_GRID_HEIGHT,
                    anchor="n")

        return GridReferences(grid_master=grid_master, grid1=grid1, grid1_label=grid1_label,
                              grid1_clockwise_rotation_label=grid1_clockwise_rotation_label,
                              grid1_anticlockwise_rotation_label=grid1_anticlockwise_rotation_label, grid2=grid2,
                              grid2_label=grid2_label, grid2_clockwise_rotation_label=grid2_clockwise_rotation_label,
                              grid2_anticlockwise_rotation_label=grid2_anticlockwise_rotation_label,
                              top_bar=top_bar)

    def pvc_computer_place_ships(self, _=None):
        grid_refs = self.grid_refs

        top_bar = grid_refs.top_bar
        base_text = "Computer's turn to place"
        iterations = 4
        max_periods = 3
        pause_ms = 333

        def load(i: int, iteration: int):
            if iteration >= iterations: return

            top_bar.config(text=f"{base_text}{'.' * i}")

            if i == max_periods:
                top_bar.after(pause_ms, load, 0, iteration + 1)
            else:
                top_bar.after(pause_ms, load, i + 1, iteration)

        top_bar.after(0, load, 0, 0)

    def pvc_ship_placement_init(self):
        print(f"Welcome, {self.player1.name}")
        grid_refs = self.grid_refs

        grid_refs.grid1_label.config(text="Your grid")
        grid_refs.grid2_label.config(text="Computer's grid")

        grid_refs.top_bar.config(text=f"Place your ships")
        grid_refs.grid_master.place(relwidth=1, relheight=1)

        player_grid = grid_refs.grid1

        PlacementManager(player_grid, grid_refs.grid1_clockwise_rotation_label,
                         grid_refs.grid1_anticlockwise_rotation_label, self.pvc_computer_place_ships)()

    def pvp_ship_placement_init(self):
        grid_refs = self.grid_refs
        grid_refs.grid1_label.config(text=f"{self.player1.name}'s grid")
        grid_refs.grid2_label.config(text=f"{self.player2.name}'s grid")

        self.pvp_place_ships(self.player1)
        grid_refs.grid_master.place(relwidth=1, relheight=1)

    def pvp_place_ships(self, player: Player):
        grid_refs = self.grid_refs
        grid_refs.top_bar.config(text=f"{player.name}'s turn to place")

        grid_name = f"grid{player.instance}"

        def callback(grid: Grid):
            grid.hide_ships()

            if player.instance == Player.instances:
                grid.frame.after(0, self.play_pvp)  # type: ignore[arg-type]
            else:
                grid.frame.after(0, self.pvp_place_ships, getattr(self, f"player{player.instance + 1}"))

        PlacementManager(getattr(grid_refs, grid_name), getattr(grid_refs, f"{grid_name}_clockwise_rotation_label"),
                         getattr(grid_refs, f"{grid_name}_anticlockwise_rotation_label"), callback)()

    def player_turn(self, player: Player, player_grid: Grid, other_player: Player, other_grid: Grid,
                    callback: Callable[[Player], None]):

        turn_label = self.grid_refs.top_bar
        turn_label.config(text=f"{player.name}'s turn")

        def cell_button1(cell: Cell, _):
            if cell.destroyed: return

            other_grid.cell_unbind("<Enter>")
            other_grid.cell_unbind("<Leave>")
            other_grid.cell_unbind("<Button-1>")

            if cell.ship:
                cell.destroy("X")
                turn_label.config(text="Hit!")
            else:
                cell.destroy()
                turn_label.config(text="Miss!")

            args = (callback, player) if Game.game_over(other_grid) else (self.player_turn, other_player, other_grid,
                                                                          player, player_grid, callback)
            cell.label.after(1000, *args)

        other_grid.cell_bind("<Enter>", Game.on_cell_enter)
        other_grid.cell_bind("<Leave>", Game.on_cell_leave)
        other_grid.cell_bind("<Button-1>", cell_button1)

    def play_pvc(self):
        print(f"Playing {self.player1.name} vs computer")

    def player_won(self, player: Player):
        interval_ms = 150
        iterations = 25

        def set_red(top_bar: tk.Label, count: int):
            if count >= iterations: return self.prompt_play_again()
            top_bar.config(fg="#ffd700")  # gold
            top_bar.after(interval_ms, set_white, top_bar, count)

        def set_white(top_bar: tk.Label, count: int):
            top_bar.config(fg="white")
            top_bar.after(interval_ms, set_red, top_bar, count + 1)

        grid_refs = self.grid_refs
        grid_refs.top_bar.config(text=f"{player.name} has won!")
        set_red(grid_refs.top_bar, 1)

    def play_pvp(self):
        print(f"Player {self.player1.name} vs {self.player2.name}")
        grid_refs = self.grid_refs

        self.player_turn(self.player1, grid_refs.grid1, self.player2, grid_refs.grid2, self.player_won)

    def prompt_play_again(self):
        popup = tk.Toplevel()
        popup.title("Play again?")

        if False: self.restart()

    def switch_grid(self):  # for pvp
        grid_refs = self.grid_refs
        grid_refs.top_bar.config(text=f"{self.turn.name}'s turn")
        grid_refs.grid2_label.config(text=f"{self.other.name}'s field")

    def start(self):
        self.menu.place()
        self.root.mainloop()

    def restart(self):
        self.player1 = Player.from_other(self.player1)
        self.player2 = Player.from_other(self.player2)
        self.grid_refs.grid_master.place_forget()
        self.menu.place()
