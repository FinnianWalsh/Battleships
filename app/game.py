import threading
import tkinter as tk
import tkinter.font as tk_font

from .constants import (
    grid as grid_consts,
    misc as misc_consts,
    root as root_consts,
    rules as rules_consts
)
from .constants.root import ROOT_BACKGROUND_COLOR
from .field import Grid, GridData, Cell
from .player import Player
from .ship import Ship, Direction
from .util import create_bar, create_table, hex_color_mut, Number, ratio_place

from enum import Enum
from time import perf_counter, sleep
from typing import Callable


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
        self.background_color = ROOT_BACKGROUND_COLOR

        root.title("Battleships")
        root.geometry(self.root_size)
        root.config(bg=self.background_color)
        root.resizable(False, False)

        self.turn = self.player1
        self.grid_data = self.create_player_grids()
        self.menu, self.reset_menu = self.create_menu()

    @property
    def other(self) -> Player:
        if self.turn == self.player1:
            return self.player2
        else:
            return self.player1

    def create_menu(self) -> (tk.Frame, Callable[[], None]):
        bg_color = self.background_color

        menu = tk.Frame(self.root, bg=bg_color)

        relative_rules_head_offset = 5 / self.root_height
        relative_rules_head_size = 30 / self.root_height

        rules_head = tk.Label(menu, text="Rules")
        rules_head.config(font=tk_font.Font(family="Helvetica", size=20, weight="bold"), fg="#ffffff",
                          bg=bg_color)
        rules_head.place(relwidth=1.0, rely=relative_rules_head_offset, relheight=relative_rules_head_size)

        relative_rules_label_offset = relative_rules_head_offset + relative_rules_head_size
        relative_rules_label_height = 180 / self.root_height

        rules_label = tk.Label(menu, text=rules_consts.text, anchor="n", wraplength=self.root_width - 50)
        rules_label.config(font=tk_font.Font(family="Helvetica", size=14), fg="#ffffff", bg=bg_color)
        rules_label.place(relwidth=1.0, rely=relative_rules_label_offset, relheight=relative_rules_label_height)

        relative_base_component_padding = 20 / self.root_height
        relative_rules_table_offset = relative_rules_label_offset + relative_rules_label_height + relative_base_component_padding

        table_columns, table_rows = 2, len(rules_consts.SHIP_SETUP) + 1
        relative_rules_table_height = 200 / self.root_height
        relative_rules_table_width_subtraction = -50 / self.root_width
        rules_table = tk.Frame(menu, bg=bg_color)

        rules_table.place(relwidth=1, width=relative_rules_table_width_subtraction,
                          relheight=relative_rules_table_height, relx=0.5, rely=relative_rules_table_offset, anchor="n")

        relative_rules_bar_height = 4 / self.root_height

        table_contents, row_height = create_table(rules_table, table_columns, table_rows, [],
                                                  [0, relative_rules_bar_height * 5], bg=self.background_color,
                                                  font=tk_font.Font(family="Helvetica", size=14), fg="#ffffff")

        first_row = table_contents[0]
        first_row[0].config(text="Name", anchor="center")
        first_row[1].config(text="Length", anchor="center")

        for i in range(table_rows - 1):
            row = table_contents[i + 1]
            ship = rules_consts.SHIP_SETUP[i]
            row[0].config(text=ship["class"].__name__, anchor="center")
            row[1].config(text=ship["length"], anchor="center")

        create_bar(rules_table, relwidth=1 + relative_rules_table_width_subtraction, relx=0.5, rely=row_height,
                   anchor="n")

        relative_mode_selection_offset = relative_rules_table_offset + relative_rules_table_height + relative_base_component_padding
        relative_mode_selection_height = 150 / self.root_height

        relative_entries_frame_offset = relative_mode_selection_offset + relative_mode_selection_height + relative_base_component_padding
        relative_entries_frame_width = 1 - 20 / self.root_width
        relative_entries_frame_height = 80 / self.root_height

        mode_selection_color_unselected = hex_color_mut(bg_color, lambda n: n * 0.9)
        mode_selection_color_selected = hex_color_mut(mode_selection_color_unselected, lambda n: n * 0.9)
        mode_selection_color_hover = hex_color_mut(mode_selection_color_unselected, lambda n: n * 0.8)

        mode_selection_frame = tk.Frame(menu, bg=mode_selection_color_unselected)
        mode_selection_frame.place(relwidth=relative_entries_frame_width,
                                   relheight=relative_mode_selection_height, relx=0.5,
                                   rely=relative_mode_selection_offset, anchor="n")

        mode_btn_width, mode_btn_height = 1.0, 0.38461538461
        mode_header_height = 1 - 2 * mode_btn_height

        mode_header = tk.Label(mode_selection_frame, bg=mode_selection_color_unselected, text="Select mode:",
                               fg="#ffffff")
        mode_header.place(relwidth=1.0, relheight=mode_header_height, relx=0.5, anchor="n")

        pvc_btn = tk.Label(mode_selection_frame, bg=mode_selection_color_unselected, text="Player VS Computer",
                           fg="#ffffff")
        pvc_btn.place(relwidth=mode_btn_width, relheight=mode_btn_height, relx=0.5, rely=mode_header_height, anchor="n")

        pvp_btn = tk.Label(mode_selection_frame, bg=mode_selection_color_unselected, text="Player VS Player",
                           fg="#ffffff")
        pvp_btn.place(relwidth=mode_btn_width, relheight=mode_btn_height, relx=0.5,
                      rely=mode_header_height + mode_btn_height, anchor="n")

        entries_frame = tk.Frame(menu, bg=bg_color)
        entries_frame.place(relwidth=relative_entries_frame_width, relheight=relative_entries_frame_height, relx=0.5,
                            rely=relative_entries_frame_offset, anchor="n")

        entry_component_relative_height = 0.4

        entry_background_color = hex_color_mut(bg_color, lambda n: n * 1.5)

        entry_label_relative_width = 0.4
        entry_instance_relative_width = 1 - entry_label_relative_width

        player1_entry_label = tk.Label(entries_frame, bg=entry_background_color,
                                       fg="#ffffff")
        player1_entry = tk.Entry(entries_frame, bg=entry_background_color, fg="#ffffff")

        player2_entry_relative_offset = 1 - entry_component_relative_height * 2 + entry_component_relative_height

        player2_entry = tk.Entry(entries_frame, bg=entry_background_color, fg="#ffffff")

        player2_entry_label = tk.Label(entries_frame, text="Enter player 2 name:", bg=entry_background_color,
                                       fg="#ffffff")

        options = Enum("Mode", ["none", "PVP", "PVC"])
        selected_mode = options.none

        def unselect_mode(btn: tk.Label):
            nonlocal selected_mode

            selected_mode = options.none

            btn.config(bg=mode_selection_color_unselected)

            player1_entry_label.place_forget()
            player1_entry.place_forget()

            player2_entry_label.place_forget()
            player2_entry.place_forget()

        def on_pvc_btn_click(_=None):
            nonlocal selected_mode

            if selected_mode == options.PVC: return unselect_mode(pvc_btn)

            selected_mode = options.PVC

            pvc_btn.config(bg=mode_selection_color_selected)
            pvp_btn.config(bg=mode_selection_color_unselected)

            player1_entry_label.place(relwidth=entry_label_relative_width, relheight=entry_component_relative_height)
            player1_entry_label.config(text="Enter player name:")
            player1_entry.place(relwidth=entry_instance_relative_width, relheight=entry_component_relative_height,
                                relx=entry_label_relative_width)

            player2_entry_label.place_forget()
            player2_entry.place_forget()

        pvc_btn.bind("<Button-1>", on_pvc_btn_click)

        def on_pvp_btn_clicked(_=None):
            nonlocal selected_mode

            if selected_mode == options.PVP: return unselect_mode(pvp_btn)

            selected_mode = options.PVP

            pvc_btn.config(bg=mode_selection_color_unselected)
            pvp_btn.config(bg=mode_selection_color_selected)

            player1_entry_label.place(relwidth=entry_label_relative_width, relheight=entry_component_relative_height)
            player1_entry_label.config(text="Enter player 1 name:")
            player1_entry.place(relwidth=entry_instance_relative_width, relheight=entry_component_relative_height,
                                relx=entry_label_relative_width)

            player2_entry.place(relwidth=entry_instance_relative_width, relheight=entry_component_relative_height,
                                relx=entry_label_relative_width, rely=player2_entry_relative_offset)
            player2_entry_label.place(relwidth=entry_label_relative_width, relheight=entry_component_relative_height,
                                      rely=player2_entry_relative_offset)

        pvp_btn.bind("<Button-1>", on_pvp_btn_clicked)

        def on_mode_btn_enter(event):
            event.widget.config(bg=mode_selection_color_hover)

        pvc_btn.bind("<Enter>", on_mode_btn_enter)
        pvp_btn.bind("<Enter>", on_mode_btn_enter)

        def on_pvc_btn_leave(_=None):
            pvc_btn.config(bg=mode_selection_color_selected if selected_mode == options.PVC
            else mode_selection_color_unselected)

        pvc_btn.bind("<Leave>", on_pvc_btn_leave)

        def on_pvp_btn_leave(_=None):
            pvp_btn.config(bg=mode_selection_color_selected if selected_mode == options.PVP
            else mode_selection_color_unselected)

        pvp_btn.bind("<Leave>", on_pvp_btn_leave)

        relative_start_btn_offset = -10 / self.root_height
        relative_start_btn_width = 80 / self.root_width
        relative_start_btn_height = 30 / self.root_height

        start_btn = tk.Button(menu, text="Start", bg="#00ff00")
        start_btn.place(relwidth=relative_start_btn_width, relheight=relative_start_btn_height, relx=0.5,
                        rely=1 + relative_start_btn_offset, anchor="s")

        relative_warning_label_offset = relative_start_btn_offset * 2 - relative_start_btn_height

        warning_label = tk.Label(menu, text="", bg=self.background_color, fg="#ff0000")
        warning_label.place(relwidth=1.0, relheight=relative_start_btn_height, relx=0.5,
                            rely=1 + relative_warning_label_offset, anchor="s")
        last_warning = 0

        has_started = False

        def can_start_pvc() -> str | None:
            if not len(player_entry_text := player1_entry.get()): return "Enter player name!"
            if player_entry_text == "Computer": return "You cannot name yourself 'Computer'!"
            if len(player_entry_text) > misc_consts.MAX_NAME_LENGTH:
                return f"Player names must be no more than {misc_consts.MAX_NAME_LENGTH} characters long!"

            return None

        def can_start_pvp() -> str | None:
            player2_entry_text = player2_entry.get()

            if not len(player1_entry_text := player1_entry.get()):
                if len(player2_entry_text):
                    return "Enter player 1 name!"
                else:
                    return "Enter player names!"
            if not len(player2_entry_text): return "Enter player 2 name!"
            if len(player1_entry_text) > misc_consts.MAX_NAME_LENGTH or len(
                    player2_entry_text) > misc_consts.MAX_NAME_LENGTH:
                return f"Player names must be no more than {misc_consts.MAX_NAME_LENGTH} characters long!"
            if player1_entry_text == player2_entry_text: return "Enter two different names!"

            return None

        warning_duration = 2

        def clear_warning(warning_time: float):
            sleep(warning_duration)

            if warning_time == last_warning:
                warning_label.after(0, lambda: warning_label.config(text=""))  # type: ignore[arg-type]

        def warn(warning: str):
            nonlocal last_warning

            this_warning = perf_counter()
            last_warning = this_warning
            warning_label.config(text=warning)

            threading.Thread(target=clear_warning, daemon=True, args=(this_warning,)).start()

        def reset_text():
            delay = 2
            sleep(delay)

            if not has_started:
                start_btn.after(0, lambda _: start_btn.config(text="Start"))  # type: ignore[arg-type]

        def check_confirmation():
            start_btn.config(text="Confirm")
            threading.Thread(target=reset_text, daemon=True).start()

        def on_start(_: tk.Event):
            nonlocal has_started

            if has_started:
                warn("Game has already started!")
            elif selected_mode == options.none:
                warn("Select a mode!")
            elif selected_mode == options.PVC:
                if warning := can_start_pvc():
                    warn(warning)
                elif start_btn.cget("text") == "Confirm":
                    has_started = True
                    menu.place_forget()
                    self.player1.name = player1_entry.get()
                    self.player2.name = "Computer"
                    self.pvc_ship_placement()
                else:
                    check_confirmation()
            elif selected_mode == options.PVP:
                if warning := can_start_pvp():
                    warn(warning)
                elif start_btn.cget("text") == "Confirm":
                    has_started = True
                    menu.place_forget()
                    self.player1.name = player1_entry.get()
                    self.player2.name = player2_entry.get()
                    self.pvp_ship_placement()
                else:
                    check_confirmation()

        start_btn.bind("<Button-1>", on_start)

        def reset_menu():
            unselect_mode(pvc_btn)
            pvp_btn.config(bg=mode_selection_color_unselected)

        return menu, reset_menu

    def place_menu(self):
        self.menu.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    def create_player_grids(self) -> GridData:
        bg_color: str = self.background_color

        grid_master = tk.Frame(self.root, bg=bg_color)

        grid_label_height = (1 - (grid_consts.RELATIVE_GRID_HEIGHT * 2 + grid_consts.RELATIVE_TURN_LABEL_HEIGHT)) / 2
        grid_color = hex_color_mut(bg_color, lambda n: n * 1.2)

        grid_label_kwargs = {"bg": bg_color, "font": tk_font.Font(family="TkSmallCaptionFont", size=20),
                             "fg": "#fafafa"}

        turn_label = tk.Label(grid_master, bg=bg_color, text="Player's turn",
                              font=tk_font.Font(family="TkHeadingFont", size=24),
                              fg="#ffffff")

        turn_label.place(relwidth=1.0, relheight=grid_consts.RELATIVE_TURN_LABEL_HEIGHT, relx=0.5, rely=0, anchor="n")

        rotation_label_ratio_placement_kwargs = {"parent_width": self.root_width,
                                                 "parent_height": self.root_height,
                                                 "relwidth": grid_consts.RELATIVE_ROTATION_LABEL_SIZE,
                                                 "relheight": grid_consts.RELATIVE_ROTATION_LABEL_SIZE}

        grid1_label = tk.Label(grid_master, text=f"Player1's grid", **grid_label_kwargs)
        grid1_clockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)
        grid1_anticlockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)

        grid1_label_rely = grid_consts.RELATIVE_TURN_LABEL_HEIGHT

        grid1_label.place(relwidth=1.0, relheight=grid_label_height, relx=0.5,
                          rely=grid1_label_rely, anchor="n")

        ratio_place(grid1_anticlockwise_rotation_label, **rotation_label_ratio_placement_kwargs, relx=1,
                    rely=grid1_label_rely + grid_label_height / 2, anchor="e")
        ratio_place(grid1_clockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
                    rely=grid1_label_rely + grid_label_height / 2, anchor="w")

        grid2_label = tk.Label(grid_master, text="Player2's grid", **grid_label_kwargs)
        grid2_clockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)
        grid2_anticlockwise_rotation_label = tk.Label(grid_master, **grid_label_kwargs)

        grid2_label_rely = grid_consts.RELATIVE_TURN_LABEL_HEIGHT + grid_label_height + grid_consts.RELATIVE_GRID_HEIGHT

        grid2_label.place(relwidth=1.0, relheight=grid_label_height, relx=0.5, rely=grid2_label_rely, anchor="n")

        ratio_place(grid2_anticlockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
                    relx=1.0, rely=grid2_label_rely + grid_label_height / 2, anchor="e")
        ratio_place(grid2_clockwise_rotation_label, **rotation_label_ratio_placement_kwargs,
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

        return GridData(grid_master=grid_master, grid1=grid1, grid1_label=grid1_label,
                        grid1_clockwise_rotation_label=grid1_clockwise_rotation_label,
                        grid1_anticlockwise_rotation_label=grid1_anticlockwise_rotation_label, grid2=grid2,
                        grid2_label=grid2_label, grid2_clockwise_rotation_label=grid2_clockwise_rotation_label,
                        grid2_anticlockwise_rotation_label=grid2_anticlockwise_rotation_label, turn_label=turn_label)

    @staticmethod
    def fill_direction_unchecked(cell, direction: str, length: int, color: str):
        Game.fill_cell(cell, color)

        for i in range(1, length):
            cell = getattr(cell, direction)
            Game.fill_cell(cell, color)

    @staticmethod
    def check_occupied(cell: Cell, direction: str, length: int) -> bool:
        if cell.ship: return True

        for i in range(1, length):
            cell = getattr(cell, direction)
            if cell.ship: return True

        return False

    @staticmethod
    def fill_above(cell: Cell, length: int, color: str) -> bool:
        if length > cell.position_vector[1] or Game.check_occupied(cell, "above", length): return False
        Game.fill_direction_unchecked(cell, "above", length, color)
        return True

    @staticmethod
    def fill_below(cell: Cell, length: int, color: str) -> bool:
        if length + cell.position_vector[1] - 1 > grid_consts.GRID_Y or Game.check_occupied(cell, "below", length):
            return False
        Game.fill_direction_unchecked(cell, "below", length, color)
        return True

    @staticmethod
    def fill_left(cell: Cell, length: int, color: str) -> bool:
        if (ord(cell.position_vector[0]) - misc_consts.ALPHA_BASE < length or
                Game.check_occupied(cell, "left", length)): return False
        Game.fill_direction_unchecked(cell, "left", length, color)
        return True

    @staticmethod
    def fill_right(cell: Cell, length: int, color: str) -> bool:
        if ord(cell.position_vector[0]) - ord('A') + length > grid_consts.GRID_X or Game.check_occupied(
                cell, "right", length): return False
        Game.fill_direction_unchecked(cell, "right", length, color)
        return True

    @staticmethod
    def fill_cell(cell: Cell, color: str):
        cell.label.config(bg=color)

    def place_ships(self, grid: Grid, clockwise_rotation_label: tk.Label, anticlockwise_rotation_label: tk.Label,
                    callback: Callable):
        current_direction = Direction.left
        current_ship_index = 0
        current_ship = rules_consts.SHIP_SETUP[current_ship_index]
        current_ship_length, current_ship_color = current_ship["length"], current_ship["color"]

        rendered_direction: Direction = Direction.none
        rendered_length = 0

        def update_ship_refs():
            nonlocal current_ship, current_ship_length, current_ship_color

            current_ship = rules_consts.SHIP_SETUP[current_ship_index]
            current_ship_length, current_ship_color = current_ship["length"], current_ship["color"]

        fill_functions = {Direction.above: Game.fill_above, Direction.below: Game.fill_below,
                          Direction.left: Game.fill_left, Direction.right: Game.fill_right}

        def render_ship(cell: Cell):
            nonlocal rendered_direction, rendered_length
            direction, length = current_direction, current_ship_length

            if fill_functions[direction](cell, length, current_ship_color):
                rendered_direction = direction
                rendered_length = length
            else:
                rendered_direction = direction.none
                Game.fill_cell(cell, "#ff0000")

        def unrender_ship(cell: Cell):
            if rendered_direction == Direction.none:
                if ship := cell.ship:
                    Game.fill_cell(cell, ship.color)
                else:
                    Game.fill_cell(cell, grid_consts.GRID_COLOR)
            else:
                Game.fill_direction_unchecked(cell, rendered_direction.name, rendered_length, grid_consts.GRID_COLOR)

        clockwise_rotation_label.config(text='⟳')
        anticlockwise_rotation_label.config(text='⟲')

        def clockwise_rotation(_=None):
            nonlocal current_direction

            if current_direction == Direction.left:
                current_direction = Direction.above
            else:
                current_direction = Direction(current_direction.value + 1)

        def anticlockwise_rotation(_=None):
            nonlocal current_direction

            if current_direction == Direction.above:
                current_direction = Direction.left
            else:
                current_direction = Direction(current_direction.value - 1)

        def place_ship(cell: Cell):
            nonlocal rendered_direction, current_ship_index

            if rendered_direction == Direction.none: return

            ship: Ship = current_ship["class"](cell, rendered_direction)

            cell.ship = ship

            for i in range(1, rendered_length):
                cell = getattr(cell, rendered_direction.name)
                cell.ship = ship

            rendered_direction = Direction.none

            current_ship_index += 1

            if current_ship_index < len(rules_consts.SHIP_SETUP):
                update_ship_refs()
            else:
                clockwise_rotation_label.config(text="")
                anticlockwise_rotation_label.config(text="")

                clockwise_rotation_label.unbind("<Button-1>")
                anticlockwise_rotation_label.unbind("<Button-1>")

                grid.cell_unbind("<Enter>")
                grid.cell_unbind("<Leave>")
                grid.cell_unbind("<Button-1>")

                self.root.after(0, callback)  # type: ignore[arg-type]

        clockwise_rotation_label.bind("<Button-1>", clockwise_rotation)
        anticlockwise_rotation_label.bind("<Button-1>", anticlockwise_rotation)

        grid.cell_bind("<Enter>", render_ship)
        grid.cell_bind("<Leave>", unrender_ship)
        grid.cell_bind("<Button-1>", place_ship)

    def pvc_computer_place_ships(self):
        grid_data = self.grid_data

        turn_label = grid_data.turn_label
        base_text = "Computer's turn to place"
        iterations = 4
        max_periods = 3
        pause_ms = 333

        def load(i: int, iteration: int):
            if iteration >= iterations: return

            turn_label.config(text=f"{base_text}{'.' * i}")

            if i == max_periods:
                turn_label.after(pause_ms, load, 0, iteration + 1)
            else:
                turn_label.after(pause_ms, load, i + 1, iteration)

        turn_label.after(0, load, 0, 0)

    def pvc_ship_placement(self):
        print(f"Welcome, {self.player1.name}")
        grid_data = self.grid_data

        grid_data.grid1_label.config(text="Your grid")
        grid_data.grid2_label.config(text="Computer's grid")

        grid_data.turn_label.config(text=f"Place your ships")
        grid_data.grid_master.place(relwidth=1, relheight=1)

        player_grid = grid_data.grid1

        self.place_ships(player_grid, grid_data.grid1_clockwise_rotation_label,
                         grid_data.grid1_anticlockwise_rotation_label, self.pvc_computer_place_ships)

    def pvp_ship_placement(self):
        grid_data = self.grid_data
        grid_data.grid1_label.config(text=f"{self.player1.name}'s grid")
        grid_data.grid2_label.config(text=f"{self.player2.name}'s grid")

        self.pvp_player_place_ships(self.player1)
        grid_data.grid_master.place(relwidth=1, relheight=1)

    def pvp_player_place_ships(self, player: Player):
        grid_data = self.grid_data
        grid_data.turn_label.config(text=f"{player.name}'s turn to place")

        grid_name = f"grid{player.instance}"

        self.place_ships(getattr(grid_data, grid_name), getattr(grid_data, f"{grid_name}_clockwise_rotation_label"),
                         getattr(grid_data, f"{grid_name}_anticlockwise_rotation_label"),
                         self.play_pvp if player.instance == Player.instances else
                         lambda: self.pvp_player_place_ships(getattr(self, f"player{player.instance + 1}")))

    def play_pvc(self):
        print(f"Playing {self.player1} vs computer")

    def play_pvp(self):
        print(f"Player {self.player1} vs {self.player2}")

    def switch_grid(self):  # for pvp
        grid_data = self.grid_data
        grid_data.turn_label.config(text=f"{self.turn.name}'s turn")
        grid_data.grid2_label.config(text=f"{self.other.name}'s field")

    def start(self):
        self.place_menu()
        self.root.mainloop()

    def replay(self):
        self.player1 = Player.new(self.player1)
        self.player2 = Player.new(self.player2)
