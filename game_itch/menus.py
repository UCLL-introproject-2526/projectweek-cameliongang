import pygame as pg
from standard_use import game_background

import csv
import threading




class Button:
    # Button font defaults (loaded once)
    img_normal = None
    img_pressed = None
    
    def __init__(self, txt , pos):
        self.text = txt
        self.pos = pos
        self.button = pg.rect.Rect((self.pos[0], self.pos[1]), (260,50)) # Hitbox
    
    clicked_state = False 
    just_clicked = False # New flag for one-shot events

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
                # Create smaller variants for navigation
                Button.img_small_norm = pg.transform.scale(raw_norm, (60, 50))
                Button.img_small_press = pg.transform.scale(raw_press, (60, 50))
            except Exception as e:
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
        
        self.just_clicked = False # Reset frame flag
        
        # Sound Logic (Rising Edge) & Click Logic
        if is_pressed and not self.clicked_state:
            # Rising Edge
            if hasattr(Button, "snd_click") and Button.snd_click:
                Button.snd_click.play()
            self.clicked_state = True
            self.just_clicked = True # Signal that a click happened THIS frame
        elif not is_pressed:
            self.clicked_state = False
        
        if Button.img_normal and Button.img_pressed:
            if is_pressed:
                img = Button.img_small_press if self.button.width < 100 else Button.img_pressed
                surface.blit(img, self.button)
                text_offset_y = 10 
            else:
                img = Button.img_small_norm if self.button.width < 100 else Button.img_normal
                surface.blit(img, self.button)
                text_offset_y = 7
        else:
            # Fallback
            color = 'dark gray' if is_pressed else 'light gray'
            pg.draw.rect(surface, color, self.button, 0, 5)
            pg.draw.rect(surface, 'black', self.button, 3, 5)
            text_offset_y = 7

        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.button.center)
        text_rect.y -= 5
        text_rect.y += 2 if is_pressed else 0
        surface.blit(text, text_rect)
    
    def check_clicked(self):
        # Now returns True ONLY on the frame it was pressed
        return self.just_clicked
        

def draw_panel(surface, x, y, w, h):
    # Helper to draw a semi-transparent panel for readability
    s = pg.Surface((w, h))
    s.set_alpha(200) # Semi-transparent
    s.fill((30, 30, 40)) # Dark blue-grey
    surface.blit(s, (x, y))
    # Border
    pg.draw.rect(surface, (200, 200, 200), (x, y, w, h), 2)

        

#Maken van het menu
#Maken van het menu
start_button = Button('Start Game', (500, 300))
levels_button = Button('Choose Level', (500, 400))
leaderboard_button = Button('Leaderboard', (500, 500))
settings_button = Button('Settings', (800, 300)) 
credits_button = Button('Credits', (200, 400))
exit_button = Button('Quit Game', (800, 400))

# Dynamic button for login/logout
login_button = Button('Login', (200, 300))

def draw_mainmenu(surface, font, network):
    surface.fill((0, 0, 0))
    # Reuse background
    try:
        background = game_background('mainmenu_background.png', menu=True)
        surface.blit(background, (0, 0))
    except:
        pass
        
    command = 0
    start_button.draw(surface, font)
    levels_button.draw(surface, font)
    leaderboard_button.draw(surface, font)
    settings_button.draw(surface, font) 
    credits_button.draw(surface, font)
    exit_button.draw(surface, font)
    
    # Login Button Logic
    if network.user:
         login_button.text = "Logout"
         # Show Name
         try:
            dname = network.user.get('user_metadata', {}).get('display_name')
            if not dname: 
                email = network.user.get('email', '')
                dname = email.split('@')[0] if email else "Player"
            
            name_surf = font.render(f"Hi, {dname}", True, "cyan")
            s_rect = name_surf.get_rect(topright=(surface.get_width()-20, 20))
            surface.blit(name_surf, s_rect)
         except: 
            pass
    else:
         login_button.text = "Login"
    login_button.draw(surface, font)

    if exit_button.check_clicked():
        command = 'q'
    if credits_button.check_clicked():
        command = 2
    if levels_button.check_clicked():
        command = 3
    if start_button.check_clicked():
        command = 4
    if settings_button.check_clicked():
        command = 5
    if leaderboard_button.check_clicked():
        command = 6 # Leaderboard
    if login_button.check_clicked():
        if network.user:
             network.logout() # Instant logout
        else:
             command = 7 # Go to Login Menu
             
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
    # Use 'name' from dictionary
    btn_text = lvl.get('name', f"Level {i+1}")
    btn = Button(btn_text, (x, y))
    level_buttons.append((i, btn))

