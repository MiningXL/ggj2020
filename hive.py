import pygame
from constants import *
import itertools as it
from asset import Flower, Intruder

# define secondary functions
class Hive:
    def __init__(self):
        self.rows = 5
        self.cols = 6
        self.cells = list(it.product(range(self.rows),range(self.cols)))
        self.flowers = [Flower((1,1))]
        self.flowers_collected = 0
        self.intruders = []
        self.items = [self.flowers, self.intruders]

    def is_valid(self, pos):
        return pos in self.cells

    def draw_grid(self, surface):
        """
        Draws a hex grid, based on the map object, onto this Surface
        """
        surface.fill(pygame.Color('white'))
        unit_cell = [(.5 * RADIUS, 0),
                    (1.5 * RADIUS, 0),
                    (2 * RADIUS, SQRT3 / 2 * RADIUS),
                    (1.5 * RADIUS, SQRT3 * RADIUS),
                    (.5 * RADIUS, SQRT3 * RADIUS),
                    (0, SQRT3 / 2 * RADIUS)]

        # A point list describing a single cell, based on the radius of each hex
        for cell in self.cells:
            row, col = cell
            # Alternate the offset of the cells based on column
            offset = RADIUS * SQRT3 / 2 if col % 2 else 0
            # Calculate the offset of the cell
            top = offset + SQRT3 * row * RADIUS
            left = 1.5 * col * RADIUS
            # Create a point list containing the offset cell
            points = [(x + left, y + top) for (x, y) in unit_cell]
            # Draw the polygon onto the surface

            if col==3 and row == 4:
                #pass
                pygame.draw.polygon(surface, (0, 0, 255), points, 0)
            else:
                pygame.draw.polygon(surface, (255, 255, 0), points, 0)

            pygame.draw.polygon(surface, (0,0,0), points, 2)
