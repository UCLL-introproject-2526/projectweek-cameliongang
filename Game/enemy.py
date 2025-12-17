import pygame as pg
import random
from level import LEVEL_WIDTH, LEVEL_HEIGHT
class Enemy(pg.sprite.Sprite):
    def __init__(self, type_enemy = 'enemy_1'):
        super().__init__()
        self.type_enemy = type_enemy
   
        # Animatie voor enemy_1
    def load_enemy_1(self, surface):
        try: 
            enemy_1_1 = pg.image.load('./resources/enemy_1_50x50_1.png').convert_alpha()
            enemy_1_2 = pg.image.load('./resources/enemy_1_50x50_2.png').convert_alpha()
            enemy_1_3 = pg.image.load('./resources/enemy_1_50x50_3.png').convert_alpha()
            enemy_1_4 = pg.image.load('./resources/enemy_1_50x50_4.png').convert_alpha()
            self.frames = [enemy_1_1,enemy_1_2,enemy_1_3,enemy_1_4]
        except Exception as e:
                shifted_rect = self.camera.apply_rect(self.rect)
                pg.draw.rect(surface, (255, 0, 0), shifted_rect)
        self.speed = 400  #snelheid van enemy_1 
        self.damage = 10   #schade van enemy_1 

        self.animation_index = 0
        self.image = self.frames[self.animation_index]


    def spawn_enemy_1(self, surface):
        self.load_enemy_1(surface)
        self.rect = self.image.get_rect(midbottom = (LEVEL_WIDTH,LEVEL_HEIGHT-300 ))
        surface.blit(self.rect, (300, 400))
     # Bepalen spawnpoint enemy
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
      
        if self.type_enemy == 'enemy_1':
            x, y = self.rect.midbottom
            x -= self.speed
            if x < 0:
                x = LEVEL_WIDTH
            self.rect.midbottom = (x,y)