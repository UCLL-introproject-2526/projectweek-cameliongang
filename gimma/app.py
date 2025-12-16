import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gimma - Grapple Platformer")
        self.clock = pygame.time.Clock()
        
        self.level_index = 0
        self.level = Level(self.level_index)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Restart
                         self.level = Level(self.level_index)
                    if event.key == pygame.K_n: # Next level
                         self.level_index = (self.level_index + 1) % len(LEVELS) # Need access to LEVELS import or better level mgmt
                         # Fixed for now to just re-import or handle inside level better
                         # Let's just import LEVELS here simply
                         from level import LEVELS
                         self.level_index = (self.level_index + 1) % len(LEVELS)
                         self.level = Level(self.level_index)

            self.screen.fill(BG_COLOR)
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
