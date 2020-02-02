import math
from enum import Enum


DISP_HEIGHT = 600
DISP_WIDTH = 800

GRID_HEIGHT = 20
GRID_WIDTH = 27

# width: 1.65
# height: 1.75
RADIUS = int(min(DISP_HEIGHT/GRID_HEIGHT/1.75, DISP_WIDTH/GRID_WIDTH/1.65))
SQRT3 = math.sqrt(3)
FPS = 30

html_dict = {
    'tl': ((-1, -1),(0, -1)),
    't': ((-1, 0),(-1, 0)),
    'tr': ((-1, 1),(0, 1)),
    'br': ((0, 1),(1,1)),
    'b': ((1, 0),(1,0)),
    'bl': ((0, -1), (1,-1))
}

