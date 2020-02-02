import pygame
from constants import *
import itertools as it
from asset import *
import perlin
import os

from helper import get_surface_pos

current_path = os.path.dirname(__file__)

# define secondary functions
class Hive:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = list(it.product(range(self.rows),range(self.cols)))
        self.flowers = [Flower((1,1)),Flower((3,1))]
        self.flowers_collected = 0
        self.intruders = []
        self.wax = [Wax((2,2))]
        self.flower_machines = []
        self.items = [self.flowers, self.intruders, self.wax]
        self.cell_state = perlin.gen_perlin((self.rows, self.cols), 2, 100, 0.5, 1.5)
        self.platform = pygame.image.load(os.path.join(current_path, 'Platform.png'))
        self.place_flower_machine()

        self.flower_spawn_pos = [(self.rows-1, i) for i in range(int(self.cols/4),int(self.cols/4)+9)]

        w = self.platform.get_width()
        h = self.platform.get_height()
        scaling = 4 * RADIUS/h
        self.platform = pygame.transform.scale(self.platform, (int(w * scaling), int(h * scaling)))


    def place_flower_machine(self):
        while True:
            pos = self.get_random_valid_cell()
            fm = FlowerMachine(pos)
            if self.is_valid(fm.input) and self.is_valid(fm.output):
                self.flower_machines.append(fm)
                return

    def get_random_cell(self):
        return random.choice(self.cells)

    def get_random_valid_cell(self):
        while True:
            pos = self.get_random_cell()
            if self.is_valid(pos):
                return pos

    def place_intruder(self):
        while True:
            pos = self.get_random_cell()
            if not self.is_valid(pos):
                self.intruders.append(Intruder(pos))
                return


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

        # put platform to the left
        (top, left) = get_surface_pos(self.flower_spawn_pos[0])
        surface.blit(self.platform, ((top-RADIUS, left-RADIUS), (0, 0)))

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
