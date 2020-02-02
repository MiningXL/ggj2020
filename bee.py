import pygame
import os

from helper import get_surface_pos

from constants import *
from asset import Flower, Wax, Dancer

current_path = os.path.dirname(__file__)

class Bee:
    def __init__(self, grid_pos, id=None, color=None, image='bee_small_2.png'):
        self.grid_pos = grid_pos
        self.id = id
        self.color = color
        self.item = None

        self.image = pygame.image.load(os.path.join(current_path, 'BEE_BODY.png'))
        self.image = pygame.transform.scale(self.image, (2*RADIUS, 2*RADIUS))
        color_bee = pygame.Surface(self.image.get_size()).convert_alpha()
        color_bee.fill(self.color)
        self.image.blit(color_bee, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

        wing_bee = pygame.image.load(os.path.join(current_path, 'BEE_WINGS.png'))
        wing_bee = pygame.transform.scale(wing_bee, (2*RADIUS, 2*RADIUS))
        self.image.blit(wing_bee, (0, 0))

        line_bee = pygame.image.load(os.path.join(current_path, 'BEE_LINES.png'))
        line_bee = pygame.transform.scale(line_bee, (2*RADIUS, 2*RADIUS))
        self.image.blit(line_bee, (0, 0))

        dancing_bee_glasses = pygame.image.load(os.path.join(current_path, 'BEE_Dancing_Sunglases.png'))
        dancing_bee_stars = pygame.image.load(os.path.join(current_path, 'BEE_Dancing_Stars.png'))
        dancing_bee_glasses = pygame.transform.scale(dancing_bee_glasses, (2 * RADIUS, 2 * RADIUS))
        dancing_bee_stars = pygame.transform.scale(dancing_bee_stars, (2 * RADIUS, 2 * RADIUS))

        self.dancing_sprites = [self.image]
        self.dancing_state = 0
        n_steps = 50
        for i in range(1,n_steps):
            dancing_body = pygame.transform.rotate(self.image, 360 / n_steps * i)
            dancing_ovelay_glasses = pygame.transform.rotate(dancing_bee_glasses, 360 / n_steps * i)
            dancing_ovelay_stars = pygame.transform.rotate(dancing_bee_stars, 360 / n_steps * i)
            if i//10 % 2:
                dancing_body.blit(dancing_ovelay_stars, (0,0))
            dancing_body.blit(dancing_ovelay_glasses, (0,0))
            self.dancing_sprites.append(dancing_body)

        basket = pygame.image.load(os.path.join(current_path, 'BEE_Basket_Flowers.png'))
        self.basket = pygame.transform.scale(basket, (2*RADIUS, 2*RADIUS))

        wax = pygame.image.load(os.path.join(current_path, 'BEE_Wax.png'))
        self.wax = pygame.transform.scale(wax, (2 * RADIUS, 2 * RADIUS))

        helmet = pygame.image.load(os.path.join(current_path, 'BEE_helmet_orange.png'))
        self.helmet = pygame.transform.scale(helmet, (2 * RADIUS, 2 * RADIUS))

        self.surface_pos = self.get_target_pos() # current draw position of bee

    def get_target_pos(self):
        return get_surface_pos(self.grid_pos)

    def paint(self, surface):
        bee_pos_shift = (self.surface_pos[0]-self.image.get_height()/2,self.surface_pos[1]-self.image.get_width()/2)

        if self.isdancer():
            # dancing animation
            surface.blit(self.dancing_sprites[self.dancing_state], (bee_pos_shift, (0, 0)))
            self.dancing_state = (self.dancing_state + 1 ) % len(self.dancing_sprites)
        else:
            surface.blit(self.image, (bee_pos_shift, (0, 0)))

        if isinstance(self.item, Flower):
            surface.blit(self.basket, (bee_pos_shift, (0,0)))
        if isinstance(self.item, Wax):
            surface.blit(self.wax, (bee_pos_shift, (0, 0)))
            surface.blit(self.helmet, (bee_pos_shift, (0,0)))

        # radius = surface.get_width() / 2
        # # draw Biene
        # surface.blit(self.image, ((int(radius), int(SQRT3 / 2 * radius)), (0, 0)))

    def new_pos(self, direction):
        pos = self.grid_pos
        direction = direction[pos[1]%2]
        return (pos[0] + direction[0], pos[1] + direction[1])


    def move_bee(self, pos):
        if not isinstance(self.item, Dancer):   # dancing bees cannot move
            self.grid_pos = pos

    def pick_up(self, item):
        print('picked up:', type(item).__name__)
        self.item = item

    def dance(self):
        if self.item is None:
            self.item = Dancer(self.grid_pos)
        elif self.isdancer():
            self.item = None

    def isdancer(self):
        return isinstance(self.item, Dancer)
