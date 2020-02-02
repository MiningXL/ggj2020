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

class GameManager:
    def __init__(self, telegram=False):
        # Define Screen Size
        self.disp_height = DISP_HEIGHT
        self.disp_width = DISP_WIDTH

        self.screen = pygame.display.set_mode((self.disp_width, self.disp_height))

        self.grid_height = GRID_HEIGHT
        self.grid_width = GRID_WIDTH

        self.map = Map(self.grid_height, self.grid_width)

        self.bees = {
        }

        self.thermometer = pygame.image.load(os.path.join(current_path, 'Thermometer_grey.png'))

        self.queue = queue.Queue(maxsize=10)

        self.webserver = make_app(self.queue)
        self.webserver.listen(8090)

        self.hive = hive.Hive(self.grid_height, self.grid_width)

        self.tornado_target = tornado.ioloop.IOLoop.current()
        self.tornado_thread = threading.Thread(target=self.tornado_target.start)
        self.tornado_thread.start()

        self.bot_queue = queue.Queue()
        if telegram:
            self.bot = bot.Bot(self.bot_queue)

        self.temperature = 200

    def new_color(self):
        return tuple([255*i for i in colorsys.hsv_to_rgb(random.random(),1,1)])

    def add_bee(self, id):
        valied = False
        while not valied:
            x = random.randint(0, self.hive.rows)
            y = random.randint(0, self.hive.cols)
            valied = self.hive.is_valid((x,y))

        color = self.new_color()
        self.bees.update({id: Bee((x,y), id=id, color=color)})

    def add_flower(self):
        pos_found = False
        while not pos_found:
            pos = self.hive.flower_spawn_pos[random.randint(0,len(self.hive.flower_spawn_pos)-1)]
            if self.hive.is_valid(pos):
                pos_found = True
                self.hive.flowers.append(Flower(pos))

    def handle_bot_queue(self):
        while(not self.bot_queue.empty()):
            item = self.bot_queue.get()
            if item == "flower":
                self.add_flower()
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
                self.dance(id)
                self.repair_comb(id)
                self.drop_wax(id)
                self.pick_up(id)
            else:
                dir = html_dict[cmd]
                if id in self.bees:
                    self.move_bee(id,dir)
                else:
                    self.add_bee(id)

    def dance(self, id):
        bee = self.bees[id]
        bee.dance()

    def drop_wax(self,id):
        bee = self.bees[id]
        for fm in self.hive.flower_machines:
            if bee.grid_pos == fm.input:
                if isinstance(bee.item, Flower):
                    bee.item = None
                    self.hive.wax.append(Wax(fm.output))

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
                self.bees[id].move_bee(pos)
        except:
            pass

    def pick_up(self, id):
        pos = self.bees[id].grid_pos
        for item_list in self.hive.items:
            for i,item in enumerate(item_list):
                if item.grid_pos == pos:
                    del item_list[i]
                    self.drop(id)
                    self.bees[id].pick_up(item)
                    continue

    def drop(self, id):
        item = self.bees[id].item
        if isinstance(item, Flower):
            self.hive.flowers.append(Flower(self.bees[id].grid_pos))
        elif isinstance(item, Wax):
            self.hive.flowers.append(Wax(self.bees[id].grid_pos))
        self.bees[id].item = None

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
        total_dancers = sum(bee.isdancer() for bee in self.bees.values())
        total_bees = len(self.bees)

        self.temperature += float(total_dancers)/(total_bees+1) - 0.25

    def draw_flower_machine(self):
        for fm in self.hive.flower_machines:
            fm.draw(self.screen)

    def draw_temperature(self, surface=None):
        if surface is None:
            surface = self.screen
        width = 30
        height = min(210,max(0,int(self.temperature)))

        thermometer_current = self.thermometer.copy()
        pygame.draw.circle(thermometer_current, (255, 0, 0), (35, 273), 30)
        pygame.draw.rect(thermometer_current, (255,0,0), ((22,247-height), (width,height)))
        thermometer_current.blit(self.thermometer, ((0,0), (0, 0)))

        surface.blit(thermometer_current, ((int(self.disp_width * 0.90),int(self.disp_height * 0.2)), (0, 0)))

    def check_game_over(self):
        if sum(state == 0 for state in self.hive.cell_state.values()) == 0:
            return True
        else:
            return False

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
    game_over = False

    # define Radius from gridsize and screensize
    clock = pygame.time.Clock()
    # main loop
    while not game_over:
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
                if event.key == pygame.K_PLUS:
                    game.add_bee(random.randint(0,100))
                if event.key == pygame.K_SPACE:
                    game.add_flower()
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
        game.draw_flower_machine()
        game.draw_bees()

        # game.draw_flowers()
        # game.draw_intruders()
        game.draw_flower_machine()
        game.draw_items()
        game.draw_temperature()

        game_over = game.check_game_over()

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
