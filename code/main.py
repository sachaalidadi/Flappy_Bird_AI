import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")
        self.clock = pygame.time.Clock()
        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(FPS)
            pygame.display.update()
            self.screen.fill(SKY_BLUE)
            # self.screen.fill((255,0,0), self.level.bird.hitbox)
            # for pipe in self.level.pipes:
            #     self.screen.fill((0,255,0), pipe.hitbox_up)
            #     self.screen.fill((0,0,255), pipe.hitbox_down)
            self.level.run()

if __name__ == "__main__":
    game = Game()
    game.run()