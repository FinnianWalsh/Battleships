import tkinter as tk
from typing import Callable

from .grid_system import Grid, Cell

from .ship import Ship, Direction
from .constants.menu import SHIP_SETUP
from .constants.misc import ALPHA_BASE, FILL_SYMBOLS
from .constants.grid import GRID_COLOR, GRID_X, GRID_Y


class PlacementManager:
    def __init__(self, grid: Grid, clockwise_rotation_label: tk.Label, anticlockwise_rotation_label: tk.Label,
                 callback: Callable[[Grid], None]):
        self.grid = grid
        self.clockwise_rotation_label = clockwise_rotation_label
        self.anticlockwise_rotation_label = anticlockwise_rotation_label
        self.callback = callback

        self.current_direction = Direction.above
        self.current_ship_index = 0
        self.current_ship = None
        self.current_ship_length = 0
        self.current_ship_color = ""

        self.rendered_direction: Direction = Direction.none
        self.rendered_length = 0

        self.update_ship_refs()

    def __call__(self):
        self.clockwise_rotation_label.config(text='⟳')
        self.anticlockwise_rotation_label.config(text='⟲')

        self.clockwise_rotation_label.bind("<Button-1>", self.clockwise_rotation)
        self.anticlockwise_rotation_label.bind("<Button-1>", self.anticlockwise_rotation)

        self.grid.cell_bind("<Enter>", self.render_ship)
        self.grid.cell_bind("<Leave>", self.unrender_ship)
        self.grid.cell_bind("<Button-1>", self.place_ship)

    @staticmethod
    def fill_cell(cell: Cell, color: str):
        cell.label.config(bg=color)

    @staticmethod
    def fill_direction_unchecked(cell, direction: str, length: int, color: str):
        PlacementManager.fill_cell(cell, color)

        for i in range(1, length):
            cell = getattr(cell, direction)
            PlacementManager.fill_cell(cell, color)

    @staticmethod
    def check_occupied(cell: Cell, direction: str, length: int) -> bool:
        if cell.ship: return True

        for i in range(1, length):
            cell = getattr(cell, direction)
            if cell.ship: return True

        return False

    @staticmethod
    def fill_above(cell: Cell, length: int, color: str) -> bool:
        if length > cell.position_vector[1] or PlacementManager.check_occupied(cell, "above", length): return False
        PlacementManager.fill_direction_unchecked(cell, "above", length, color)
        return True

    @staticmethod
    def fill_below(cell: Cell, length: int, color: str) -> bool:
        if length + cell.position_vector[1] - 1 > GRID_Y or PlacementManager.check_occupied(cell, "below", length):
            return False
        PlacementManager.fill_direction_unchecked(cell, "below", length, color)
        return True

    @staticmethod
    def fill_left(cell: Cell, length: int, color: str) -> bool:
        if (ord(cell.position_vector[0]) - ALPHA_BASE < length or
                PlacementManager.check_occupied(cell, "left", length)): return False
        PlacementManager.fill_direction_unchecked(cell, "left", length, color)
        return True

    @staticmethod
    def fill_right(cell: Cell, length: int, color: str) -> bool:
        if ord(cell.position_vector[0]) - ord('A') + length > GRID_X or PlacementManager.check_occupied(
                cell, "right", length): return False
        PlacementManager.fill_direction_unchecked(cell, "right", length, color)
        return True

    fill_functions = {Direction.above: fill_above, Direction.below: fill_below,
                      Direction.left: fill_left, Direction.right: fill_right}

    def update_ship_refs(self):
        current_ship = SHIP_SETUP[self.current_ship_index]
        self.current_ship = current_ship
        self.current_ship_length, self.current_ship_color = current_ship["length"], current_ship["color"]

    def render_ship(self, cell: Cell, _):
        direction, length = self.current_direction, self.current_ship_length

        if PlacementManager.fill_functions[direction](cell, length, self.current_ship_color):
            cell.label.config(text=FILL_SYMBOLS[direction.name])
            self.rendered_direction = direction
            self.rendered_length = length
        else:
            self.rendered_direction = direction.none
            PlacementManager.fill_cell(cell, "#ff0000")

    def unrender_ship(self, cell: Cell, _):
        if (rendered_direction := self.rendered_direction) == Direction.none:
            if ship := cell.ship:
                PlacementManager.fill_cell(cell, ship.color)
            else:
                PlacementManager.fill_cell(cell, GRID_COLOR)
        else:
            PlacementManager.fill_direction_unchecked(cell, rendered_direction.name, self.rendered_length, GRID_COLOR)
            cell.label.config(text="")

    def clockwise_rotation(self, _=None):
        if self.current_direction == Direction.left:
            self.current_direction = Direction.above
        else:
            self.current_direction = Direction(self.current_direction.value + 1)

    def anticlockwise_rotation(self, _=None):
        if self.current_direction == Direction.above:
            self.current_direction = Direction.left
        else:
            self.current_direction = Direction(self.current_direction.value - 1)

    def place_ship(self, cell: Cell, _):
        if (rendered_direction := self.rendered_direction) == Direction.none: return

        cell.label.config(text="")

        ship: Ship = self.current_ship["class"](cell, rendered_direction)

        cell.ship = ship

        for i in range(1, self.rendered_length):
            cell = getattr(cell, rendered_direction.name)
            cell.ship = ship

        self.rendered_direction = Direction.none

        self.current_ship_index += 1

        if self.current_ship_index < len(SHIP_SETUP):
            self.update_ship_refs()
        else:
            self.clockwise_rotation_label.config(text="")
            self.anticlockwise_rotation_label.config(text="")

            self.clockwise_rotation_label.unbind("<Button-1>")
            self.anticlockwise_rotation_label.unbind("<Button-1>")

            self.grid.cell_unbind("<Enter>")
            self.grid.cell_unbind("<Leave>")
            self.grid.cell_unbind("<Button-1>")

            self.callback(self.grid)
