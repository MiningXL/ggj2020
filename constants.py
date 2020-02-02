import math
from enum import Enum


DISP_HEIGHT = 1024
DISP_WIDTH = 1280

GRID_HEIGHT = 25
GRID_WIDTH = 20

# width: 1.65
# height: 1.8
RADIUS = int(min(DISP_HEIGHT/GRID_HEIGHT/1.8, DISP_WIDTH/GRID_WIDTH/1.65))
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

