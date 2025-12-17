import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT

#health bar crezation
class HealthBar:
    def __init__(self, x, y ,w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pg.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pg.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))





#standard music
def play_music():
    try:
        pg.mixer.music.load('.\\resources\\themesong.mp3')
        pg.mixer.music.play(-1)
    except:
        pass

#background
def game_background(surface, player):
    try:
        background = pg.image.load(".\\resources\\background_img.jpg").convert()
        background = pg.transform.scale(background, (LEVEL_WIDTH, LEVEL_HEIGHT))
         # Create a background rect and shift it
        bg_rect = background.get_rect()
        surface.blit(background, player.camera.apply_rect(bg_rect))
    except:
        background = pg.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        background.fill((100, 100, 255))
        
