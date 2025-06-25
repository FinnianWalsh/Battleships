import tkinter as tk
import threading
import tkinter.font as tk_font
from enum import auto, Enum
from time import perf_counter, sleep
from typing import Callable, Union

from .constants.menu import *
from .constants.misc import MAX_NAME_LENGTH
from .constants.root import ROOT_BACKGROUND_COLOR
from .util import create_bar, create_table, Number, ratio_place


class Gamemode(Enum):
    none = auto()
    PVP = auto()
    PVC = auto()


class Menu(tk.Frame):
    def __init__(self, root: tk.Tk, root_width: Number, root_height: Number, pvc_callback: Callable[[str], None],
                 pvp_callback: Callable[[str, str], None]):
        super().__init__(root, bg=ROOT_BACKGROUND_COLOR)
        self.pvc_callback, self.pvp_callback = pvc_callback, pvp_callback

        self.relative_rules_head_offset = 5 / root_height
        self.relative_rules_head_size = 30 / root_height

        self.relative_rules_label_offset = self.relative_rules_head_offset + self.relative_rules_head_size
        self.relative_rules_label_height = 200 / root_height

        self.relative_base_component_padding = 20 / root_height
        self.relative_rules_table_offset = self.relative_rules_label_offset + self.relative_rules_label_height + self.relative_base_component_padding

        self.relative_rules_table_height = 200 / root_height
        self.relative_rules_table_width = 1 - 20 / root_width

        self.relative_start_btn_offset = -10 / root_height
        self.relative_start_btn_width = 80 / root_width
        self.relative_start_btn_height = 30 / root_height

        self.rules_head = tk.Label(self, text=RULES_HEAD)
        self.rules_head.config(font=tk_font.Font(family="Helvetica", size=20, weight="bold"), fg="#ffffff",
                               bg=ROOT_BACKGROUND_COLOR)
        self.rules_head.place(relwidth=1.0, rely=self.relative_rules_head_offset,
                              relheight=self.relative_rules_head_size)

        self.rules_label = tk.Label(self, text=RULES_BODY, anchor="n", wraplength=root_width - 50,
                                    font=tk_font.Font(family="Helvetica", size=14), fg="#ffffff",
                                    bg=ROOT_BACKGROUND_COLOR)
        self.rules_label.place(relwidth=1.0, rely=self.relative_rules_label_offset,
                               relheight=self.relative_rules_label_height)

        self.rules_table = tk.Frame(self, bg=ROOT_BACKGROUND_COLOR)

        self.rules_table.place(relwidth=self.relative_rules_table_width,
                               relheight=self.relative_rules_table_height, relx=0.5,
                               rely=self.relative_rules_table_offset, anchor="n")

        self.relative_rules_bar_height = 4 / root_height

        self.table_contents, self.relative_column_width, self.relative_row_height = create_table(self.rules_table,
                                                                                                 TABLE_COLUMNS,
                                                                                                 TABLE_ROWS, [],
                                                                                                 [0,
                                                                                                  self.relative_rules_bar_height * 5],
                                                                                                 bg=ROOT_BACKGROUND_COLOR,
                                                                                                 font=tk_font.Font(
                                                                                                     family="Helvetica",
                                                                                                     size=14),
                                                                                                 fg="#ffffff")

        first_row = self.table_contents[0]
        first_row[0].config(text="Name", anchor="center")
        first_row[1].config(text="Length", anchor="center")
        first_row[2].config(text="Color", anchor="center")

        column_width = root_width * self.relative_rules_table_width * self.relative_column_width
        row_height = root_height * self.relative_rules_table_height * self.relative_row_height

        for i in range(TABLE_ROWS - 1):
            row = self.table_contents[i + 1]
            ship = SHIP_SETUP[i]
            row[0].config(text=ship["class"].__name__, anchor="center")
            row[1].config(text=ship["length"], anchor="center")

            color_square = tk.Label(row[2])

            ratio_place(color_square, parent_width=column_width, parent_height=row_height, relwidth=0.8, relheight=0.8,
                        ratio=1, relx=0.5, rely=0.5, anchor="center")
            color_square.config(bg=ship["color"], anchor="center")

        create_bar(self.rules_table, relwidth=self.relative_rules_table_width, relx=0.5, rely=self.relative_row_height,
                   anchor="n")

        self.relative_mode_selection_offset = self.relative_rules_table_offset + self.relative_rules_table_height + self.relative_base_component_padding
        self.relative_mode_selection_height = 150 / root_height

        self.relative_entries_frame_offset = self.relative_mode_selection_offset + self.relative_mode_selection_height + self.relative_base_component_padding
        self.relative_entries_frame_width = 1 - 20 / root_width
        self.relative_entries_frame_height = 80 / root_height

        mode_selection_frame = tk.Frame(self, bg=MODE_SELECTION_COLOR_UNSELECTED)
        mode_selection_frame.place(relwidth=self.relative_entries_frame_width,
                                   relheight=self.relative_mode_selection_height, relx=0.5,
                                   rely=self.relative_mode_selection_offset, anchor="n")

        mode_header = tk.Label(mode_selection_frame, bg=MODE_SELECTION_COLOR_UNSELECTED, text="Select mode:",
                               fg="#ffffff")
        mode_header.place(relwidth=1.0, relheight=MODE_HEADER_HEIGHT, relx=0.5, anchor="n")

        self.pvc_btn = tk.Label(mode_selection_frame, bg=MODE_SELECTION_COLOR_UNSELECTED,
                                text="Player VS Computer",
                                fg="#ffffff")
        self.pvc_btn.place(relwidth=MODE_BUTTON_WIDTH, relheight=MODE_BUTTON_HEIGHT, relx=0.5,
                           rely=MODE_HEADER_HEIGHT, anchor="n")

        self.pvp_btn = tk.Label(mode_selection_frame, bg=MODE_SELECTION_COLOR_UNSELECTED, text="Player VS Player",
                                fg="#ffffff")
        self.pvp_btn.place(relwidth=MODE_BUTTON_WIDTH, relheight=MODE_BUTTON_HEIGHT, relx=0.5,
                           rely=MODE_HEADER_HEIGHT + MODE_BUTTON_HEIGHT, anchor="n")

        entries_frame = tk.Frame(self, bg=ROOT_BACKGROUND_COLOR)
        entries_frame.place(relwidth=self.relative_entries_frame_width, relheight=self.relative_entries_frame_height,
                            relx=0.5,
                            rely=self.relative_entries_frame_offset, anchor="n")

        self.player1_entry_label = tk.Label(entries_frame, bg=ENTRY_BACKGROUND_COLOR,
                                            fg="#ffffff")
        self.player1_entry = tk.Entry(entries_frame, bg=ENTRY_BACKGROUND_COLOR, fg="#ffffff")

        self.player2_entry_relative_offset = 1 - ENTRY_COMPONENT_RELATIVE_HEIGHT * 2 + ENTRY_COMPONENT_RELATIVE_HEIGHT

        self.player2_entry = tk.Entry(entries_frame, bg=ENTRY_BACKGROUND_COLOR, fg="#ffffff")

        self.player2_entry_label = tk.Label(entries_frame, text="Enter player 2 name:", bg=ENTRY_BACKGROUND_COLOR,
                                            fg="#ffffff")

        self.selected_mode = Gamemode.none

        self.pvc_btn.bind("<Button-1>", self.on_pvc_btn_click)
        self.pvp_btn.bind("<Button-1>", self.on_pvp_btn_clicked)

        self.pvc_btn.bind("<Enter>", self.on_mode_btn_enter)
        self.pvp_btn.bind("<Enter>", self.on_mode_btn_enter)

        self.pvc_btn.bind("<Leave>", self.on_pvc_btn_leave)
        self.pvp_btn.bind("<Leave>", self.on_pvp_btn_leave)

        self.start_btn = tk.Button(self, text="Start", bg="#00ff00")
        self.start_btn.place(relwidth=self.relative_start_btn_width, relheight=self.relative_start_btn_height, relx=0.5,
                             rely=1 + self.relative_start_btn_offset, anchor="s")

        self.relative_warning_label_offset = self.relative_start_btn_offset * 2 - self.relative_start_btn_height

        self.warning_label = tk.Label(self, text="", bg=ROOT_BACKGROUND_COLOR, fg="#ff0000")
        self.warning_label.place(relwidth=1.0, relheight=self.relative_start_btn_height, relx=0.5,
                                 rely=1 + self.relative_warning_label_offset, anchor="s")

        self.last_warning = 0
        self.has_started = False

        self.start_btn.bind("<Button-1>", self.on_start)

    @staticmethod
    def on_mode_btn_enter(event: tk.Event):
        event.widget.config(bg=MODE_SELECTION_COLOR_HOVER)

    def on_pvc_btn_leave(self, _):
        self.pvc_btn.config(bg=MODE_SELECTION_COLOR_SELECTED if self.selected_mode == Gamemode.PVC
        else MODE_SELECTION_COLOR_UNSELECTED)

    def on_pvp_btn_leave(self, _):
        self.pvp_btn.config(bg=MODE_SELECTION_COLOR_SELECTED if self.selected_mode == Gamemode.PVP
        else MODE_SELECTION_COLOR_UNSELECTED)

    @staticmethod
    def show_entry_component(entry: tk.Entry, label: tk.Label, label_text: str, num: int = 1):
        relative_y = 0.5 * (num - 1)

        label.config(text=label_text)
        label.place(relwidth=ENTRY_LABEL_RELATIVE_WIDTH,
                    relheight=ENTRY_COMPONENT_RELATIVE_HEIGHT, rely=relative_y)

        entry.place(relwidth=ENTRY_INSTANCE_RELATIVE_WIDTH,
                    relheight=ENTRY_COMPONENT_RELATIVE_HEIGHT,
                    relx=ENTRY_LABEL_RELATIVE_WIDTH, rely=relative_y)

    @staticmethod
    def hide_entry_component(entry: tk.Entry, label: tk.Label):
        entry.place_forget()
        label.place_forget()

    def place(self):
        super().place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    def unselect_mode(self, btn: tk.Label):
        self.selected_mode = Gamemode.none

        btn.config(bg=MODE_SELECTION_COLOR_UNSELECTED)

        Menu.hide_entry_component(self.player1_entry, self.player1_entry_label)
        Menu.hide_entry_component(self.player2_entry, self.player2_entry_label)

    def select_gamemode(self, gamemode: Gamemode, selected_gamemode_btn: tk.Label, other_gamemode_btn: tk.Label):
        self.selected_mode = gamemode
        selected_gamemode_btn.config(bg=MODE_SELECTION_COLOR_SELECTED)
        other_gamemode_btn.config(bg=MODE_SELECTION_COLOR_UNSELECTED)

    def on_pvc_btn_click(self, _=None):
        if self.selected_mode == Gamemode.PVC:
            return self.unselect_mode(self.pvc_btn)

        self.select_gamemode(Gamemode.PVC, self.pvc_btn, self.pvp_btn)
        Menu.show_entry_component(self.player1_entry, self.player1_entry_label, "Enter player name")
        Menu.hide_entry_component(self.player2_entry, self.player2_entry_label)

    def on_pvp_btn_clicked(self, _=None):
        if self.selected_mode == Gamemode.PVP:
            return self.unselect_mode(self.pvp_btn)

        self.select_gamemode(Gamemode.PVP, self.pvp_btn, self.pvc_btn)

        Menu.show_entry_component(self.player1_entry, self.player1_entry_label, "Enter player 1 name:", 1)
        Menu.show_entry_component(self.player2_entry, self.player2_entry_label, "Enter player 2 name:", 2)

    def clear_warning(self, warning_time: float):
        sleep(WARNING_DURATION)

        if warning_time == self.last_warning:
            self.warning_label.after(0, lambda: self.warning_label.config(text=""))  # type: ignore[arg-type]

    def warn(self, warning: str):
        this_warning = perf_counter()
        self.last_warning = this_warning
        self.warning_label.config(text=warning)

        threading.Thread(target=self.clear_warning, daemon=True, args=(this_warning,)).start()

    def reset_text(self):
        delay = 2
        sleep(delay)

        if not self.has_started:
            self.start_btn.after(0, lambda: self.start_btn.config(text="Start"))  # type: ignore[arg-type]

    def can_start_pvc(self) -> Union[str, None]:
        if not len(player_entry_text := self.player1_entry.get()): return "Enter player name!"
        if player_entry_text == "Computer": return "You cannot name yourself 'Computer'!"
        if len(player_entry_text) > MAX_NAME_LENGTH:
            return f"Player names must be no more than {MAX_NAME_LENGTH} characters long!"

        return None

    def can_start_pvp(self) -> Union[str, None]:
        player2_entry_text = self.player2_entry.get()

        if not len(player1_entry_text := self.player1_entry.get()):
            if len(player2_entry_text):
                return "Enter player 1 name!"
            else:
                return "Enter player names!"
        if not len(player2_entry_text): return "Enter player 2 name!"
        if len(player1_entry_text) > MAX_NAME_LENGTH or len(
                player2_entry_text) > MAX_NAME_LENGTH:
            return f"Player names must be no more than {MAX_NAME_LENGTH} characters long!"
        if player1_entry_text == player2_entry_text: return "Enter two different names!"

        return None

    def on_start(self, _):
        if self.has_started:
            self.warn("Game has already started!")
        elif self.selected_mode == Gamemode.none:
            self.warn("Select a mode!")
        elif self.selected_mode == Gamemode.PVC:
            if warning := self.can_start_pvc():
                self.warn(warning)
            elif self.start_btn.cget("text") == "Confirm":
                self.has_started = True
                self.place_forget()
                self.pvc_callback(self.player1_entry.get())
                # self.pvc_ship_placement_init()
            else:
                self.check_confirmation()
        elif self.selected_mode == Gamemode.PVP:
            if warning := self.can_start_pvp():
                self.warn(warning)
            elif self.start_btn.cget("text") == "Confirm":
                self.has_started = True
                self.place_forget()
                self.pvp_callback(self.player1_entry.get(), self.player2_entry.get())
                # self.pvp_ship_placement_init()
            else:
                self.check_confirmation()

    def check_confirmation(self):
        self.start_btn.config(text="Confirm")
        threading.Thread(target=self.reset_text, daemon=True).start()

    def reset(self):
        self.unselect_mode(self.pvc_btn)
        self.pvp_btn.config(bg=MODE_SELECTION_COLOR_UNSELECTED)
