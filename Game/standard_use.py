import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT
import json
import os

SETTINGS_FILE = 'settings.json'

def load_settings():
    global SFX_MUTED
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                SFX_MUTED = data.get('sfx_muted', False)
                
                # Apply Music Volume if mixer init
                if pg.mixer.get_init():
                    vol = data.get('music_volume', 0.3)
                    pg.mixer.music.set_volume(vol)
                    if vol == 0:
                        pg.mixer.music.pause()
        except Exception as e:
            print(f"Error loading settings: {e}")

def save_settings():
    data = {}
    data['sfx_muted'] = SFX_MUTED
    if pg.mixer.get_init():
        # If paused, volume might not be 0 internally, but effectively is silent?
        # MuteButton sets volume to 0. 
        data['music_volume'] = pg.mixer.music.get_volume()
    
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving settings: {e}")

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
        
        draw_hp = max(0, self.hp)
        ratio = draw_hp / self.max_hp
        
        # Inset Logic for Pixel Frame
        # Frame is drawn at x-10, y-10 with size w+20, h+20.
        # This implies a 10px borders.
        # Let's inset the bars by 5px so they sit inside the frame.
        bar_x = self.x + 5
        bar_y = self.y + 5
        bar_w = self.w - 10
        bar_h = self.h - 10
        
        # Draw Back Red
        pg.draw.rect(surface, "red", (bar_x, bar_y, bar_w, bar_h))
        # Draw Front Green
        pg.draw.rect(surface, "green", (bar_x, bar_y, bar_w * ratio, bar_h))
        
        # Draw Frame On Top (Bezel)
        if HealthBar.img_frame:
            # Drawn slightly larger to cover edges
            surface.blit(HealthBar.img_frame, (self.x - 10, self.y - 10))

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
        rect_total = text_total.get_rect(topright=(1260, 15)) # Shifted up 5px
        surface.blit(text_total, rect_total)
        
        # Draw Level Info (top left, below healthbar)
        # Healthbar is usually at (10, 10, 200, 20) -> bottom is 30.
        # So we draw at y=40. -> Shifted to 35?
        # Original was 75. 75-5 = 70.
        level_deaths = self.count - self.previous_level_deaths_snapshot
        
        info_text = f"Level: {level_num} | Deaths: {level_deaths}"
        text_level = self.font.render(info_text, True, (255, 255, 255))
        rect_level = text_level.get_rect(topleft=(19, 70)) # Shifted up 5px
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
    screen_size = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption('Chameleon Quest')
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
        
    return background

# SFX Global State
SFX_MUTED = False

def play_sound(sound):
    """Wrapper to play sounds only if SFX is not muted."""
    if sound and not SFX_MUTED:
        sound.play()

class MuteButton:
    img_on = None
    img_off = None

    def __init__(self, x, y):
        # Increased size slightly for better touch/click area if needed, or keep 40x40
        self.rect = pg.Rect(x, y, 40, 40)
        self.muted = False
        
        # Load Images Lazy
        if MuteButton.img_on is None:
            try:
                # Load and Scale
                raw_on = pg.image.load('./resources/mute_icon_on.png').convert_alpha()
                raw_off = pg.image.load('./resources/mute_icon_off.png').convert_alpha()
                MuteButton.img_on = pg.transform.scale(raw_on, (40, 40))
                MuteButton.img_off = pg.transform.scale(raw_off, (40, 40))
            except Exception as e:
                # Fallback if load fails
                print(f"Failed to load mute icons: {e}")
                MuteButton.img_on = None

    def draw(self, surface):
        if MuteButton.img_on and MuteButton.img_off:
            img = MuteButton.img_off if self.muted else MuteButton.img_on
            surface.blit(img, self.rect)
        else:
            # Fallback Drawing
            color = (200, 50, 50) if self.muted else (50, 200, 50)
            pg.draw.rect(surface, color, self.rect, border_radius=5)
            pg.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)
            # Text Fallback
            font = pg.font.SysFont('Arial', 12, bold=True)
            text_surf = font.render("OFF" if self.muted else "ON", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def toggle(self):
        self.muted = not self.muted
        if self.muted:
            pg.mixer.music.set_volume(0) 
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()
            pg.mixer.music.set_volume(0.3)
        save_settings()
        return self.muted

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.toggle()
                return True
        return False

class SFXButton(MuteButton):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.muted = SFX_MUTED # Sync with global
    
    def toggle(self):
        global SFX_MUTED
        self.muted = not self.muted
        SFX_MUTED = self.muted
        save_settings()
        # No mixer call needed, play_sound checks the flag
        return self.muted