back_button = Button("Back", (500, 600))
prev_button = Button("Prev", (200, 600))
next_button = Button("Next", (800, 600))

def draw_star(surface, center, size, color):
    # Procedural Star
    import math
    points = []
    outer_radius = size
    inner_radius = size / 2.5
    angle = -math.pi / 2 # Start at top
    step = math.pi / 5 # 5 points
    
    for i in range(10):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = center[0] + math.cos(angle) * r
        y = center[1] + math.sin(angle) * r
        points.append((x, y))
        angle += step
    pg.draw.polygon(surface, color, points)
    pg.draw.polygon(surface, "black", points, 1) # Outline

def draw_levels_menu(surface, font, page=0, max_level_reached=1):
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
        
        # Button class stores pos, let's update it.
        btn.pos = (x, y)
        btn.button = pg.rect.Rect((x, y), (260,50)) # Update collision rect
        
        btn.draw(surface, font)
        if btn.check_clicked():
            command = 10 + real_idx # 10=lvl1, 11=lvl2, etc.
            
        # Draw Star if completed
        # Completion Logic: If I am on Level X (real_idx+1), and max_level > real_idx+1, it implies I beat it?
        # Typically max_level_reached means "I can access until here".
        # So if max_level_reached = 5, Level 4 is done. (real_idx 3 + 1 < 5 -> True)
        # Level 5 (real_idx 4) is unlocked but not necessarily done.
        # But if max_level_reached is updated AFTER beating level, equal to "next level idx",
        # then max_level_reached = 2 means Level 1 is done.
        if (real_idx + 1) < max_level_reached:
             # Draw Star top-right of button
             star_pos = (x + 240, y + 10)
             draw_star(surface, star_pos, 15, "gold")
        # Optional: Lock visual? Use grey out if (real_idx + 1) > max_level_reached?
        # User said "dont lock a level". So we keep it clickable and normal.
        
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



back_settings_button = Button('Back', (500, 600))

def draw_settings_menu(surface, font, mute_button):
    surface.fill((0, 0, 0))
    # Reuse background
    try:
        bg = game_background('mainmenu_background.png', menu=True)
        surface.blit(bg, (0, 0))
    except:
        pass
        
    # Draw Mute Button - Center it?
    # Mute button uses absolute position from init (1230, 60).
    # User calls for it "in a new menu called settings".
    # Should we move it to center for this menu?
    # Or just let it stay at top right?
    # "mute button ONLY in the main menu in a new menu called settings"
    # This implies it should be the main feature of this menu.
    # Let's override its position temporarily or draw a new one?
    # Better: Update the mute_button.rect before drawing?
    # No, that affects global state if we switch quickly.
    # But since we are IN the menu, global state IS this menu.
    
    # Let's rely on the passed mute_button but maybe we move it?
    # Or we construct a dedicated one?
    # But `initial.py` owns the instance.
    # Let's just draw it where it is, OR move it to center.
    # User said: "mute button only in the main menu in a new menu... and in the pause menu".
    # This implies it should NOT be on the HUD during gameplay?
    # I'll handle that in `initial.py` (stop drawing it in HUD).
    # For now, let's just make sure it draws here.
    
    # We'll center it for the settings menu
    original_rect = mute_button.rect.copy()
    mute_button.rect.topleft = (620, 300) # Center-ish
    mute_button.draw(surface)
    
    # Reset for next frame/other menus? 
    # This is tricky in a loop.
    # Actually, if we only draw it here and pause menu, we can just keep it at one spot or move it.
    # Let's move it back after drawing to be safe?
    # Or just accept it jumps around if we use the same instance.
    
    # Add label
    lbl = font.render("Mute Music", True, "white")
    surface.blit(lbl, (620 - 20, 260))

    back_settings_button.draw(surface, font)
    
    # Feedback Button
    btn_open_feedback.draw(surface, font)
    
    # Timer Toggle
    global show_timer
    if show_timer:
        btn_toggle_timer.text = "Timer: ON"
    else:
        btn_toggle_timer.text = "Timer: OFF"
    btn_toggle_timer.draw(surface, font)
    
    command = 0
    if btn_open_feedback.check_clicked():
        command = 20 # Open Feedback UI
        
    if back_settings_button.check_clicked():
        command = 2 # Back

    if btn_toggle_timer.check_clicked():
        show_timer = not show_timer
        
    # We must restore rect if we want it to be elsewhere in Pause menu?
    # Pause menu probably wants it elsewhere (e.g. top right or listed).
    mute_button.rect = original_rect
    
    return command

