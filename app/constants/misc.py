from enum import auto, Enum

ALPHA_BASE = ord('A') - 1

MAX_NAME_LENGTH = 10

FILL_SYMBOLS = {
    "above": '\u2191',
    "right": '\u2192',
    "below": '\u2193',
    "left": '\u2190',
}


class SetupSize(Enum):
    MINIMAL = auto()
    SMALL = auto()
    NORMAL = auto()
    LARGE = auto()


SHIP_SETUP_SIZE = SetupSize.NORMAL
