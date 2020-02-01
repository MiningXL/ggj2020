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
from constants import *

import bot
from asset import Flower, Intruder, Wax
from constants import FPS

import colorsys

pygame.init()

current_path = os.path.dirname(__file__)

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


class GameManager:
    def __init__(self, telegram=True):
        # Define Screen Size
        self.disp_height = 600
        self.disp_width = 800

        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))

        self.grid_horizontal = 10
        self.grid_vertical = 15

        self.map = Map(self.grid_vertical, self.grid_horizontal)

        self.bees = {
        }

        self.thermometer = pygame.image.load(os.path.join(current_path, 'Thermometer.png'))

        self.queue = queue.Queue(maxsize=10)

        self.webserver = make_app(self.queue)
        self.webserver.listen(8090)

        self.hive = hive.Hive()

        self.tornado_target = tornado.ioloop.IOLoop.current()
        self.tornado_thread = threading.Thread(target=self.tornado_target.start)
        self.tornado_thread.start()

        self.bot_queue = queue.Queue()
        if telegram:
            self.bot = bot.Bot(self.bot_queue)
        self.flower_machine = FlowerMachine((3,3))

        self.temperature = 50

    def new_color(self):
        return tuple([255*i for i in colorsys.hsv_to_rgb(random.random(),1,1)])
        # func = (random.randint(0,255) for i in range(3))
        # return tuple(func)

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

    def handle_bot_queue(self):
        while(not self.bot_queue.empty()):
            item = self.bot_queue.get()
            if item == "flower":
                self.hive.flowers.append(Flower((0,0)))
            if item == "intruder":
                self.hive.intruders.append(Intruder((0,0)))

    def handle_input(self):
        while(not self.queue.empty()):
            id, cmd = self.queue.get()

            if (cmd == "kill"):
                try:
                    del self.bees[id]
                except:
                    print("Kill Error")
            elif (cmd == 'action') and (id in self.bees):
                self.pick_up(id)
                self.drop(id)
                self.repair_comb(id)
            else:
                dir = html_dict[cmd]
                if id in self.bees:
                    self.move_bee(id,dir)
                else:
                    self.add_bee(id)


    def drop(self,id):
        bee = self.bees[id]
        if bee.grid_pos == self.flower_machine.input:
            if isinstance(bee.item, Flower):
                print("flower dropped!")
                bee.item = None

                self.hive.wax.append(Wax(self.flower_machine.output))


        else:
            print("wrong position for drop")

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
                self.temperature += 2/len(self.bees.keys())
                self.bees[id].move_bee(pos)
        except:
            pass

    def pick_up(self, id):
        pos = self.bees[id].grid_pos
        for item_list in self.hive.items:
            for i,item in enumerate(item_list):
                if item.grid_pos == pos:
                    del item_list[i]
                    self.bees[id].pick_up(item)
                    continue

    def repair_comb(self, id):
        if isinstance(self.bees[id].item, Wax):
            for i in html_dict:
                pos = self.bees[id].new_pos(html_dict[i])
                if self.hive.exists(pos):
                    if not self.hive.cell_state[pos]:
                        self.hive.cell_state[pos] = 1
                        self.bees[id].item = None
                        return

    def draw_items(self, surface=None):
        if surface is None:
            surface = self.screen
        for item_list in self.hive.items:
            for item in item_list:
                item.paint(surface)

    def apply_temperature(self):
        self.temperature -= 0.1

    def draw_flower_machine(self):
        self.flower_machine.draw(self.screen)

    def draw_temperature(self, surface=None):
        if surface is None:
            surface = self.screen
        width = 30
        height = min(210,max(0,int(self.temperature)))

        thermometer_current = self.thermometer.copy()
        pygame.draw.circle(thermometer_current, (255, 0, 0), (35, 273), 30)
        pygame.draw.rect(thermometer_current, (255,0,0), ((22,247-height), (width,height)))
        thermometer_current.blit(self.thermometer, ((0,0), (0, 0)))

        surface.blit(thermometer_current, ((int(self.disp_width * 0.9),int(self.disp_height * 0.2)), (0, 0)))

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
    clock = pygame.time.Clock()
    # main loop
    while running:
        clock.tick(FPS)
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
        game.apply_temperature()

        game.animate_bees()
        game.hive.draw_grid(game.screen)
        game.draw_bees()

        # game.draw_flowers()
        # game.draw_intruders()
        game.draw_flower_machine()
        game.draw_items()
        game.draw_temperature()

        pygame.display.flip()
        # draw a line

    pygame.display.quit()
    game.bot.kill()
    pygame.quit()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
