from abc import ABC, abstractmethod
from enum import auto, Enum
from typing import Set

from .field.cell import Cell

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Ship(ABC):
    @abstractmethod
    def __init__(self, name: str, base: Cell, direction: Direction):
        self._name = name
        self._length = next(item["length"] for item in SHIP_SETUP if item["name"] == name)

        assert self._length is int, "Expected length to be int"
        assert self._length >= 1, "Expected length to be at least 1"

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
    {"class": Battleship, "length": 4, "color": "101010"},
    {"class": Cruiser, "length": 3, "color": "#636b2f"},
    {"class": Submarine, "length": 3, "color": "#050505"},
    {"class": Destroyer, "length": 2, "color": "#ffa500"}
]
