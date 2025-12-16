import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, type='spiky'):
        super().__init__(pos, groups, obstacle_sprites)
        self.enemy_type = type
        
        if self.enemy_type == 'slime':
             self.image = pygame.image.load('assets/enemy_slime.png').convert_alpha()
             self.power_type = 'sticky'
        else:
             self.image = pygame.image.load('assets/enemy.png').convert_alpha()
             self.power_type = 'fire'

        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # Simple AI
        
        # Simple AI
        self.direction.x = 1
        self.speed = 2

    def update(self):
        # Patrol logic
        # Check for cliff (ground ahead)
        look_ahead_x = self.rect.right + 2 if self.direction.x > 0 else self.rect.left - 2
        look_ahead_rect = pygame.Rect(look_ahead_x, self.rect.bottom + 2, 2, 2)
        
        floor_detected = False
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(look_ahead_rect):
                floor_detected = True
                break
        
        if not floor_detected:
            self.direction.x *= -1

        self.velocity.x = self.direction.x * self.speed
        
        # Move
        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        
        self.apply_gravity()
        self.check_vertical_collision()
        
        # Turn around at walls - basic check
        # Actually within check_horizontal_collision we can't easily see if we hit wall
        # But if velocity.x becomes 0, we hit something
        if self.velocity.x == 0:
            self.direction.x *= -1
