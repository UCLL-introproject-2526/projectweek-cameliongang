import pygame as pg
import random
from level import LEVEL_WIDTH, LEVEL_HEIGHT

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, type_enemy='enemy_1'):
        super().__init__()
        self.type_enemy = type_enemy
        self.speed = 2
        self.damage = 10
        self.animation_index = 0
        
        # Load images with fallback
        self.frames = []
        try:
            # Try loading animation frames if they exist
            enemy_1_1 = pg.image.load('./resources/enemy_1_50x50_1.png').convert_alpha()
            enemy_1_2 = pg.image.load('./resources/enemy_1_50x50_2.png').convert_alpha()
            enemy_1_3 = pg.image.load('./resources/enemy_1_50x50_3.png').convert_alpha()
            enemy_1_4 = pg.image.load('./resources/enemy_1_50x50_4.png').convert_alpha()
            self.frames = [enemy_1_1, enemy_1_2, enemy_1_3, enemy_1_4]
        except Exception as e:
            print(f"Warning: Enemy assets not found ({e}). Using fallback.")
            # Fallback to a red square or potato if available
            try:
                img = pg.image.load('./resources/potato.png').convert_alpha()
                img = pg.transform.scale(img, (50, 50))
                self.frames = [img]
            except:
                surf = pg.Surface((50, 50))
                surf.fill((255, 0, 0)) # Red square fallback
                self.frames = [surf]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y) # Start position from arguments

    def update(self):
        # Animation
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
        # Movement
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = LEVEL_WIDTH

    def render(self, surface, camera):
        shifted_rect = camera.apply_rect(self.rect)
        surface.blit(self.image, shifted_rect)