def draw_pause_menu(surface, font, mute_button):
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
    
    # Draw Mute Button in Pause Menu
    # Let's put it top right (standard) or near buttons?
    # User asked for it in pause menu.
    # standard pos (1230, 60) is fine for pause menu (HUD-like).
    mute_button.draw(surface)
    
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

def draw_loading_screen(surface, font, progress, level_name_or_idx, is_name=False):
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
    if is_name:
         text_str = f"Loading {level_name_or_idx}..."
    else:
         text_str = f"Loading Level {level_name_or_idx + 1}..."
         
    text = font.render(text_str, True, (255, 255, 255))
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

class InputBox:
    def __init__(self, x, y, w, h, text='', is_password=False):
        self.rect = pg.Rect(x, y, w, h)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.is_password = is_password
        self.txt_surface = None
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def update(self):
        # Resize the box if the text is too long?
        width = max(200, len(self.text) * 10)
        # self.rect.w = width
        pass

    def draw(self, screen, font):
        # Render the current text.
        display_text = "*" * len(self.text) if self.is_password else self.text
        self.txt_surface = font.render(display_text, True, self.color)
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


# Login Menu Components
# Login Menu Components
# FIXED LAYOUT COORDINATES
# Panel Top (Title): Y=180
# Email: Y=230
# Username: Y=300
# Password: Y=370
# Forgot Pass: Y=440 (Small/Offset)
# Buttons: Y=500
# Back: Y=560

login_email_box = InputBox(526, 230, 228, 32) 
username_box = InputBox(526, 300, 228, 32) 
login_pass_box = InputBox(526, 370, 228, 32, is_password=True)

# Toggle Box for Anonymous - Move to top right of panel or below title?
# Let's put it below title (Y=180 is title). So Y=130 (above panel) or Y=200?
# Maybe top right of the screen? Or just smaller on the panel.
# Let's put it at Y=140 (above title area inside panel)
show_username = True
btn_toggle_anon = Button('Show Name: ON', (510, 130)) 

# Actions
btn_login_action = Button('Login', (350, 480)) 
btn_signup_action = Button('Register', (670, 480)) 
btn_forgot_pass = Button('Forgot Pass?', (510, 420)) # Centered below password
btn_login_back = Button('Back', (510, 550))
login_message = ""

# OTP Reset Components
reset_step = 0 # 0=Normal, 1=Enter Code, 2=New Password
reset_email = "" 
otp_box = InputBox(526, 330, 228, 32) # Replaces Password box in view
btn_verify_otp = Button('Verify Code', (510, 450))
new_pass_box = InputBox(526, 330, 228, 32, is_password=True)
btn_set_pass = Button('Set Password', (510, 450))

# Feedback Components
feedback_box = InputBox(410, 300, 460, 32) # Wider
btn_send_feedback = Button('Send Feedback', (510, 400))
feedback_message = ""
show_feedback_ui = False
btn_open_feedback = Button('Feedback', (620, 200)) # Small button?

