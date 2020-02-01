#   Global Game Jam 2020
#   2020-01-31 bis 2020-02-03

# import
import os
import pygame
import numpy as np

from map import Map

import random
import math

import time

summen = True
RADIUS = 40
SQRT3 = math.sqrt( 3 )


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

    #surface.blit(grid, (0, 0))

def draw_bees(surface, bees):
    for bee in bees:
        bee_pos_shift = (bee.surface_pos[0]-bee.image.get_height()/2,bee.surface_pos[1]-bee.image.get_width()/2)
        surface.blit(bee.image, (bee_pos_shift,(0,0)))

    pass
    #m.units[(0, 0)] = Unit(m)
    #m.units[(3, 2)] = Unit(m)
def move_bees(bees):
    # calculate next position on bee path
    for bee in bees:
        target_pos = np.array(bee.get_target_pos())
        current_pos = np.array(bee.surface_pos)
        path = target_pos - current_pos
        #print(np.linalg.norm(path))
        if np.linalg.norm(path) < 5:
            #print("summen")
            r = random.random()
            dir = np.array([r, 1.0-r])
            dir = dir/np.linalg.norm(dir)
            amplitude = random.random() * 2
            bee.surface_pos = current_pos + amplitude * dir
        else:
            #print("move")
            step = 0.4
            bee.surface_pos = current_pos + step * path

            #print(bee.surface_pos)

    #pygame.draw.rect(surface, (255,0,0), ((50,50),(100,100)))

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("First Try")

    # Define Screen Size
    disp_height = 600
    disp_width = 800
    screen = pygame.display.set_mode((disp_width, disp_height))

    # Key Dictionary
    key_dict = {
        # pygame.key : (xmove, ymove, bee_id)
        pygame.K_w : (-1,-1, 0),
        pygame.K_e : (-1,0, 0),
        pygame.K_d : (0,1, 0),
        pygame.K_x : (1,1, 0),
        pygame.K_y : (1,0, 0),
        pygame.K_a : (0,-1, 0),
        pygame.K_u: (-1, -1, 1),
        pygame.K_i: (-1, 0, 1),
        pygame.K_k: (0, 1, 1),
        pygame.K_m: (1, 1, 1),
        pygame.K_n: (1, 0, 1),
        pygame.K_h: (0, -1, 1)
    }

    # define a variable to control the main loop
    running = True

    grid_horizontal = 10
    grid_vertical = 15
    m = Map(grid_horizontal, grid_vertical)

    # define Radius from gridsize and screensize

    bees = [Bee((3,3), id=0, color=(255,0,0)) , Bee((5,1), id=1, color=(0,255,0))]

    # main loop
    while running:
        #
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.KEYDOWN:
                try:
                    xy_move = key_dict[event.key]
                    pos = bees[xy_move[2]].grid_pos
                    pos = (pos[0] + xy_move[0], pos[1] + xy_move[1])
                    if m.valid_cell(pos):
                        bees[xy_move[2]].grid_pos = pos
                except KeyError:
                    pass
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        move_bees(bees)
        draw_grid(screen, m)
        draw_bees(screen, bees)

        pygame.display.flip()
        # draw a line

        time.sleep(0.04)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()