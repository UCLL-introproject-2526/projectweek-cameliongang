import pygame
from settings import *
from particles import Particle

class Bush(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((34, 139, 34)) # Forest Green
        # Make it look a bit bushier?
        pygame.draw.circle(self.image, (0, 100, 0), (16, 16), 16)
        self.image.set_colorkey((0,0,0)) # Transparent corners
        
        self.rect = self.image.get_rect(topleft=pos)
        self.type = 'bush'

class Mine(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Red circle with black border
        pygame.draw.circle(self.image, (50, 50, 50), (16, 16), 12)
        pygame.draw.circle(self.image, (255, 0, 0), (16, 16), 8)
        # Blinking light?
        
        self.rect = self.image.get_rect(topleft=pos)
        self.type = 'mine'