# Settings Components
show_timer = True
btn_toggle_timer = Button('Timer: ON', (620, 400)) 

def draw_login_menu(surface, font, network):
    global login_message, reset_step, reset_email
    surface.fill((0, 0, 0))
    # Reuse background
    try:
        bg = game_background('mainmenu_background.png', menu=True)
        surface.blit(bg, (0, 0))
    except:
        pass
    
    # Draw Panel for Readability
    # Screen is 1280x720 typically
    panel_w = 600
    panel_h = 500
    panel_x = (surface.get_width() - panel_w) // 2
    panel_y = (surface.get_height() - panel_h) // 2 + 50 # slightly lower
    draw_panel(surface, panel_x, panel_y, panel_w, panel_h)

    # Titles
    # TITLE
    if reset_step == 0:
        title_str = "Login / Register"
    elif reset_step == 1:
        title_str = "Enter Code"
    elif reset_step == 2:
        title_str = "New Password"
        
    title = font.render(title_str, True, "white")
    surface.blit(title, (panel_x + 220, panel_y + 30))
    
    # ----------------------------
    # STEP 0: LOGIN / REGISTER
    # ----------------------------
    if reset_step == 0:
        lbl_email = font.render("Email:", True, "white")
        surface.blit(lbl_email, (526, 230 - 25)) 
        login_email_box.draw(surface, font)
        
        lbl_user = font.render("Username:", True, "white")
        surface.blit(lbl_user, (526, 300 - 25)) 
        username_box.draw(surface, font)
        
        lbl_pass = font.render("Password:", True, "white")
        surface.blit(lbl_pass, (526, 370 - 25)) 
        login_pass_box.draw(surface, font)
        
        # Buttons
        btn_login_action.draw(surface, font)
        btn_signup_action.draw(surface, font)
        btn_login_back.draw(surface, font)
        
        # Anon Toggle
        # Update text first
        global show_username
        if show_username:
            btn_toggle_anon.text = "Show Name: ON"
        else:
            btn_toggle_anon.text = "Show Name: OFF"
        btn_toggle_anon.pos = (510, 130) # Ensure pos is set if button didn't update
        btn_toggle_anon.button.topleft = (510, 130)
        btn_toggle_anon.draw(surface, font)
        
        # Forgot Pass
        btn_forgot_pass.draw(surface, font)

    # ----------------------------
    # STEP 1: ENTER CODE
    # ----------------------------
    elif reset_step == 1:
        lbl_otp = font.render("Check Email & Enter Code:", True, "white")
        surface.blit(lbl_otp, (526, 280))
        otp_box.draw(surface, font)
        
        btn_verify_otp.draw(surface, font)
        btn_login_back.draw(surface, font)

    # ----------------------------
    # STEP 2: SET NEW PASSWORD
    # ----------------------------
    elif reset_step == 2:
        lbl_new = font.render("Enter New Password:", True, "white")
        surface.blit(lbl_new, (526, 280))
        new_pass_box.draw(surface, font)
        
        btn_set_pass.draw(surface, font)
        btn_login_back.draw(surface, font)
    
    # Message
    if login_message:
        msg_color = "red" if "Error" in login_message or "Offline" in login_message else "green"
        msg_surf = font.render(login_message, True, msg_color)
        surface.blit(msg_surf, (panel_x + 50, panel_y + 450)) # Bottom of panel

    # ----------------------------
    # LOGIC / ACTIONS
    # ----------------------------
    command = 0
    
    # BACK BUTTON (Shared)
    if btn_login_back.check_clicked():
        if reset_step == 0:
            command = 2 # Back to Main
            login_message = ""
        else:
            reset_step = 0 # Cancel Reset
            login_message = ""

    # STEP 0 LOGIC
    if reset_step == 0:
        if btn_toggle_anon.check_clicked():
            show_username = not show_username
        
        if btn_login_action.check_clicked():
            email = login_email_box.text
            password = login_pass_box.text
            res = network.login(email, password)
            if "error" in res:
                 login_message = f"Error: {res['error']}"
            else:
                 login_message = "Logged In!"
                 network.save_session()
        
        if btn_signup_action.check_clicked():
            email = login_email_box.text
            password = login_pass_box.text
            username = username_box.text
            
            if network.contains_profanity(email) or network.contains_profanity(username):
                 login_message = "Error: Invalid Email/Name"
            else:
                # Pass data=metadata for display_name
                res = network.signup(email, password, data={"display_name": username})
                if "error" in res:
                     login_message = f"Error: {res['error']}"
                else:
                     if network.access_token:
                         login_message = "Registered! Auto-logging in..."
                         network.save_session()
                     else:
                         login_message = "Registered! Check Email." 

        if btn_forgot_pass.check_clicked():
            email = login_email_box.text
            if not email or "@" not in email:
                login_message = "Enter Valid Email!"
            else:
                reset_email = email # Store for next steps
                if network.reset_password(email):
                    login_message = "Code Sent! Check Email."
                    reset_step = 1 # Go to Step 1
                else:
                    login_message = "Error Sending Code."

    # STEP 1 LOGIC
    elif reset_step == 1:
        if btn_verify_otp.check_clicked():
            code = otp_box.text
            res = network.verify_otp(reset_email, code)
            if "success" in res:
                login_message = "Verified! Set New Password."
                reset_step = 2 # Go to Step 2
            else:
                login_message = f"Error: {res.get('error')}"

    # STEP 2 LOGIC
    elif reset_step == 2:
        if btn_set_pass.check_clicked():
            new_pw = new_pass_box.text
            res = network.update_password(new_pw)
            if "success" in res:
                login_message = "Password Reset Success! Return to Login."
                reset_step = 0 # Done
            else:
                login_message = f"Error: {res.get('error')}"

    return command

