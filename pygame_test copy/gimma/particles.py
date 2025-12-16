import pygame
from settings import *
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type='dust'):
        super().__init__(groups)
        self.type = type
        self.pos = list(pos)
        
        if self.type == 'dust':
            self.image = pygame.Surface((4, 4))
            self.image.fill(WHITE)
            self.velocity = [random.uniform(-1, 1), random.uniform(-2, -0.5)]
            self.lifetime = random.randint(20, 40)
        elif self.type == 'spark':
            self.image = pygame.Surface((3, 3))
            self.image.fill((255, 200, 50))
            self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
            self.lifetime = random.randint(10, 20)
        elif self.type == 'jump':
            self.image = pygame.Surface((6, 6))
            self.image.fill(WHITE)
            self.velocity = [random.uniform(-2, 2), random.uniform(0, 1)]
            self.lifetime = 15

        self.rect = self.image.get_rect(center=pos)
        self.original_lifetime = self.lifetime

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        
        # Move
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        
        # Effects based on lifetime
        alpha = int(255 * (self.lifetime / self.original_lifetime))
        self.image.set_alpha(alpha)
        
        if self.type == 'dust' or self.type == 'jump':
             # Shrink
             if self.lifetime % 5 == 0:
                 size = self.image.get_width() - 1
                 if size > 0:
                     center = self.rect.center
                     self.image = pygame.transform.scale(self.image, (size, size))
                     self.rect = self.image.get_rect(center=center)
