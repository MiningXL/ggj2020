import pygame
import os
import math

from constants import SQRT3, RADIUS

current_path = os.path.dirname(__file__)

def get_surface_pos(pos):
    """
    Returns a subsurface corresponding to the surface, hopefully with trim_cell wrapped around the blit method.
    """
    row = pos[0]
    col = pos[1]
    width = 2 * RADIUS
    height = RADIUS * SQRT3

    midy = (row - math.ceil(col / 2.0)) * height + (height / 2 if col % 2 == 1 else 0) + height/2
    midx = 1.5 * RADIUS * col + width/2

    return (midx, midy)

class Bee:
    def __init__(self, grid_pos, id=None, color=None, image='bee_small_2.png'):
        self.grid_pos = grid_pos
        self.id = id
        self.color = color

        self.image = pygame.image.load(os.path.join(current_path, 'bee_body.png'))
        self.image = pygame.transform.scale(self.image, (2*RADIUS, 2*RADIUS))
        color_bee = pygame.Surface(self.image.get_size()).convert_alpha()
        color_bee.fill(self.color)
        self.image.blit(color_bee, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

        wing_bee = pygame.image.load(os.path.join(current_path, 'bee_wings.png'))
        wing_bee = pygame.transform.scale(wing_bee, (2*RADIUS, 2*RADIUS))
        self.image.blit(wing_bee, (0, 0))

        line_bee = pygame.image.load(os.path.join(current_path, 'bee_lines.png'))
        line_bee = pygame.transform.scale(line_bee, (2*RADIUS, 2*RADIUS))
        self.image.blit(line_bee, (0, 0))

        self.surface_pos = self.get_target_pos() # current draw position of bee

    def get_target_pos(self):
        return get_surface_pos(self.grid_pos)

    def paint(self, surface):
        radius = surface.get_width() / 2
        # draw Biene
        surface.blit(self.image, ((int(radius), int(SQRT3 / 2 * radius)), (0, 0)))
