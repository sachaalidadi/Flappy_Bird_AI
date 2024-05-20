import pygame
from settings import *
import random

class Pipe:
    def __init__(self,x=700):
        self.center_gap = random.randint(200, HEIGHT - 200)
        # self.center_gap = 400
        self.gap = 200
        self.x = x
        self.y = 2000
        self.pipe_up = pygame.image.load("../assets/pipe_texture_up.png")
        self.pipe_up = pygame.transform.scale(self.pipe_up, (PIPE_WIDTH, PIPE_HEIGHT))
        self.pipe_down = pygame.image.load("../assets/pipe_texture_down.png")
        self.pipe_down = pygame.transform.scale(self.pipe_down, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect_up = self.pipe_up.get_rect()
        self.rect_down = self.pipe_down.get_rect()

        self.hitbox_up = self.rect_up.inflate(-6, HITBOX_OFFSET)
        self.hitbox_down = self.rect_down.inflate(-6, HITBOX_OFFSET)
        self.hitbox_up.y = self.center_gap - self.gap - PIPE_HEIGHT
        self.hitbox_down.y = self.center_gap


        self.velocity = 5
    
    def move(self):
        self.x -= self.velocity
        # if self.x < -PIPE_WIDTH:
        #     self.x = WIDTH
        #     self.center_gap = random.randint(200, HEIGHT - 200)
        #     self.hitbox_up.y = self.center_gap - self.gap - PIPE_HEIGHT
        #     self.hitbox_down.y = self.center_gap

        self.hitbox_up.x = self.x
        self.hitbox_down.x = self.x
    
    def update(self):
        self.move()