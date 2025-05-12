from ..util import hex_color_mut

DEFAULT_BACKGROUND_COLOR = "#1a2129"

GRID_COLOR = hex_color_mut(DEFAULT_BACKGROUND_COLOR, lambda n: n * 1.15)
