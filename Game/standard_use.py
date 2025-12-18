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

        if self.hp > self.max_hp:
            self.hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pg.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pg.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

class DeathCounter:
    def __init__(self, font):
        self.font = font
        self.count = 0

    def draw(self, surface):
        text = self.font.render(f"Deaths: {self.count}", True, (255, 255, 255))
        rect = text.get_rect(topright=(1260, 20)) 
        surface.blit(text, rect)

# Function to create and return the main game surface (window)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
def create_main_surface():
    screen_size = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('chameleon Run!')
    return screen_size

#standard music
def play_music():
    try:
        pg.mixer.music.load('.\\resources\\themesong.mp3')
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(-1)
    except:
        pass

#background
def game_background(background_img, width=None, height=None, menu=False):
    # Determine target size
    target_w = width if width else SCREEN_WIDTH
    target_h = height if height else SCREEN_HEIGHT
    
    if menu:
        target_w = SCREEN_WIDTH
        target_h = SCREEN_HEIGHT

    try:
        background = pg.image.load(f".\\resources\\{background_img}").convert_alpha()
        background = pg.transform.scale(background, (int(target_w), int(target_h)))
    except Exception as e:
        print(f"Error loading background {background_img}: {e}")
        background = pg.Surface((int(target_w), int(target_h)))
        background.fill((100, 100, 255))
    return background
        
