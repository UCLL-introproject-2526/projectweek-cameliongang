import pygame
import random
from level import LEVEL_WIDTH, LEVEL_HEIGHT
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type_enemy = 'enemy_1'):
        super().__init__()
        self.type_enemy = type_enemy

        if self.type_enemy == 'enemy_1':
            self.load_enemy_1()
            self.spawn_enemy_1()
    
        
        
        # Animatie voor enemy_1
    def load_enemy_1(self):
        enemy_1_1 = pygame.image.load('./resources/enemy_1_50x50_1.png').convert_alpha()
        enemy_1_2 = pygame.image.load('./resources/enemy_1_50x50_2.png').convert_alpha()
        enemy_1_3 = pygame.image.load('./resources/enemy_1_50x50_3.png').convert_alpha()
        enemy_1_4 = pygame.image.load('./resources/enemy_1_50x50_4.png').convert_alpha()
        self.frames = [enemy_1_1,enemy_1_2,enemy_1_3,enemy_1_4]
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
           

    def spawn_enemy_1(self, LEVEL_WIDTH):
        self.rect = self.image.get_rect(midbottom = (LEVEL_WIDTH,200 ))
     # Bepalen spawnpoint enemy
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()