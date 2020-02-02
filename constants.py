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
