import tkinter as tk
from typing import Any, Tuple

from app.constants.grid import GRID_COLOR, CELL_DESTROY_COLOR


class NullCell:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(NullCell, cls).__new__(cls)
            cls._instance.position = None
        return cls._instance

    def __str__(self):
        return "Null"

    def __repr__(self):
        return "NullCell()"


NullCell = NullCell()


class Cell:
    def __init__(self, label: tk.Label, position_vector: Tuple[str, int]):
        self.label = label
        self.position_vector = position_vector
        self.position = f"{position_vector[0]}{position_vector[1]}"
        self.above = None
        self.below = None
        self.left = None
        self.right = None
        self.ship = None
        self.destroyed = False

    def __setattr__(self, name: str, value: Any):
        if getattr(self, name, None) is not None:
            raise AttributeError(f"Property {name} cannot be overwritten")
        object.__setattr__(self, name, value)

    def __str__(self):
        return self.position

    def __repr__(self):
        return f"Cell(label={self.label}, position={self.position}, above={self.above}, below={self.below}, left={self.left}, right={self.right})"

    def destroy(self, text=""):
        object.__setattr__(self, "ship", None)
        object.__setattr__(self, "destroyed", True)

        (label := self.label).config(bg=CELL_DESTROY_COLOR)

        if len(text):
            label.config(bg=CELL_DESTROY_COLOR, fg="#ff0000", text=text)

    def reset(self):
        object.__setattr__(self, "ship", None)
        self.label.config(bg=GRID_COLOR, fg="#ffffff", text="")
