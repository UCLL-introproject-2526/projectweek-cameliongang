import pygame as pg
from standard_use import game_background

class Button:
    # Static assets (loaded once)
    img_normal = None
    img_pressed = None
    
    def __init__(self, txt , pos):
        self.text = txt
        self.pos = pos
        self.button = pg.rect.Rect((self.pos[0], self.pos[1]), (260,50)) # Hitbox
    
    clicked_state = False # Track previous frame state

    def ensure_assets(self):
         # Only try loading if display is initialized (needed for convert_alpha)
         if not pg.display.get_init() or not pg.display.get_surface():
             return

         if Button.img_normal is None:
            try:
                # Load and Scale
                # Use absolute path relative to CWD if needed, but './resources' usually fine
                raw_norm = pg.image.load('./resources/button_normal.png').convert_alpha()
                raw_press = pg.image.load('./resources/button_pressed.png').convert_alpha()
                Button.img_normal = pg.transform.scale(raw_norm, (260, 50))
                Button.img_pressed = pg.transform.scale(raw_press, (260, 50))
            except Exception as e:
                # If loading fails (e.g. file missing), set a flag to stop retrying every frame?
                # Or just pass. Printing every frame causes lag.
                pass
         
         # Load Sound
         if not hasattr(Button, "snd_click"):
             try:
                 Button.snd_click = pg.mixer.Sound('./resources/button_click.wav')
                 Button.snd_click.set_volume(0.4)
             except:
                 Button.snd_click = None

    def draw(self, surface, font):
        self.ensure_assets()
        
        # Determine state
        is_hovered = self.button.collidepoint(pg.mouse.get_pos())
        is_pressed = is_hovered and pg.mouse.get_pressed()[0]
        
        # Sound Logic (Rising Edge)
        if is_pressed and not self.clicked_state:
            # Just pressed
            print(f"DEBUG: Button '{self.text}' clicked.")
            if hasattr(Button, "snd_click") and Button.snd_click:
                Button.snd_click.play()
            else:
                print("DEBUG: Button sound missing or not loaded.")
            self.clicked_state = True
        elif not is_pressed:
            self.clicked_state = False
        
        if Button.img_normal and Button.img_pressed:
            if is_pressed:
                surface.blit(Button.img_pressed, self.button)
                # Offset text when pressed for juicy feel
                text_offset_y = 10 
            else:
                surface.blit(Button.img_normal, self.button)
                text_offset_y = 7
        else:
            # Fallback
            color = 'dark gray' if is_pressed else 'light gray'
            pg.draw.rect(surface, color, self.button, 0, 5)
            pg.draw.rect(surface, 'black', self.button, 3, 5)
            text_offset_y = 7

        text = font.render(self.text, True, 'black')
        # Center text?
        text_rect = text.get_rect(center=self.button.center)
        # Apply slight y offset for visual alignment
        # User requested to move ALL text up.
        # Default center might be too low.
        # Let's shift up by 3 pixels from previous.
        text_rect.y -= 5
        
        text_rect.y += 2 if is_pressed else 0
        
        surface.blit(text, text_rect)
    
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
        command = 'q'
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
prev_button = Button("Prev", (200, 600))
next_button = Button("Next", (800, 600))

def draw_levels_menu(surface, font, page=0):
    surface.fill((0, 0, 0)) # Clear previous screen content
    background = game_background('levels_background.png', menu=True)
    surface.blit(background, (0, 0))
    command = 0
    
    # Draw title
    

    # Pagination Logic
    ITEMS_PER_PAGE = 8
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_items = level_buttons[start_idx:end_idx]

    # Draw dynamic buttons
    # We need to re-position them dynamically based on their "slot" on the current page
    # because they were initialized with absolute positions for a single big list (maybe).
    # Actually code above initialized them with row based on 'i'.
    # If we have 100 levels, row 50 is off screen.
    # So we MUST re-calculate position based on visible slot index.
    
    for relative_idx, (real_idx, btn) in enumerate(page_items):
        col = relative_idx % 2
        row = relative_idx // 2
        x = 300 + (col * 350)
        y = 200 + (row * 100)
        
        # Hacky: Update button position on the fly?
        # Or Just create new Render Buttons?
        # Since Button class stores pos, let's update it.
        btn.pos = (x, y)
        btn.button = pg.rect.Rect((x, y), (260,50)) # Update collision rect
        
        btn.draw(surface, font)
        if btn.check_clicked():
            command = 10 + real_idx # 10=lvl1, 11=lvl2, etc.

    back_button.draw(surface, font)
    if back_button.check_clicked():
        command = 2 # Back to main menu
    
    # Draw Pagination Controls
    if page > 0:
        prev_button.draw(surface, font)
        if prev_button.check_clicked():
            command = 8 # Prev Page
            
    if end_idx < len(level_buttons):
        next_button.draw(surface, font)
        if next_button.check_clicked():
            command = 9 # Next Page
    
    return command


# Death Menu Content
# Pause Menu Content (Repurposed Death Menu)
# Rearrange for better layout with 4 buttons
# Row 1
resume_button = Button('Resume', (350, 500))
restart_pause_button = Button('Restart', (650, 500))
# Row 2
main_menu_pause_button = Button('Main Menu', (250, 600))
level_select_pause_button = Button('Choose Level', (550, 600))
quit_pause_button = Button('Quit Game', (850, 600))

def draw_pause_menu(surface, font):
    surface.fill((0, 0, 0))
    # Reuse gameover background or change if desired, keeping as requested
    background = game_background('gameover_background.png', menu=True)
    surface.blit(background, (0, 0))
    # Semi-transparent overlay
    overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0,0))
    
    # Title "PAUSED" could be added here if font available, but buttons suffice
    
    command = 0
    
    resume_button.draw(surface, font)
    restart_pause_button.draw(surface, font)
    level_select_pause_button.draw(surface, font)
    main_menu_pause_button.draw(surface, font)
    quit_pause_button.draw(surface, font)
    
    if resume_button.check_clicked():
        command = 1 # Resume
    if quit_pause_button.check_clicked():
        command = 2 # Quit
    if main_menu_pause_button.check_clicked():
        command = 3 # Main Menu
    if level_select_pause_button.check_clicked():
        command = 4 # Level Select
    if restart_pause_button.check_clicked():
        command = 5 # Restart
        
    return command

def draw_loading_screen(surface, font, progress, level_idx=0):
    # Background
    surface.fill((0, 0, 0))
    try:
        # Use NEW dedicated loading background
        bg = game_background('loading_background.png', menu=True)
        surface.blit(bg, (0,0))
    except:
        # Fallback to main menu if missing
        try:
             bg = game_background('mainmenu_background.png', menu=True)
             surface.blit(bg, (0,0))
        except:
             pass
    
    # Overlay for text readability - Slightly darker
    overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0,0))
    
    # Text
    text = font.render(f"Loading Level {level_idx + 1}...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 55)) # Shifted up 5px (50 -> 55)
    surface.blit(text, text_rect)
    
    # Bar Geometry
    bar_width = 400
    bar_height = 30
    bar_x = (surface.get_width() - bar_width) // 2
    bar_y = surface.get_height() // 2 + 20
    
    # Draw Geometric Bar (Reverted per user request)
    # Trough (Background)
    pg.draw.rect(surface, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
    # Fill
    fill_width = int(bar_width * progress)
    pg.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height))
    # Border
    pg.draw.rect(surface, 'white', (bar_x, bar_y, bar_width, bar_height), 2)