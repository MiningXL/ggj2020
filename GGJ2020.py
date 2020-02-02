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
    def __init__(self, telegram=False, temperature_game_over=False):
        # Define Screen Size
        self.disp_height = DISP_HEIGHT
        self.disp_width = DISP_WIDTH

        self.t0 = time.time()

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

        self.temperature = 60
        self.temperature_game_over = temperature_game_over
        self.temperature_limits = [0, 210]

        background_path = os.path.join(current_path, 'background_bees.ogg')
        dance_path = os.path.join(current_path, 'wild_bees.ogg')

        self.base_volume = 0.2
        self.background_sound = pygame.mixer.Sound(background_path)
        self.background_sound.set_volume(self.base_volume)
        self.dance_sound = pygame.mixer.Sound(dance_path)
        self.dance_sound.set_volume(self.base_volume)

    def new_color(self):
        # color = colorsys.hsv_to_rgb(random.random(),1,1)
        # return tuple([int(255*i) for i in color])
        color = pygame.Color(0,0,0)
        color.hsva = (random.randint(0,360),100,100,100)
        return (color.r,color.g,color.b)
    # needs futher work
        colors = np.array([colorsys.rgb_to_hsv(*bee.color) for bee in self.bees.values()])
        colors_hue = np.array([c[0] for c in colors])
        if len(colors) <= 2:
            return tuple([255*i for i in colorsys.hsv_to_rgb(random.random(),1,1)])
        else:
            color_diff = np.roll(colors_hue,1) - colors_hue
            print(colors_hue)
            print(color_diff)
            index = np.argmax(np.abs(color_diff))
            print(index)
            new_hue = colors_hue[index]+color_diff[index]/2
            color = (int(255*(new_hue)+255)%255, 255, 255)
            print(new_hue)
            return color

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
                self.hive.place_intruder()

    def handle_input(self):
        while(not self.queue.empty()):
            id, cmd = self.queue.get()

            if (cmd == "kill"):
                try:
                    del self.bees[id]
                except:
                    print("Kill Error")
            elif not id in self.bees:
                self.add_bee(id)
            else:
                if cmd == 'action':
                    self.dance(id)
                    self.repair_comb(id)
                    self.drop_wax(id)
                    self.pick_up(id)
                else:
                    dir = html_dict[cmd]
                    if id in self.bees:
                        self.move_bee(id,dir)
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
                        for intr in self.hive.intruders:
                            if intr.grid_pos == pos:
                                break
                        else: # executed only if intr loop did not break -> no intruder on pos
                            self.hive.cell_state[pos] = 1
                            self.bees[id].item = None
                            return
                        continue # executed if intr loop did break -> pos occupied by intruder

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
        self.temperature = max(self.temperature, 0)

    def draw_flower_machine(self):
        for fm in self.hive.flower_machines:
            fm.draw(self.screen)

    def draw_temperature(self, surface=None):
        if surface is None:
            surface = self.screen
        width = 30
        height = min(210,max(0,int(self.temperature)))

        # temperature warning
        if self.temperature > self.temperature_limits[1]*0.7:
            speedup = (self.temperature-self.temperature_limits[1]*0.7) // 5
            freq = (time.time() - self.t0 )
            warning_level = max(0,int( 255 * (np.sin(freq * speedup))))
            self.screen.fill((0, 0, warning_level))
            self.screen.fill((warning_level, 0, 0))
        elif self.temperature < self.temperature_limits[1]*0.3:
            speedup = 1+(self.temperature_limits[1]*0.3-self.temperature)// 5
            freq = (time.time() - self.t0 )
            warning_level = max(0,int( 255 * (np.sin(freq * speedup))))
            self.screen.fill((0, 0, warning_level))
        else:
            self.screen.fill((0, 0, 0))
        #print(self.temperature)

        thermometer_current = self.thermometer.copy()
        pygame.draw.circle(thermometer_current, (255, 0, 0), (35, 273), 30)
        pygame.draw.rect(thermometer_current, (255,0,0), ((22,247-height), (width,height)))
        thermometer_current.blit(self.thermometer, ((0,0), (0, 0)))

        surface.blit(thermometer_current, ((int(self.disp_width * 0.90),int(self.disp_height * 0.2)), (0, 0)))

    def check_game_over(self):
        if sum(state == 0 for state in self.hive.cell_state.values()) == 0:
            return True
        elif self.temperature_game_over:
            if self.temperature <= self.temperature_limits[0]:
                print("Bees froze to death!")
                return True
            elif self.temperature > self.temperature_limits[1]:
                print("Bees suffocated to the heat!")
                return True
        else:
            return False

    def audio_settings(self):
        num_bees = len(self.bees)
        num_dancer = sum([bee.isdancer() for bee in self.bees.values()])
        pygame.mixer.Channel(1).set_volume(self.audio_function(num_bees))
        pygame.mixer.Channel(2).set_volume(self.audio_function(num_dancer))
        # print(self.background_sound.get_volume())
        # print(pygame.mixer.Channel(1).get_volume())

    def audio_function(self, x):
        return self.base_volume + (1-self.base_volume)*min(1,x/10)


# define a main function
def main():
    game = GameManager()

    pygame.mixer.pre_init()
    pygame.mixer.init()
    # pygame.mixer.music.load(sound_path)

    pygame.mixer.Channel(1).play(game.background_sound, loops=-1)
    pygame.mixer.Channel(2).play(game.dance_sound, loops=-1)

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
                game_over = True
                print("Waiting for Tornado")
                game.tornado_target.stop()
                game.tornado_thread.join(1)
                print("Tornado joined")

        game.handle_input()
        game.handle_bot_queue()
        game.apply_temperature()
        game.audio_settings()

        game.draw_temperature()

        game.animate_bees()
        game.hive.draw_grid(game.screen)
        game.draw_flower_machine()
        game.draw_bees()

        game.draw_flower_machine()
        game.draw_items()

        if not game_over:
            game_over = game.check_game_over()

        pygame.display.flip()
        # draw a line

    pygame.display.quit()
    if hasattr(game, 'bot'):
        game.bot.kill()
    pygame.quit()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
