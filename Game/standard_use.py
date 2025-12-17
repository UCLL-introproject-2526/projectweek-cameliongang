import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT

#health bar creation
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



# Function to create and return the main game surface (window)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
def create_main_surface():
    screen_size = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Camelion Run!')
    return screen_size

#standard music
def play_music():
    try:
        pg.mixer.music.load('.\\resources\\themesong.mp3')
        pg.mixer.music.play(-1)
    except:
        pass

#background
def game_background(background_img, menu = False):
    try:
        if menu == False:
            background = pg.image.load(f".\\resources\\{background_img}").convert()
            background = pg.transform.scale(background, (LEVEL_WIDTH, LEVEL_HEIGHT))
        else:
            background = pg.image.load(f".\\resources\\{background_img}").convert()
            background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = pg.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        background.fill((100, 100, 255))
    return background
        