def draw_feedback_menu(surface, font, network):
    global feedback_message
    surface.fill((0,0,0))
    try:
        bg = game_background('mainmenu_background.png', menu=True)
        surface.blit(bg, (0, 0))
    except:
        pass
    
    # Panel
    draw_panel(surface, 340, 100, 600, 500)
    
    title = font.render("Send Feedback", True, "white")
    surface.blit(title, (550, 120))
    
    lbl = font.render("Message (Bugs/Ideas):", True, "white")
    surface.blit(lbl, (410, 270))
    
    feedback_box.draw(surface, font)
    btn_send_feedback.draw(surface, font)
    
    # Back button reuse
    btn_login_back.draw(surface, font)
    
    if feedback_message:
        color = "green" if "Sent" in feedback_message else "red"
        msg = font.render(feedback_message, True, color)
        surface.blit(msg, (400, 550))
        
    command = 0
    if btn_login_back.check_clicked():
        command = 2 # Back
        feedback_message = ""
        
    if btn_send_feedback.check_clicked():
        msg = feedback_box.text
        if network.send_feedback(msg):
            feedback_message = "Sent! Thank you."
            feedback_box.text = "" # Clear
        else:
            feedback_message = "Error sending."
            
    return command

def handle_feedback_input(events):
    for event in events:
        feedback_box.handle_event(event)

def handle_login_input(events):
    for event in events:
        if reset_step == 0:
            login_email_box.handle_event(event)
            username_box.handle_event(event)
            login_pass_box.handle_event(event)
        elif reset_step == 1:
            otp_box.handle_event(event)
        elif reset_step == 2:
            new_pass_box.handle_event(event)


# Leaderboard Menu Components
btn_lb_back = Button("Back", (100, 580)) 
btn_lb_refresh = Button("Refresh", (600, 580))
# Nav buttons initialized with small size via custom pos/rect
# We will override their rects in the draw loop anyway
btn_lb_prev = Button("<", (300, 100)) 
btn_lb_next = Button(">", (900, 100)) 
# Sort Toggles
sort_by_time = False # Default: False (Sort by Deaths)
btn_sort_deaths = Button("Sort: Death", (500, 580)) # Will toggle text

