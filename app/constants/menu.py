from .. import util
from . import grid as grid_consts, root as root_consts
from ..ship import SHIP_SETUP

RULES_HEAD = "✩ Rules ✩"

RULES_BODY = f"Welcome to Battleships! In this game, two players (one person and the computer or two people) will each \
receive {len(SHIP_SETUP)} ships to place on a designated {grid_consts.GRID_X}x{grid_consts.GRID_Y} grid. Each ship \
will have a unique color as well as a length, and the two players will compete against each other by trying to sink \
their opponent's ships; the player who sinks all of their opponent's ships first is the winner!\nThe ship \
configuration is:\n"

TABLE_COLUMNS = 3
TABLE_ROWS = len(SHIP_SETUP) + 1

# GUI

MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT = 1.0, 0.38461538461
MODE_HEADER_HEIGHT = 1 - 2 * MODE_BUTTON_HEIGHT

ENTRY_COMPONENT_RELATIVE_HEIGHT = 0.4
ENTRY_LABEL_RELATIVE_WIDTH = 0.4
ENTRY_INSTANCE_RELATIVE_WIDTH = 1 - ENTRY_LABEL_RELATIVE_WIDTH

WARNING_DURATION = 2

# Colo(u)r

ENTRY_BACKGROUND_COLOR = util.hex_color_mut(root_consts.ROOT_BACKGROUND_COLOR, lambda n: n * 1.5)

MODE_SELECTION_COLOR_UNSELECTED = util.hex_color_mut(root_consts.ROOT_BACKGROUND_COLOR, lambda n: n * 0.9)
MODE_SELECTION_COLOR_SELECTED = util.hex_color_mut(MODE_SELECTION_COLOR_UNSELECTED, lambda n: n * 0.9)
MODE_SELECTION_COLOR_HOVER = util.hex_color_mut(MODE_SELECTION_COLOR_UNSELECTED, lambda n: n * 0.8)
