import pygame
import os
import math
import random

from constants import SQRT3, RADIUS
from bee import get_surface_pos

current_path = os.path.dirname(__file__)

class Asset:
    def __init__(self, grid_pos, imagename):
        self.grid_pos = grid_pos

        self.image = pygame.image.load(os.path.join(current_path, imagename))
        self.image = pygame.transform.scale(self.image, (2*RADIUS, 2*RADIUS))
        self.surface_pos = get_surface_pos(grid_pos)

    def paint(self, surface):
        bee_pos_shift = (self.surface_pos[0]-self.image.get_height()/2,self.surface_pos[1]-self.image.get_width()/2)
        surface.blit(self.image, (bee_pos_shift,(0,0)))

class Flower(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename=None):
        colors = ["red", "blue", "orange"]
        imagelist = ["flower_" + c + ".png" for c in colors]
        if imagename is None:
            imagename = random.choice(imagelist)

        super().__init__(grid_pos, imagename)

class Intruder(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename="Vasp.png"):
        super().__init__(grid_pos, imagename)
