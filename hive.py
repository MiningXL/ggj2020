import pygame
from constants import *
import itertools as it
from asset import Flower, Intruder, Wax
import perlin

# define secondary functions
class Hive:
    def __init__(self, rows, cols):
        print("rows = ", rows)
        print("cols = ", cols)
        self.rows = rows
        self.cols = cols
        self.cells = list(it.product(range(self.rows),range(self.cols)))
        self.flowers = [Flower((1,1))]
        self.flowers_collected = 0
        self.intruders = []
        self.wax = []
        self.items = [self.flowers, self.intruders, self.wax]
        self.cell_state = perlin.gen_perlin((self.rows, self.cols), 2, 100, 0.5, 1.5)

    def is_valid(self, pos):
        if (pos in self.cells) and (self.cell_state[pos]):
            return True
        else:
            return False

    def exists(self, pos):
        return pos in self.cells

    def draw_grid(self, surface):
        """
        Draws a hex grid, based on the map object, onto this Surface
        """
        surface.fill(pygame.Color('black'))
        unit_cell = [(.5 * RADIUS, 0),
                    (1.5 * RADIUS, 0),
                    (2 * RADIUS, SQRT3 / 2 * RADIUS),
                    (1.5 * RADIUS, SQRT3 * RADIUS),
                    (.5 * RADIUS, SQRT3 * RADIUS),
                    (0, SQRT3 / 2 * RADIUS)]

        r = RADIUS*0.75
        unit_cell_inner = [(.5 * r, 0),
                     (1.5 * r, 0),
                     (2 * r, SQRT3 / 2 * r),
                     (1.5 * r, SQRT3 * r),
                     (.5 * r, SQRT3 * r),
                     (0, SQRT3 / 2 * r)]

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
            points_inner = [(RADIUS/4 + x + left, RADIUS/4 + y + top) for (x, y) in unit_cell_inner]
            # Draw the polygon onto the surface

            if col==3 and row == 4:
                pygame.draw.polygon(surface, (0, 0, 255), points, 0)
            elif self.cell_state[cell]:
                pygame.draw.polygon(surface, (255, 204, 0), points, 0)
                pygame.draw.polygon(surface, (255, 255, 0), points_inner, 0)
            else:
                pygame.draw.polygon(surface, (125, 125, 0), points, 0)

            pygame.draw.polygon(surface, (0,0,0), points, 2)
