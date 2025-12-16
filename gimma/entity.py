import pygame
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WHITE) # Default placeholder
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 0
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2()


    def apply_gravity(self):
        self.velocity.y += GRAVITY
        if self.velocity.y > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY
        self.rect.y += self.velocity.y

    def check_vertical_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.y > 0: # Falling
                    self.rect.bottom = sprite.rect.top
                    self.velocity.y = 0
                elif self.velocity.y < 0: # Jumping into ceiling
                    self.rect.top = sprite.rect.bottom
                    self.velocity.y = 0

    def check_horizontal_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.x > 0: # Moving right
                    self.rect.right = sprite.rect.left
                elif self.velocity.x < 0: # Moving left
                    self.rect.left = sprite.rect.right
                self.velocity.x = 0

    def update(self):
        # Base update logic, can be overridden but physics should usually be here or called here
        pass
