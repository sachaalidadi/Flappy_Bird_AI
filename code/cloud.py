import pygame
from settings import *
import random

class Cloud:
    def __init__(self,x = 700):
        self.x = x
        self.y = random.randint(50,400)

        self.img = pygame.image.load("../assets/cloud_texture.png")
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def move(self):
        self.x -= 2
        self.rect.x = self.x