from . import grid as grid_consts
from ..ship import SHIP_SETUP

text = f"Welcome to Battleships! In this game, two players will each receive {len(SHIP_SETUP)} ships to place on \
a designated {grid_consts.GRID_X}x{grid_consts.GRID_Y} grid. Each ship will have its own name and length, and the two players will compete against each \
other by trying to sink their opponent's ships. The player who sinks all of their opponent's ships first is the winner!\
\nThe ship setup is:\n"
