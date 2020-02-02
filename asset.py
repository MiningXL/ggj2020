import pygame
import os
import math
import random

from constants import *
from helper import get_surface_pos

current_path = os.path.dirname(__file__)

class Asset:
    def __init__(self, grid_pos, imagename):
        self.grid_pos = grid_pos

        self.image = pygame.image.load(os.path.join(current_path, imagename))
        self.image = pygame.transform.scale(self.image, (int(1.5*RADIUS), int(1.5*RADIUS)))
        self.surface_pos = get_surface_pos(grid_pos)

    def paint(self, surface):
        bee_pos_shift = (self.surface_pos[0]-self.image.get_height()/2,self.surface_pos[1]-self.image.get_width()/2)
        surface.blit(self.image, (bee_pos_shift,(0,0)))

class Flower(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename=None):
        colors = ["red", "blue", "orange", "purple", "turkis"]
        imagelist = ["flower_" + c + ".png" for c in colors]
        if imagename is None:
            imagename = random.choice(imagelist)

        super().__init__(grid_pos, imagename)

class Wax(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename="wax.png"):
        super().__init__(grid_pos, imagename)

class Intruder(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename="Vasp.png"):
        super().__init__(grid_pos, imagename)

class Dancer(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename="wax.png"):
        super().__init__(grid_pos, imagename)

class Weapon(Asset):
    def __init__(self, grid_pos, id=None, color=None, imagename="weapon.png"):
        super().__init__(grid_pos, imagename)

class FlowerMachine:
    def __init__(self,pos):
        self.input = pos
        dir = html_dict['br'][pos[1]%2]
        self.output = (pos[0] + dir[0], pos[1] + dir[1])

        row = self.input[0]
        col = self.input[1]
        # Alternate the offset of the cells based on column
        offset = RADIUS * SQRT3 / 2 if col % 2 else 0
        # Calculate the offset of the cell
        top = offset + SQRT3 * row * RADIUS
        left = 1.5 * RADIUS * col

        self.draw_pos = (left, top)

        self.image = pygame.image.load(os.path.join(current_path, 'Flower_Machine.png'))
        self.image = pygame.transform.scale(self.image, (int(3.5 * RADIUS),  int(1.5 * RADIUS * SQRT3)))

    def draw(self, surface):
        surface.blit(self.image, (self.draw_pos,(0,0)))
