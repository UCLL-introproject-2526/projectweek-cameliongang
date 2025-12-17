import pygame as pg
import random
from level import LEVEL_WIDTH, LEVEL_HEIGHT
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, type_enemy='enemy_1'):
        super().__init__()
        self.type_enemy = type_enemy
        self.speed = 6
        self.damage = 10
        self.hoveramplitude = 70
        self.hover_speed = 0.1
        self.animation_index = 0
        self.hover_phase = 0
        self.base_y = y
        self.size = (50,50)
        
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
                img = pg.transform.scale(img, self.size)
                self.frames = [img]
            except:
                surf = pg.Surface(self.size)
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
        
        
        self.hover_phase += self.hover_speed
        self.rect.y = self.base_y + int(math.sin(self.hover_phase) * self.hoveramplitude)
        
        self.rect.y = max(0, min(LEVEL_HEIGHT - self.rect.height, self.rect.y))
        #nu gaat die niet meer buiten het scherm
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = LEVEL_WIDTH
            self.base_y = random.randint(1,LEVEL_HEIGHT- self.rect.height)
            self.hover_phase = 0  
            self.rect.y = self.base_y

    def render(self, surface, camera):
        shifted_rect = camera.apply_rect(self.rect)
        surface.blit(self.image, shifted_rect)

