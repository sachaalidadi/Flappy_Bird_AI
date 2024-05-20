import pygame
from settings import *
from network import Network
from functions import *

class Bird:
    def __init__(self,mutate=False,weights=None,bias=None):
        self.x = 100
        self.y = 200
        self.vel = 0
        self.img = pygame.image.load("../assets/bird_texture.png")
        self.img = pygame.transform.scale(self.img, (BIRD_WIDTH, BIRD_HEIGHT))
        self.rect = self.img.get_rect()
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET)

        self.gravity = 0.5 
        self.brain = Network(mutate,weights,bias)
        self.jumping = False
        self.jump_time = None
        self.dead = False

        self.score = 0
        self.can_score = True
        self.score_time = 0
    
    def check_boundary_collision(self):
        if self.y < 0:
            self.y = 0
            self.vel = 0
        if self.y > HEIGHT - BIRD_HEIGHT:
            self.y = HEIGHT - BIRD_HEIGHT
            self.vel = 0
    
    def check_pipe_collision(self, pipe):
        if self.hitbox.colliderect(pipe.hitbox_up) or self.hitbox.colliderect(pipe.hitbox_down):
            return True
        return False

    def input(self):
        if not self.jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.vel = -10
                self.jumping = True
                self.jump_time = pygame.time.get_ticks()
    
    def act(self,action):
        if not self.jumping:
            if action > 0.5:
                self.vel = -10
                self.jumping = True
                self.jump_time = pygame.time.get_ticks()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.jumping:
            if current_time - self.jump_time > 200:
                self.jumping = False
    
    def move(self):
        self.vel += self.gravity
        self.y += self.vel
        self.hitbox.y = self.y
        self.hitbox.x = self.x
    
    def score_cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.score_time > 700:
            self.can_score = True

    def update_score(self,pipe):
        if self.x > pipe.x + PIPE_WIDTH and self.can_score:
            self.score += 1
            self.can_score = False
            self.score_time = pygame.time.get_ticks()
        self.score_cooldown()
    
    def think(self, pipe):
        input1 = normalize(self.vel, -30,100)
        
        input2 = pipe.x - (self.x + BIRD_WIDTH/2)
        if input2 < 0:
            input2 = 0
        input2 = normalize(input2, 0, PIPE_WIDTH-BIRD_WIDTH)

        input3 = (self.y - BIRD_WIDTH/2) - (pipe.hitbox_up.y+pipe.hitbox_down.y)/2
        input3 = normalize(input3, -HEIGHT, HEIGHT)

        input4 = ((pipe.hitbox_up.y+pipe.hitbox_down.y)/2 + pipe.gap) - (self.y + BIRD_HEIGHT/2)
        input4 = normalize(input4, -HEIGHT, HEIGHT)

        output = self.brain.forward([input1, input2, input3, input4])
        
        return output

        

    def update(self,pipe):
        if not self.dead:
            action = self.think(pipe)
            # self.input()
            self.act(action)
            self.cooldown()
            self.move()
            self.check_boundary_collision()