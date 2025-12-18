import pygame as pg
import random
from level import LEVEL_WIDTH, LEVEL_HEIGHT
import math


ENEMY_CACHE = {}

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 6
        self.damage = 10
        self.hoveramplitude = 15
        self.hover_speed = 0.1
        self.animation_index = 0
        self.hover_phase = 0
        self.base_y = y
        self.size = (50,50)
        self.has_hit_player = False
        
        
        
        self.frames = []
        if 'enemy_frames' in ENEMY_CACHE:
            self.frames = ENEMY_CACHE['enemy_frames']
        else:
            try:
                # Load Animated Fly Spritesheet (2x2 Grid)
                fly_sheet = pg.image.load('./resources/animated_fly.png').convert_alpha()
                
                sheet_w = fly_sheet.get_width()
                sheet_h = fly_sheet.get_height()
                
                cols = 2
                rows = 2
                frame_w = sheet_w // cols
                frame_h = sheet_h // rows
                
                self.frames = []
                for r in range(rows):
                    for c in range(cols):
                        # Extract frame
                        frame_surf = pg.Surface((frame_w, frame_h), pg.SRCALPHA)
                        frame_surf.blit(fly_sheet, (0, 0), (c * frame_w, r * frame_h, frame_w, frame_h))
                        
                        # Scale to enemy size
                        scaled_frame = pg.transform.scale(frame_surf, self.size)
                        self.frames.append(scaled_frame)
                        
                ENEMY_CACHE['enemy_frames'] = self.frames
            except Exception as e:
                print(f"Warning: Animated Fly assets not found ({e}). Using fallback.")
                
                # Check for cached fallback
                if 'fallback_frame' in ENEMY_CACHE:
                    self.frames = ENEMY_CACHE['fallback_frame']
                else:
                    try:
                        img = pg.image.load('./resources/potato.png').convert_alpha()
                        img = pg.transform.scale(img, self.size)
                        self.frames = [img]
                        ENEMY_CACHE['fallback_frame'] = self.frames
                    except:
                        surf = pg.Surface(self.size)
                        surf.fill((255, 0, 0)) 
                        self.frames = [surf]


        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y) 
    def update(self):
        
        self.animation_index += 0.5 # Hyper fast animation (30 FPS visual)
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
            self.rect.right = LEVEL_WIDTH + 500
            self.hover_phase = 0  
            self.rect.y = self.base_y

    def render(self, surface, camera):
        shifted_rect = camera.apply_rect(self.rect)
        surface.blit(self.image, shifted_rect)

    def kill_enemy(self):
        self.rect.right = LEVEL_WIDTH + 750 