current_lb_level = 0
cached_scores = []
my_cached_score = None # New cache for personal score
last_fetch_time = 0
is_fetching = False

def fetch_worker(level_id):
    global cached_scores, is_fetching, last_fetch_time
    is_fetching = True
    # Simulate slightly longer load or just fetch
    # scores = network.fetch_top_scores(level_id)
    # We need 'network' instance. But thread functions are tricky with arguments.
    # We can pass network to this function.
    pass

def draw_leaderboard_menu(surface, font, network):
    global current_lb_level, cached_scores, last_fetch_time, is_fetching, sort_by_time, my_cached_score
    
    surface.fill((0,0,0))
    try:
        bg = game_background('levels_background.png', menu=True) # Reuse level bg
        surface.blit(bg, (0, 0))
    except:
        pass

    # Draw Panel
    # Large panel for table
    # Draw Panel
    # Large panel for table
    panel_w = 900 # Increased from 800 to fit 3 buttons
    panel_h = 600
    panel_x = (surface.get_width() - panel_w) // 2
    panel_y = (surface.get_height() - panel_h) // 2 + 30
    draw_panel(surface, panel_x, panel_y, panel_w, panel_h)

    # Header with Navigation
    # Center logic: Title in middle. Buttons flanking it.
    
    title = font.render(f"Leaderboard - Level {current_lb_level + 1}", True, "gold")
    title_rect = title.get_rect(center=(surface.get_width()//2, panel_y + 40))
    surface.blit(title, title_rect)
    
    # Position Buttons relative to title
    # Prev button to left of title
    btn_lb_prev.pos = (title_rect.left - 70, panel_y + 15)
    btn_lb_prev.button.topleft = btn_lb_prev.pos
    btn_lb_prev.button.size = (60, 50) # Force small size
    
    btn_lb_next.pos = (title_rect.right + 10, panel_y + 15)
    btn_lb_next.button.topleft = btn_lb_next.pos
    btn_lb_next.button.size = (60, 50) # Force small size
    
    btn_lb_prev.draw(surface, font)
    btn_lb_next.draw(surface, font)
    
    # Offline Check
    if network.is_offline:
        err = font.render("OFFLINE MODE - Reconnect to view scores", True, "red")
        err_rect = err.get_rect(center=(surface.get_width()//2, 300))
        surface.blit(err, err_rect)
    else:
        # Fetch if needed (cache for 10 seconds or on level change)
        current_time = pg.time.get_ticks()
        # Auto-fetch if cache empty or stale AND not currently fetching
        if (not cached_scores or (current_time - last_fetch_time > 10000)) and not is_fetching:
            is_fetching = True
            def task():
                global cached_scores, is_fetching, last_fetch_time, my_cached_score
                # Pass sort param?
                # network.fetch_top_scores currently hardcodes sorting.
                # We need to update network.py to support sorting OR sort client side.
                # Client side is easier for small lists.
                scores = network.fetch_top_scores(current_lb_level + 1)
                
                # Fetch My Score
                my_score = network.get_my_score(current_lb_level + 1)
                my_cached_score = my_score
                
                # Client Side Sort
                if scores:
                    if sort_by_time:
                         # Sort by time_seconds (asc) then deaths (asc)
                         scores.sort(key=lambda x: (x.get('time_seconds', 9999), x.get('deaths', 0)))
                    else:
                         # Sort by deaths (asc) then time_seconds (asc) - Default
                         scores.sort(key=lambda x: (x.get('deaths', 9999), x.get('time_seconds', 0)))
                         
                cached_scores = scores if scores else []
                last_fetch_time = pg.time.get_ticks()
                is_fetching = False
                
            threading.Thread(target=task, daemon=True).start()

        # Loading Indicator
        if is_fetching:
             load_txt = font.render("Loading...", True, "yellow")
             surface.blit(load_txt, (panel_x + panel_w - 150, panel_y + 45))

        # Draw Table Header
        h_y = panel_y + 100
        pg.draw.line(surface, "white", (panel_x + 50, h_y+30), (panel_x + panel_w - 50, h_y+30), 2)
        
        # Columns
        col1_x = panel_x + 50
        col2_x = panel_x + 150
        col3_x = panel_x + 450
        col4_x = panel_x + 600
        
        # Highlight sort column
        c_death = "yellow" if not sort_by_time else "cyan"
        c_time = "yellow" if sort_by_time else "cyan"
        
        surface.blit(font.render("#", True, "cyan"), (col1_x, h_y))
        surface.blit(font.render("Player", True, "cyan"), (col2_x, h_y))
        surface.blit(font.render("Deaths", True, c_death), (col3_x, h_y))
        surface.blit(font.render("Time", True, c_time), (col4_x, h_y))
        
        # Draw Rows
        start_y = h_y + 50
        for i, score in enumerate(cached_scores[:10]): # Limit to 10 visual
            row_y = start_y + (i * 40)
            name = score.get('player_name', 'Unknown')
            deaths = str(score.get('deaths', 0))
            time_s = str(score.get('time_seconds', 0))
            
            color = "white"
            if i == 0: color = "gold"
            elif i == 1: color = "silver"
            elif i == 2: color = "brown"
            
            # Rank
            surface.blit(font.render(str(i+1), True, color), (col1_x, row_y))
            # Name (Truncate)
            if len(name) > 12: name = name[:12] + ".."
            surface.blit(font.render(name, True, color), (col2_x, row_y))
            # Deaths
            surface.blit(font.render(deaths, True, color), (col3_x, row_y))
            # Time
            surface.blit(font.render(time_s + "s", True, color), (col4_x, row_y))

    # Draw "My Score" Footer
    if my_cached_score:
         footer_y = panel_y + panel_h - 100
         pg.draw.line(surface, "gray", (panel_x + 50, footer_y), (panel_x + panel_w - 50, footer_y), 1)
         
         lbl = font.render(f"Your Best:", True, "cyan")
         surface.blit(lbl, (col1_x, footer_y + 10))
         
         # Assuming my_cached_score follows same structure
         deaths_my = str(my_cached_score.get('deaths', 0))
         time_my = str(my_cached_score.get('time_seconds', 0))
         
         surface.blit(font.render(deaths_my, True, "white"), (col3_x, footer_y + 10))
         surface.blit(font.render(time_my + "s", True, "white"), (col4_x, footer_y + 10))

    # Controls (Bottom)
    # Panel Width 900. 3 Buttons x 260 = 780.
    # Spare = 120. 4 gaps (left, btn, gap, btn, gap, btn, right).
    # roughly 30px spacing.
    # B1: 30
    # B2: 30 + 260 + 30 = 320
    # B3: 320 + 260 + 30 = 610
    
    btn_lb_back.pos = (panel_x + 30, panel_y + panel_h - 70)
    btn_lb_back.button.topleft = btn_lb_back.pos
    btn_lb_back.draw(surface, font)
    
    # Sort Button
    btn_sort_deaths.text = "Sort: Time" if sort_by_time else "Sort: Death"
    btn_sort_deaths.pos = (panel_x + 320, panel_y + panel_h - 70)
    btn_sort_deaths.button.topleft = btn_sort_deaths.pos
    btn_sort_deaths.draw(surface, font)
    
    btn_lb_refresh.pos = (panel_x + 610, panel_y + panel_h - 70)
    btn_lb_refresh.button.topleft = btn_lb_refresh.pos
    btn_lb_refresh.draw(surface, font)
    
    command = 0
    if btn_lb_back.check_clicked():
        command = 2 # Back
        
    if btn_sort_deaths.check_clicked():
        sort_by_time = not sort_by_time
        # Invalidate cache to trigger re-sort/fetch logic
        # Ideally we just re-sort locally if we have data?
        # Re-fetch is safer if data changed.
        # But for instantaneous feedback, let's re-sort locally.
        if cached_scores:
            if sort_by_time:
                 cached_scores.sort(key=lambda x: (x.get('time_seconds', 9999), x.get('deaths', 0)))
            else:
                 cached_scores.sort(key=lambda x: (x.get('deaths', 9999), x.get('time_seconds', 0)))
        
    if btn_lb_refresh.check_clicked():
        # Force Fetch
        if not network.is_offline and not is_fetching:
            # Clear cache to show we are doing something?
            cached_scores = [] 
            my_cached_score = None
            is_fetching = True
            def task_force():
                global cached_scores, is_fetching, last_fetch_time, my_cached_score
                scores = network.fetch_top_scores(current_lb_level + 1)
                
                # My Score
                my_score = network.get_my_score(current_lb_level + 1)
                my_cached_score = my_score
                
                if scores:
                    if sort_by_time:
                         scores.sort(key=lambda x: (x.get('time_seconds', 9999), x.get('deaths', 0)))
                    else:
                         scores.sort(key=lambda x: (x.get('deaths', 9999), x.get('time_seconds', 0)))
                
                cached_scores = scores if scores else []
                last_fetch_time = pg.time.get_ticks()
                is_fetching = False
            threading.Thread(target=task_force, daemon=True).start()
            
    if btn_lb_prev.check_clicked():
        if current_lb_level > 0:
            current_lb_level -= 1
            cached_scores = [] # Clear cache
            my_cached_score = None
            is_fetching = False # Trigger new auto fetch
            
    if btn_lb_next.check_clicked():
        current_lb_level += 1
        cached_scores = []
        my_cached_score = None
        is_fetching = False

    return command

# Level Complete Components
btn_lc_next = Button('Next Level', (800, 500))
btn_lc_replay = Button('Replay', (500, 500))
btn_lc_menu = Button('Main Menu', (200, 500))

def draw_level_complete_menu(surface, font, level_idx, time_taken, deaths, new_highscore=False, best_score=None):
    surface.fill((0,0,0))
    try:
        bg = game_background('level_complete_bg.png', menu=True)
        surface.blit(bg, (0,0))
    except:
        pass
        
    title = font.render(f"Level {level_idx + 1} Complete!", True, "gold")
    title_rect = title.get_rect(center=(surface.get_width()//2, 100))
    surface.blit(title, title_rect)
    
    # Stats Panel
    panel_rect = pg.Rect(0, 0, 600, 300)
    panel_rect.center = (surface.get_width()//2, surface.get_height()//2 - 20)
    
    s = pg.Surface((panel_rect.width, panel_rect.height))
    s.set_alpha(180) # Semi-transparent
    s.fill((0,0,0))
    surface.blit(s, panel_rect.topleft)
    pg.draw.rect(surface, "white", panel_rect, 2)
    
    # Stats Text
    t_time = font.render(f"Time: {time_taken:.2f}s", True, "white")
    t_deaths = font.render(f"Deaths: {deaths}", True, "white")
    
    surface.blit(t_time, (panel_rect.x + 50, panel_rect.y + 50))
    surface.blit(t_deaths, (panel_rect.x + 50, panel_rect.y + 100))
    
    # Display Personal Best (if available)
    if best_score:
        best_time = best_score.get('time_seconds', 0)
        best_deaths = best_score.get('deaths', 0)
        pb_txt = font.render(f"Personal Best: {best_time:.2f}s / {best_deaths} deaths", True, "cyan")
        surface.blit(pb_txt, (panel_rect.x + 50, panel_rect.y + 150))
    
    if new_highscore:
        hs_txt = font.render("NEW HIGHSCORE!", True, "yellow")
        surface.blit(hs_txt, (panel_rect.x + 50, panel_rect.y + 200))

    # Buttons
    btn_lc_menu.draw(surface, font)
    btn_lc_replay.draw(surface, font)
    btn_lc_next.draw(surface, font)
    
    command = 0
    if btn_lc_menu.check_clicked(): command = 3 # Main Menu
    if btn_lc_replay.check_clicked(): command = 5 # Replay/Restart
    if btn_lc_next.check_clicked(): command = 4 # Next Level
    
    return command