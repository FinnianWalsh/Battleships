import tkinter as tk

from functools import lru_cache
from typing import Callable, List, Self

from .cell import Cell, NullCell
from ..constants.grid import GRID_X, GRID_Y, GRID_COLOR
from ..constants.misc import ALPHA_BASE
from ..util import create_table, Number


class Grid:
    def __init__(self, frame: tk.Frame, labels: List[List[tk.Label]]):
        self.frame = frame
        self.labels = labels

        cells, temp_1d_cells = [], []

        @lru_cache
        def get_char(num: int):
            return chr(num + ALPHA_BASE)

        for i in range(1, GRID_Y + 1):
            label_row = labels[i]
            cell_row = []

            for j in range(1, GRID_X + 1):
                cell = Cell(label_row[j], (get_char(j), i))
                cell_row.append(cell)
                temp_1d_cells.append(cell)

            cells.append(cell_row)

        def assign(cell_index: int, above: bool = False, below: bool = False, left: bool = False, right: bool = False):
            target_cell = temp_1d_cells[cell_index]

            target_cell.above = temp_1d_cells[cell_index - GRID_X] if above else NullCell
            target_cell.below = temp_1d_cells[cell_index + GRID_X] if below else NullCell
            target_cell.left = temp_1d_cells[cell_index - 1] if left else NullCell
            target_cell.right = temp_1d_cells[cell_index + 1] if right else NullCell

        bottom_offset = (GRID_Y - 1) * GRID_X

        x_sub1 = GRID_X - 1

        assign(0, below=True, right=True)  # top left
        assign(x_sub1, below=True, left=True)  # top right
        assign(bottom_offset, above=True, right=True)
        assign(GRID_Y * GRID_X - 1, above=True, left=True)  # bottom right

        for i in range(1, x_sub1):
            assign(i, below=True, left=True, right=True)
            assign(i + bottom_offset, above=True, left=True, right=True)

        for i in range(1, GRID_Y - 1):
            row_index = i * GRID_X
            assign(row_index, above=True, below=True, right=True)
            assign(row_index + GRID_X - 1, above=True, below=True, left=True)

            for j in range(1, x_sub1):
                assign(row_index + j, above=True, below=True, left=True, right=True)

        # print(*(v for v in temp_1d_cells))

        self.cells = cells

    def __getitem__(self, item: str) -> Cell:
        j = ord(item[0]) - ord('A')
        print(j)

        i = int(item[1:]) - 1
        print(i)

        return self.cells[i][j]

    def cell_bind(self, event_sequence: str, function: Callable[[Cell], None]):
        for i in range(GRID_Y):
            row = self.cells[i]

            for cell in row:
                cell.label.bind(event_sequence, lambda _, c=cell: function(c))

    def cell_unbind(self, event_sequence: str):
        for i in range(GRID_Y):
            row = self.cells[i]

            for cell in row:
                cell.label.unbind(event_sequence)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    @classmethod
    def create(cls, root_width: Number, root_height: Number, parent: tk.Widget, **kwargs) -> Self:
        frame = tk.Frame(parent, **kwargs)

        bar_thickness = 3

        table, _ = create_table(frame, GRID_X + 1, GRID_Y + 1, [0] + [bar_thickness / root_width] * GRID_X,
                                [0] + [bar_thickness / root_height] * GRID_Y, bg=GRID_COLOR, fg="#ffffff")

        first_column = table[0]

        for i in range(1, GRID_X + 1):
            first_column[i].config(text=chr(i + ALPHA_BASE))

        for i in range(1, GRID_Y + 1):
            table[i][0].config(text=i)

        return Grid(frame, table)


class GridData:
    def __init__(self, grid_master: tk.Frame, grid1: Grid, grid1_label: tk.Label,
                 grid1_clockwise_rotation_label: tk.Label, grid1_anticlockwise_rotation_label: tk.Label, grid2: Grid,
                 grid2_clockwise_rotation_label: tk.Label, grid2_anticlockwise_rotation_label: tk.Label,
                 grid2_label: tk.Label, turn_label: tk.Label):
        self.grid_master = grid_master
        self.grid1 = grid1
        self.grid2 = grid2

        self.grid1_label = grid1_label
        self.grid1_clockwise_rotation_label = grid1_clockwise_rotation_label
        self.grid1_anticlockwise_rotation_label = grid1_anticlockwise_rotation_label

        self.grid2_label = grid2_label
        self.grid2_clockwise_rotation_label = grid2_clockwise_rotation_label
        self.grid2_anticlockwise_rotation_label = grid2_anticlockwise_rotation_label

        self.turn_label = turn_label
