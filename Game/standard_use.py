import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT
lvl=Level

#health bar creation
class HealthBar:
    img_frame = None
    img_heart = None
    
    def __init__(self, x, y ,w, h, max_hp):
        self.x = x
        # Shift bar slightly to make room for heart on left?
        # Or assumes x,y is topleft of bar.
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        
        # Load Assets lazy
        if HealthBar.img_frame is None:
            try:
               # Try load
               raw_frame = pg.image.load('./resources/health_bar_frame.png').convert_alpha()
               # Frame should probably stretch to w + padding.
               # Let's say frame adds 10px padding all around.
               # Scale frame to (w + 20, h + 20)
               HealthBar.img_frame = pg.transform.scale(raw_frame, (w + 20, h + 20))
               
               raw_heart = pg.image.load('./resources/heart_icon.png').convert_alpha()
               # Scale heart to match height (h*2?)
               HealthBar.img_heart = pg.transform.scale(raw_heart, (h * 2, h * 2))
            except Exception:
               pass


    def draw(self, surface):
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
        # Ensure HP doesn't drop below 0 for visual
        draw_hp = max(0, self.hp)
            
        ratio = draw_hp / self.max_hp
        
        # Draw Heart (Left of bar) - Draw first or last? Top is nice.
        if HealthBar.img_heart:
            surface.blit(HealthBar.img_heart, (self.x - 50, self.y - 10))
            
        # Draw Frame First (Background)
        if HealthBar.img_frame:
            # Centered over rect. rect is at x,y. size w,h.
            # Frame is w+20, h+20.
            # So frame at x-10, y-10.
            surface.blit(HealthBar.img_frame, (self.x - 10, self.y - 10))
            
        # Draw Back Red (On top of frame)
        pg.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        # Draw Front Green (On top of red)
        pg.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

class DeathCounter:
    def __init__(self, font):
        self.font = font
        self.count = 0
        self.level_count = 0 
        self.previous_level_deaths_snapshot = 0 # To calculate deaths in *current* level

    def reset_level_counter(self):
        self.previous_level_deaths_snapshot = self.count

    def draw(self, surface, level_num=1):
        # Draw Total Deaths (top right)
        text_total = self.font.render(f"Total Deaths: {self.count}", True, (255, 255, 255))
        rect_total = text_total.get_rect(topright=(1260, 20)) 
        surface.blit(text_total, rect_total)
        
        # Draw Level Info (top left, below healthbar)
        # Healthbar is usually at (10, 10, 200, 20) -> bottom is 30.
        # So we draw at y=40.
        level_deaths = self.count - self.previous_level_deaths_snapshot
        
        info_text = f"Level: {level_num} | Deaths: {level_deaths}"
        text_level = self.font.render(info_text, True, (255, 255, 255))
        rect_level = text_level.get_rect(topleft=(19, 75))
        surface.blit(text_level, rect_level)

class Hints:
    def __init__(self, font, pos, text):
        self.font = font
        self.pos = pg.Vector2(pos)
        self.text = text
    
    def draw(self, surface, camera):
        text = self.font.render(self.text, True, (255,255,255))
        rect = text.get_rect()
        rect.topleft = camera.apply_rect(pg.Rect(self.pos, (0,0))).topleft
        surface.blit(text,rect)

  
    

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
        background = pg.Surface((int(target_w), int(target_h)))
        background.fill((100, 100, 255))
    return background
        
