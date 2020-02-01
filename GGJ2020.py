#   Global Game Jam 2020
#   2020-01-31 bis 2020-02-03

# im
import os
import pygame
import numpy as np
from map import Map
from render import RenderGrid, RenderUnits, SQRT3
import random

import time

summen = True

current_path = os.path.dirname(__file__)

class Bee:
    def __init__(self, grid_pos, render_grid, id=None, color=None, image='bee_small_2.png'):
        self.grid_pos = grid_pos
        self.render_grid = render_grid
        self.id = id
        self.color = color
        self.image = pygame.image.load(os.path.join(current_path, 'bee_small_2.png'))

        self.surface_pos = self.get_target_pos() # current draw position of bee

    def get_target_pos(self):
        return self.render_grid.get_surface_pos(self.grid_pos)

    def paint(self, surface):
        radius = surface.get_width() / 2
        # draw Biene
        surface.blit(self.image, ((int(radius), int(SQRT3 / 2 * radius)), (0, 0)))


# define secondary functions
def draw_grid(surface, grid):
    surface.fill(pygame.Color('white'))
    grid.draw()

    surface.blit(grid, (0, 0))

def draw_bees(surface, bees, render_grid):
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
    grid = RenderGrid(m, radius=30)
    units = RenderUnits(m, radius=30)

    bees = [Bee((3,3), grid, id=0, color=(255,0,0)) , Bee((5,1), grid, id=1, color=(0,255,0))]

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

                """
                if event.key == pygame.K_w:
                    pos = bees[0].grid_pos
                    # pos = (column, row)
                    pos = (pos[0]-1, pos[1]-1)
                    if m.valid_cell(pos):
                        bees[0].grid_pos = pos
                if event.key == pygame.K_e:
                    pos = bees[0].grid_pos
                    pos = (pos[0]-1, pos[1])
                    if m.valid_cell(pos):
                        bees[0].grid_pos = pos
                if event.key == pygame.K_d:
                    pos = bees[0].grid_pos
                    pos = (pos[0], pos[1]+1)
                    if m.valid_cell(pos):
                        bees[0].grid_pos = pos
                if event.key == pygame.K_x:
                    pos = bees[0].grid_pos
                    pos = (pos[0]+1, pos[1]+1)
                    if m.valid_cell(pos):
                        bees[0].grid_pos = pos
                if event.key == pygame.K_y:
                    pos = bees[0].grid_pos
                    pos = (pos[0]+1, pos[1])
                    if m.valid_cell(pos):
                        bees[0].grid_pos = pos
                if event.key == pygame.K_a:
                    pos = bees[0].grid_pos
                    pos = (pos[0], pos[1]-1)
                    bees[0].grid_pos = pos
                """
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        move_bees(bees)
        draw_grid(screen, grid)
        draw_bees(screen, bees, grid)

        pygame.display.flip()
        # draw a line

        time.sleep(0.04)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()