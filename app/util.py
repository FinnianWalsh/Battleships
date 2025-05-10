import tkinter as tk

from typing import Any, List, Optional, Self, Type, Union

Number = Union[int, float]

OptSelf = Optional[Self]


def get_bool(prompt: str) -> bool:
    while True:
        response = input(prompt).lower()

        if response in ['y', "yes"]:
            return True
        elif response in ['n', "no"]:
            return False


def hex_color_mut(hex_color: str, manip) -> str:
    red = int(manip(int(hex_color[1:3], base=16)))
    green = int(manip(int(hex_color[3:5], base=16)))
    blue = int(manip(int(hex_color[5:7], base=16)))

    return "#{:02X}{:02X}{:02X}".format(red, green, blue)


def create_table(frame: tk.Frame, columns: int, rows: int, relative_column_offsets: List[Number],
                 relative_row_offsets: List[Number], cell_cls: Type[Any] = tk.Label, **kwargs) -> (List[List], float):
    row_list, relative_universal_y_offset = [], 0

    relative_row_height = (1 - sum(relative_row_offsets)) / rows

    while rows > len(relative_row_offsets):
        relative_row_offsets.append(0)

    relative_column_width = (1 - sum(relative_column_offsets)) / columns

    while columns > len(relative_column_offsets):
        relative_column_offsets.append(0)

    for i in range(rows):
        column_list = []
        relative_universal_y_offset += relative_row_offsets[i]

        rely_offset = relative_row_height * i + relative_universal_y_offset

        relative_universal_x_offset = 0

        for j in range(columns):
            relative_universal_x_offset += relative_column_offsets[j]

            cell = cell_cls(frame, **kwargs)
            cell.place(relwidth=relative_column_width, relheight=relative_row_height,
                       relx=relative_column_width * j + relative_universal_x_offset,
                       rely=rely_offset)
            column_list.append(cell)

        row_list.append(column_list)

    return row_list, relative_row_height


def ratio_place(element: tk.Widget, parent_width: Number, parent_height: Number, relwidth: float,
                relheight: float, ratio: Number = 1, **kwargs):
    max_width = parent_width * relwidth
    max_height = parent_height * relheight

    ratio_height = max_width / ratio
    ratio_width = max_height * ratio

    if ratio_height <= max_height:
        width = max_width
        height = ratio_height
    else:
        width = ratio_width
        height = max_height

    element.place(width=width, height=height, **kwargs)


def create_bar(parent: tk.Widget, background: str = "#ffffff", **kwargs) -> tk.Frame:
    bar = tk.Frame(parent, bg=background)
    bar.place(**kwargs)
    return bar
