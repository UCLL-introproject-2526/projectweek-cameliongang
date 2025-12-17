import pygame as pg
from standard_use import game_background

class Button:
    def __init__(self, txt , pos):
        self.text = txt
        self.pos = pos
        self.button = pg.rect.Rect((self.pos[0], self.pos[1]), (260,50))

    def draw(self, surface, font):
        pg.draw.rect(surface, 'light gray', self.button, 0, 5)
        pg.draw.rect(surface, 'dark gray', self.button, 5, 5)
        text = font.render(self.text, True, 'black')
        surface.blit(text, (self.pos[0] + 15, self.pos[1] + 7))
    
    def check_clicked(self):
        if self.button.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            return True
        else:
            return False
        

#Maken van het menu
start_button = Button('Start Game', (500, 400))
levels_button = Button('Choose Level', (500, 500))
credits_button = Button('Credits', (200, 500))
exit_button = Button('Quit Game', (800, 500))
def draw_mainmenu(surface, font):
    surface.fill((0, 0, 0))
    background = game_background('mainmenu_background.png', menu=True)
    surface.blit(background, (0, 0))
    command = 0
    start_button.draw(surface, font)
    levels_button.draw(surface, font)
    credits_button.draw(surface, font)
    exit_button.draw(surface, font)
    if exit_button.check_clicked():
        command = 1
    if credits_button.check_clicked():
        command = 2
    if levels_button.check_clicked():
        command = 3
    if start_button.check_clicked():
        command = 4
    return command


#Maken van het menu levels
# Consolidate imports and setup for dynamic menu
from level import LEVELS

# Cache buttons to avoid recreating them every frame
level_buttons = []
for i, lvl in enumerate(LEVELS):
    # Layout buttons: 2 columns? Or just a list?
    # Simple list for now: 2 per row?
    # x: 300, 600... y: 200, 300, 400...
    col = i % 2
    row = i // 2
    x = 300 + (col * 350)
    y = 200 + (row * 100)
    btn = Button(f"Level {i+1}", (x, y))
    level_buttons.append((i, btn))

back_button = Button("Back", (500, 600))

def draw_levels_menu(surface, font):
    surface.fill((0, 0, 0)) # Clear previous screen content
    background = game_background('levels_background.png', menu=True)
    surface.blit(background, (0, 0))
    command = 0
    
    # Draw title
    title = font.render('Select Level', True, 'black')
    surface.blit(title, (500, 100))

    # Draw dynamic buttons
    for idx, btn in level_buttons:
        btn.draw(surface, font)
        if btn.check_clicked():
            command = 10 + idx # 10=lvl1, 11=lvl2, etc.

    back_button.draw(surface, font)
    if back_button.check_clicked():
        command = 2 # Back to main menu (credits command was 2, need to check main menu codes)
        # Actually in initial.py check:
        # 1=Start/Restart, 2=Credits?, 3=LevelSelect, 0=None
    
    return command


# Death Menu Content
# Death Menu Content
# Rearrange for better layout with 4 buttons
# Row 1
restart_button = Button('Restart', (350, 500))
level_select_death_button = Button('Choose Level', (650, 500))
# Row 2
main_menu_death_button = Button('Main Menu', (350, 600))
quit_death_button = Button('Quit Game', (650, 600))

def draw_death_menu(surface, font):
    surface.fill((0, 0, 0))
    background = game_background('gameover_background.jpg', menu=True)
    surface.blit(background, (0, 0))
    # Semi-transparent overlay
    overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0,0))
    
    command = 0
    
    restart_button.draw(surface, font)
    level_select_death_button.draw(surface, font)
    main_menu_death_button.draw(surface, font)
    quit_death_button.draw(surface, font)
    
    if restart_button.check_clicked():
        command = 1 # Restart
    if quit_death_button.check_clicked():
        command = 2 # Quit
    if main_menu_death_button.check_clicked():
        command = 3 # Main Menu
    if level_select_death_button.check_clicked():
        command = 4 # Level Select
        
    return command

def draw_loading_screen(surface, font, progress):
    # Reuse main menu background or black
    surface.fill((0, 0, 0))
    
    # Text
    text = font.render("Loading...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
    surface.blit(text, text_rect)
    
    # Bar Container
    bar_width = 400
    bar_height = 30
    bar_x = (surface.get_width() - bar_width) // 2
    bar_y = surface.get_height() // 2 + 20
    
    # Draw container
    pg.draw.rect(surface, 'white', (bar_x, bar_y, bar_width, bar_height), 2)
    
    # Draw progress
    fill_width = int(bar_width * progress)