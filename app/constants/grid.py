from ..util import hex_color_mut
from .root import ROOT_BACKGROUND_COLOR

GRID_X, GRID_Y = 10, 10

assert GRID_X >= 2, "GRID_X must be at least 2!"
assert GRID_Y >= 2, "GRID_Y must be at least 2!"

RELATIVE_GRID_WIDTH, RELATIVE_GRID_HEIGHT = 0.7, 0.4

RELATIVE_ROTATION_LABEL_SIZE = 0.1
RELATIVE_TURN_LABEL_HEIGHT = 0.1

GRID_COLOR = hex_color_mut(ROOT_BACKGROUND_COLOR, lambda n: n * 1.15)

CELL_DESTROY_COLOR = hex_color_mut(GRID_COLOR, lambda n: n * 0.75)
