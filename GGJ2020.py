#   Global Game Jam 2020
#   2020-01-31 bis 2020-02-03

# import
import os
import pygame
import numpy as np
import threading

from map import Map
from hive import draw_grid

import random

import queue

import time

from bee import Bee
from htmlhandler import make_app
import tornado

pygame.init()

# initialize the pygame module
# load and set the logo
pygame.display.set_caption("First Try")


class GameManager:

    def __init__(self):
        # Define Screen Size
        self.disp_height = 600
        self.disp_width = 800

        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))

        self.grid_horizontal = 10
        self.grid_vertical = 15

        self.map = Map(self.grid_vertical, self.grid_horizontal)

        self.bees = {
            0: Bee((3,3), id=0, color=(255,0,0)) ,
            1: Bee((5,1), id=1, color=(0,255,0))
        }

        self.queue = queue.Queue(maxsize=10)

        self.webserver = make_app(self.queue)
        self.webserver.listen(8080)

        threading.Thread(target=tornado.ioloop.IOLoop.current().start).start()

    def handle_input(self):
        while(not self.queue.empty()):
            id, dir = self.queue.get()

            pos = self.bees[id].grid_pos
            pos = (pos[0] + dir[0], pos[1] + dir[1])
            self.bees[id].grid_pos = pos

    #surface.blit(grid, (0, 0))

def draw_bees(surface, bees):
    for bee in bees.values():
        bee_pos_shift = (bee.surface_pos[0]-bee.image.get_height()/2,bee.surface_pos[1]-bee.image.get_width()/2)
        surface.blit(bee.image, (bee_pos_shift,(0,0)))

    pass
    #m.units[(0, 0)] = Unit(m)
    #m.units[(3, 2)] = Unit(m)
def move_bees(bees):
    # calculate next position on bee path
    for bee in bees.values():
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
    game = GameManager()

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

    # define Radius from gridsize and screensize

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.KEYDOWN:
                try:
                    xy_move = key_dict[event.key]
                    pos = game.bees[xy_move[2]].grid_pos
                    pos = (pos[0] + xy_move[0], pos[1] + xy_move[1])
                    if game.map.valid_cell(pos):
                        game.bees[xy_move[2]].grid_pos = pos
                except KeyError:
                    pass
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        game.handle_input()

        move_bees(game.bees)
        draw_grid(game.screen, game.map)
        draw_bees(game.screen, game.bees)

        pygame.display.flip()
        # draw a line

        time.sleep(0.04)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()