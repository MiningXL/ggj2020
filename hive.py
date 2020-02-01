import pygame
from constants import *

# define secondary functions
def draw_grid(surface, map):
    surface.fill(pygame.Color('white'))
    """
    Draws a hex grid, based on the map object, onto this Surface
    """
    cell = [(.5 * RADIUS, 0),
                 (1.5 * RADIUS, 0),
                 (2 * RADIUS, SQRT3 / 2 * RADIUS),
                 (1.5 * RADIUS, SQRT3 * RADIUS),
                 (.5 * RADIUS, SQRT3 * RADIUS),
                 (0, SQRT3 / 2 * RADIUS)]

    # A point list describing a single cell, based on the radius of each hex
    for col in range(map.cols):
        # Alternate the offset of the cells based on column
        offset = RADIUS * SQRT3 / 2 if col % 2 else 0
        for row in range(map.rows):
            # Calculate the offset of the cell
            top = offset + SQRT3 * row * RADIUS
            left = 1.5 * col * RADIUS
            # Create a point list containing the offset cell
            points = [(x + left, y + top) for (x, y) in cell]
            # Draw the polygon onto the surface

            if col==3 and row == 4:
                #pass
                pygame.draw.polygon(surface, (0, 0, 255), points, 0)
            else:
                pygame.draw.polygon(surface, (255, 255, 0), points, 0)

            pygame.draw.polygon(surface, (0,0,0), points, 2)
