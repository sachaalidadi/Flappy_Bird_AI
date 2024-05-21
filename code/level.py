import pygame
from settings import *
from debug import debug
from bird import Bird
from pipe import Pipe
from cloud import Cloud
import random

class Level:
    def __init__(self):
        # self.bird = Bird()
        self.display_surface = pygame.display.get_surface()
        self.pipes = []
        self.FPS = FPS
        x = 700
        for i in range(3):
            self.pipes.append(Pipe(x=x))
            x += 500
        
        self.clouds = []
        x = 200
        for i in range(3):
            self.clouds.append(Cloud(x=x))
            x += 700
        
        self.birds = []
        self.birds_score = {}
        self.birds_network = {}
        self.bird_alive = 350
        self.max_bird_alive = self.bird_alive
        for i in range(self.bird_alive):
            self.birds.append(Bird())
            self.birds_score[i] = 0
            self.birds_network[i] = self.birds[i].brain.weights
            self.birds_network[i].append(self.birds[i].brain.bias)

        self.pipe = Pipe()
        self.can_pass_next_gen = True
        self.can_accelerate = True
        self.accelerate_time = pygame.time.get_ticks()

    def score_cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.score_time > 700:
            self.can_score = True
    
    def accelerate_cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.accelerate_time > 700:
            self.can_accelerate = True

    def run(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_accelerate:
            if self.FPS == 60:
                self.FPS = 120
            else:
                self.FPS = 60
            self.can_accelerate = False
            self.accelerate_time = pygame.time.get_ticks()
        self.accelerate_cooldown()
        self.can_pass_next_gen = True
        for cloud in self.clouds:
            cloud.move()
            self.display_surface.blit(cloud.img, (cloud.x, cloud.y))
        
        if self.clouds[0].x < -CLOUD_WIDTH:
            self.clouds.pop(0)
            self.clouds.append(Cloud(x=self.clouds[-1].x + 700))

        for i,bird in enumerate(self.birds):
            if not bird.dead:
                bird.update(self.pipes[0])
                self.display_surface.blit(bird.img, (bird.x, bird.y))
                bird.update_score(self.pipes[0])
                self.birds_score[i] = bird.score
                bird.dead = bird.check_pipe_collision(self.pipes[0])
                if bird.dead:
                    self.bird_alive -= 1

        for pipe in self.pipes:
            pipe.update()
            self.display_surface.blit(pipe.pipe_up, (pipe.x,pipe.center_gap - pipe.gap - PIPE_HEIGHT))
            self.display_surface.blit(pipe.pipe_down, (pipe.x,pipe.center_gap))

        if self.pipes[0].x < -PIPE_WIDTH:
            self.pipes.pop(0)
            self.pipes.append(Pipe(x=self.pipes[-1].x + 700))

        font = pygame.font.Font(None, 36)
        max_score = max(self.birds_score.values())
        score_text = font.render("Score: " + str(max_score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
        self.display_surface.blit(score_text, score_rect)


        if (self.bird_alive == 0 or max_score == 100) and self.can_pass_next_gen:
            self.bird_alive = 0
            # self.can_pass_next_gen = False
            self.birds_score = {k: v for k, v in sorted(self.birds_score.items(), key=lambda item: item[1], reverse=True)}
            zero_terms = [k for k, v in self.birds_score.items() if v == 0]
            random.shuffle(zero_terms)
            # print(zero_terms)
            for i, key in enumerate(zero_terms):
                self.birds_score[key] = self.birds_score.pop(zero_terms[i])
            # print(self.birds_score)
            keys = list(self.birds_score.keys())
            self.birds = []
            for i in range(int(self.max_bird_alive*0.2)):
                # print(keys[i])
                weights = self.birds_network[keys[i]]
                bias = weights.pop()
                self.birds.append(Bird(weights=weights, bias=bias))
                self.bird_alive+=1
                for i in range(4):
                    # if i < 2:
                    #     self.birds.append(Bird(mutate=True, weights=weights, bias=bias))
                    #     self.bird_alive+=1
                    # else:
                    #     self.birds.append(Bird())
                    #     self.bird_alive+=1
                    self.birds.append(Bird(mutate=True, weights=weights, bias=bias))
                    self.bird_alive+=1
            # for i in range(20,100):
            #     self.birds.append(Bird(weights=self.birds_network[i-50]))
            self.birds_score = {}
            self.birds_network = {}
            # print(self.bird_alive)
            for i in range(self.bird_alive):
                self.birds_score[i] = 0
                self.birds_network[i] = self.birds[i].brain.weights
                self.birds_network[i].append(self.birds[i].brain.bias)
            self.pipes = []
            x = 700
            for i in range(3):
                self.pipes.append(Pipe(x=x))
                x += 500
            self.clouds = []
            x = 200
            for i in range(3):
                self.clouds.append(Cloud(x=x))
                x += 700