from abc import ABC, abstractmethod
from enum import auto, Enum
from typing import Set

from .field.cell import Cell



class Direction(Enum):
    def _generate_next_value_(name, start, count, last_values): # noqa or
        return count + 1
    none = auto()
    above = auto()
    right = auto()
    below = auto()
    left = auto()

class Ship(ABC):
    @abstractmethod
    def __init__(self, name: str, base: Cell, direction: Direction):
        self._name = name

        for item in SHIP_SETUP:
            if item["class"].__name__ == name:
                self._length = item["length"]
                self._color = item["color"]
                break
        else:
            raise ValueError(f"No length property found for {name}")

        self._base = base
        self._direction = direction
        self._remaining_length = set(range(self._length))

    @property
    def name(self) -> str:
        return self._name

    @property
    def length(self) -> int:
        return self._length

    @property
    def color(self) -> str:
        return self._color

    @property
    def base(self) -> Cell:
        return self._base

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def remaining_length(self) -> Set[int]:
        return self._remaining_length


class Carrier(Ship):
    def __init__(self, base: Cell, direction: Direction): super().__init__("Carrier", base, direction)


class Battleship(Ship):
    def __init__(self, base: Cell, direction: Direction): super().__init__("Battleship", base, direction)


class Cruiser(Ship):
    def __init__(self, base: Cell, direction: Direction): super().__init__("Cruiser", base, direction)


class Submarine(Ship):
    def __init__(self, base: Cell, direction: Direction): super().__init__("Submarine", base, direction)


class Destroyer(Ship):
    def __init__(self, base: Cell, direction: Direction): super().__init__("Destroyer", base, direction)


SHIP_SETUP = [
    {"class": Carrier, "length": 5, "color": "#000022"},
    {"class": Battleship, "length": 4, "color": "#101010"},
    {"class": Cruiser, "length": 3, "color": "#636b2f"},
    {"class": Submarine, "length": 3, "color": "#181818"},
    {"class": Destroyer, "length": 2, "color": "#ffa500"}
]
