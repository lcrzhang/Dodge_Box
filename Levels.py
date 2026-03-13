"""
Levels.py — hand-crafted level definitions.

HOW TO ADD A LEVEL:
  1. Create a new Level(...) at the bottom of this file.
  2. Add it to the LEVELS list.

Level(
    platforms = [(x, y, width, height), ...],
    door      = (x, y),          # top-left corner of the exit door
    spawn     = (x, y),          # player spawn position
)

World is 800 x 600.  Floor is at y=560 (40 px tall).
Player is 40 x 40.  Door is 20 wide x 80 tall.
Max jump height ≈ 150 px.  Max horizontal reach ≈ 320 px per jump.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Union


@dataclass
class Level:
    platforms:  List[Tuple[int, int, int, int]]            # (x, y, w, h)
    door:       Tuple[int, int]                             # (x, y) top-left
    spawn:      Tuple[int, int]                             # (x, y) player start

    # Optional theming — hook these up in mygame_client.py when ready
    # background: RGB tuple → solid colour fill
    #             str       → path to a background image
    #             None      → default black
    background: Optional[Union[Tuple[int, int, int], str]] = None
    theme:      Optional[str] = None   # e.g. "cave", "space", "forest"


# ---------------------------------------------------------------------------
# Level definitions — edit freely!
# ---------------------------------------------------------------------------

LEVEL_1 = Level(
    platforms=[
        # Ground
        (0,   560, 800, 40),
        # Staircase going up-right
        (100, 450, 130, 20),
        (260, 350, 130, 20),
        (420, 250, 130, 20),
        (580, 150, 130, 20),
    ],
    door=(740, 480),
    spawn=(20, 515),
    background=(20, 20, 40),   # dark blue
    theme="default",
)

LEVEL_2 = Level(
    platforms=[
        # Ground
        (0,   560, 800, 40),
        # Left pillar platforms
        (50,  430, 120, 20),
        (50,  300, 120, 20),
        # Gap in the middle, high bridge
        (250, 200, 300, 20),
        # Right descent
        (600, 320, 120, 20),
        (600, 440, 120, 20),
    ],
    door=(740, 480),
    spawn=(20, 515),
    background=(40, 15, 15),   # dark red
    theme="cave",
)

# Add your own levels here ↓
# LEVEL_3 = Level(
#     platforms=[...],
#     door=(...),
#     spawn=(...),
# )

LEVELS = [LEVEL_1, LEVEL_2]
