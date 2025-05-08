import tkinter as tk

from typing import Any, Optional, Self

from ..util import OptSelf


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
    def __init__(self, label: tk.Label, position: str, above: OptSelf = None, below: OptSelf = None,
                 left: OptSelf = None, right: OptSelf = None):
        self.label = label
        self.position = position
        self.above = above
        self.below = below
        self.left = left
        self.right = right

    def __setattr__(self, name: str, value: Any):
        if getattr(self, name, None) is not None:
            raise AttributeError(f"Property {name} cannot be overwritten")
        object.__setattr__(self, name, value)

    def __str__(self):
        return self.position

    def __repr__(self):
        return f"Cell(label={self.label}, position={self.position}, above={self.above}, below={self.below}, left={self.left}, right={self.right})"
