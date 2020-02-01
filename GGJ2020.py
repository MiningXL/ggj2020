#   Global Game Jam 2020
#   2020-01-31 bis 2020-02-03

# import
import os
import pygame
import numpy as np
import threading

from map import Map

import random
import queue
import time

from bee import Bee
from htmlhandler import make_app
import tornado
import hive

import bot
from flower import Flower
from intruder import Intruder

pygame.init()

# initialize the pygame module
# load and set the logo
pygame.display.set_caption("First Try")

html_dict = {
    'tl': ((-1, -1),(0, -1)),
    't': ((-1, 0),(-1, 0)),
    'tr': ((-1, 1),(0, 1)),
    'br': ((0, 1),(1,1)),
    'b': ((1, 0),(1,0)),
    'bl': ((0, -1), (1,-1))
}

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
        self.webserver.listen(8090)

        self.hive = hive.Hive()

        self.tornado_target = tornado.ioloop.IOLoop.current()
        self.tornado_thread = threading.Thread(target=self.tornado_target.start)
        self.tornado_thread.start()

    def new_color(self):
        func = (random.randint(0,255) for i in range(3))
        return tuple(func)

    def add_bee(self, id):
        valied = False
        while not valied:
            x = random.randint(0, self.hive.rows)
            y = random.randint(0, self.hive.cols)
            valied = self.hive.is_valid((x,y))

        color = self.new_color()
        self.bees.update({id: Bee((x,y), id=id, color=color)})

        self.bot_queue = queue.Queue()
        self.bot = bot.Bot(self.bot_queue)

        self.flowers = []
        self.flowers_collected = 0
        self.intruders = []

    def handle_bot_queue(self):
        while(not self.bot_queue.empty()):
            item = self.bot_queue.get()
            if item == "flower":
                self.flowers.append(Flower((0,0)))
            if item == "intruder":
                self.intruders.append(Intruder((0,0)))

    def handle_input(self):
        while(not self.queue.empty()):
            id, cmd = self.queue.get()

            if (cmd == "kill") and (id in self.bees):
                del self.bees[id]
            else:
                dir = html_dict[cmd]
                if id in self.bees:
                    self.move_bee(id,dir)
                else:
                    self.add_bee(id)

    #surface.blit(grid, (0, 0))

    def collect_flowers(self):
        to_remove = set([])
        for bee in self.bees.values():
            for i,flower in enumerate(self.flowers):
                if bee.grid_pos == flower.grid_pos:
                    to_remove.add(i)
        self.flowers_collected += len(to_remove)
        if len(to_remove) > 0:
            print("added %d flowers"%len(to_remove))
        self.flowers = [f for i,f in enumerate(self.flowers) if i not in to_remove]


    def animate_bees(self):
        # calculate next position on bee path
        for bee in self.bees.values():
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

    def draw_bees(self, surface=None):
        if surface is None:
            surface = self.screen
        for bee in self.bees.values():
            bee.paint(surface)

    def move_bee(self, id, direction):
        try:
            pos = self.bees[id].new_pos(direction)
            if self.hive.is_valid(pos):
                print('pos:', pos[0], pos[1])
                self.bees[id].move_bee(pos)
        except:
            pass

    def draw_flowers(self, surface=None):
        if surface is None:
            surface = self.screen
        for flower in self.flowers:
            flower.paint(surface)

    def draw_intruders(self, surface=None):
        if surface is None:
            surface = self.screen
        for intruder in self.intruders:
            intruder.paint(surface)

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
                    game.move_bee(xy_move[2],(xy_move[0], xy_move[1]))
                except:
                    pass
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                print("Waiting for Tornado")
                game.tornado_target.stop()
                game.tornado_thread.join(1)
                print("Tornado joined")

        game.handle_input()
        game.handle_bot_queue()
        game.collect_flowers()

        game.animate_bees()
        game.hive.draw_grid(game.screen)
        game.draw_bees()

        game.draw_flowers()
        game.draw_intruders()

        pygame.display.flip()
        # draw a line

        time.sleep(0.04)

    pygame.display.quit()
    pygame.quit()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
