
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() # CRITICAL: Initialize parent class
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        
        # Topleft puts the top-left corner at 'pos'. 
        # You can also use center=pos
        self.rect = self.image.get_rect(topleft=pos)
        
        self.direction = pygame.math.Vector2()
        self.speed = 400

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: self.direction.x = 1
        elif keys[pygame.K_LEFT]: self.direction.x = -1
        else: self.direction.x = 0

    def update(self, dt):
        self.input()
        # Move the rectangle by Speed * Time * Direction
        self.rect.center += self.direction * self.speed * dt
