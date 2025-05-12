from enum import auto, Enum

ALPHA_BASE = ord('A') - 1

MAX_NAME_LENGTH = 10

FILL_SYMBOLS = {
    "above": '↑',
    "right": '→',
    "below": '↓',
    "left": '←',
}


class SetupSize(Enum):
    MINIMAL = auto()
    SMALL = auto()
    NORMAL = auto()
    LARGE = auto()


SHIP_SETUP_SIZE = SetupSize.NORMAL
