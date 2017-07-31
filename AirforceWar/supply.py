import pygame
from random import *

class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.speed = 5
        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width ,self.bg_height = bg_size[0] , bg_size[1]
        self.rect.left , self.rect.bottom = randint(0,self.bg_width - self.rect.width) ,-100
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.bg_height:
            self.rect.bottom += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.bg_width - self.rect.width), -100

class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.speed = 5
        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width ,self.bg_height = bg_size[0] , bg_size[1]
        self.rect.left , self.rect.bottom = randint(0,self.bg_width - self.rect.width) ,-100
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.bg_height:
            self.rect.bottom += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.bg_width - self.rect.width), -100