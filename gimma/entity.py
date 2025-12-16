import pygame
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites
        
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = 4
        self.on_ground = False

    def move(self):
        # Default move (can be overridden)
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()

    def apply_gravity(self):
        self.velocity.y += GRAVITY
        if self.velocity.y > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY

    def check_horizontal_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.x > 0:
                    self.rect.right = sprite.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0:
                    self.rect.left = sprite.rect.right
                    self.velocity.x = 0

    def check_vertical_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.velocity.y = 0

    def update(self):
        self.move()
