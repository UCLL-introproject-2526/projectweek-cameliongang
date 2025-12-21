import pygame as pg
import random
import time
import sys
import os
from player import Player
from camera import Camera
import level as level_module
import menus # Import module to access globals dynamically
import threading
from level import Level
from menus import draw_level_complete_menu, btn_lc_next, btn_lc_menu, btn_lc_replay, draw_settings_menu, draw_mainmenu, draw_levels_menu, draw_pause_menu, draw_loading_screen, draw_login_menu, draw_leaderboard_menu, handle_login_input, login_email_box, draw_feedback_menu, handle_feedback_input
from network import LeaderboardClient
from standard_use import HealthBar, DeathCounter, Hints, game_background, play_music, create_main_surface, MuteButton, SFXButton, play_sound
from enemy import Enemy
from level import LEVEL_WIDTH, LEVEL_HEIGHT
import json

# Pre-load Icon (Best Effort before init)
try:
    if os.path.exists("resources/app_icon.png"):
        icon = pg.image.load("resources/app_icon.png")
        pg.display.set_icon(icon)
except:
    pass

camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
# create_main_surface imported from standard_use

# ============================================
# LOCAL SCORE STORAGE (NEVER SENT TO SERVER)
# ============================================
def _get_local_scores_path():
    """Get path to local scores file (same directory as executable)."""
    if getattr(sys, 'frozen', False):
        # Running as exe
        exe_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(exe_dir, "local_scores.json")

def load_local_scores():
    """Load local personal bests from JSON file."""
    try:
        with open(_get_local_scores_path(), 'r') as f:
            return json.load(f)
    except:
        return {}  # Empty dict if file doesn't exist

def save_local_scores(scores):
    """Save local personal bests to JSON file."""
    try:
        with open(_get_local_scores_path(), 'w') as f:
            json.dump(scores, f, indent=2)
    except Exception as e:
        print(f"[Local] Failed to save scores: {e}")

def update_local_best(level_id, time_seconds, deaths):
    """Update local best score for a level (keeps best time AND best deaths)."""
    scores = load_local_scores()
    level_key = str(level_id)
    
    if level_key not in scores:
        scores[level_key] = []
    
    # Add new score
    new_score = {"time_seconds": time_seconds, "deaths": deaths}
    scores[level_key].append(new_score)
    
    # Keep only best time and best deaths (max 2 entries)
    level_scores = scores[level_key]
    if len(level_scores) > 1:
        best_time = min(level_scores, key=lambda x: (x['time_seconds'], x['deaths']))
        best_deaths = min(level_scores, key=lambda x: (x['deaths'], x['time_seconds']))
        
        # Keep unique entries
        keep = [best_time]
        if best_deaths != best_time:
            keep.append(best_deaths)
        scores[level_key] = keep
    
    save_local_scores(scores)
    return scores[level_key]

def get_local_best(level_id):
    """Get local best score for a level (returns best overall)."""
    scores = load_local_scores()
    level_key = str(level_id)
    
    if level_key not in scores or not scores[level_key]:
        return None
    
    # Return best deaths, then best time as tiebreaker
    return min(scores[level_key], key=lambda x: (x['deaths'], x['time_seconds']))

# ============================================

# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    
    # Initial Loading Screen with Logo
    surface.fill((0,0,0))
    
    # Load Logo
    try:
        logo_img = pg.transform.scale(pg.image.load('./resources/game_logo.png').convert_alpha(),(500,500))
        logo_rect = logo_img.get_rect(center=(surface.get_width()//2, surface.get_height()//2 - 20)) # Slightly up to fit text below if needed
        surface.blit(logo_img, logo_rect)
    except:
        # Fallback text if logo fails
        font_loading = pg.font.Font(None, 48)
        text = font_loading.render("CAMELION GANG", True, (255, 255, 255))
        rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
        surface.blit(text, rect)

   
    
    pg.display.flip()

    # Wait for 3.7 seconds or until SPACE is pressed
    start_wait = time.time()
    waiting = True
    while waiting and (time.time() - start_wait < 3.7):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False
        pg.time.wait(10) 
                    

    # No asyncio.sleep here for synchronous desktop version
    
    clock = pg.time.Clock()
    
    current_level_idx = 0
    lvl = Level(current_level_idx)
    
    # Initialize Network Client
    network = LeaderboardClient()
    # Try Restore Session
    network.load_session()
    
    # Track Progress
    max_level_reached = 1
    if network.user:
         progress = network.get_user_progress()
         if progress:
             max_level_reached = progress.get('max_level_reached', 1)
             print(f"Cloud Progress Loaded: Max Level {max_level_reached}")
    
    camera = Camera(level_module.LEVEL_WIDTH, level_module.LEVEL_HEIGHT)
    player = Player(lvl, camera) # Player now takes level and camera
    
    game_over = False
    # Initialize enemies from level
    enemies = [Enemy(pos[0], pos[1]) for pos in lvl.enemy_spawns]
    
    # Debug
    show_hitboxes = False

    running = True
    levels_menu = False
    settings_menu = False
    leaderboard_menu = False
    login_menu = False
    feedback_menu = False
    
    main_menu = True
    loading_menu = False
    loading_timer = 0
    LOADING_DURATION = 120 # 2 seconds at 60 FPS
    
    # App Icon
    try:
        if os.path.exists("resources/app_icon.png"):
            icon = pg.image.load("resources/app_icon.png")
            pg.display.set_icon(icon)
    except:
        pass
    
    level_complete_menu = False
    new_highscore = False
    deaths_this_level = 0
    level_elapsed_time = 0.0
    user_best_score = None  # For displaying personal best on stats screen
    
    # App Icon moved to top of file for instance loading

    death_menu = False
    pause_menu = False
    font = pg.font.Font('.\\resources\\ARIAL.TTF', 24)
    
    health_bar = HealthBar(20, 20, 300, 40, 100)
    death_counter = DeathCounter(font)
    mute_button = MuteButton(1230, 60)
    shoot=False
    
    # Initialize hints
    hints = [
        Hints(font, (128, 128), "Use arrow keys or A/D to move left and right"),
        Hints(font, (128, 160), "Press 'Space' or 'W' to Jump"),
        Hints(font, (604, 1408), "While on wall, press jump and move left or right to jump off"),
        Hints(font, (1344, 576), "Press 'G' or 'Left Mouse' to grapple"),
        Hints(font, (783, 576), "Let go of grapple early to swing furhter!"),
        Hints(font, (132, 843), "Click right mouse to shoot tongue"),
                ]
    

    #music playing
    play_music()
    from standard_use import load_settings
    load_settings()
    # Sync initial mute state
    if pg.mixer.music.get_volume() == 0:
        mute_button.muted = True

    #background
    # Draw Game
    bg = game_background('background_img.jpg', width=level_module.LEVEL_WIDTH, height=level_module.LEVEL_HEIGHT)
    surface.blit(bg, (0, 0)) # Parallax/Static?
    facing_left = False
    facing_right = True
    
    # Delta time initialization
    # Delta time initialization
    dt_factor = 1.0
    
    levels_page = 0 # Track current page in level selector
    
    # Input Cooldown to prevent button overlap click-through
    menu_click_cooldown = 0
    
    level_start_time = time.time()
    level_elapsed_time = 0
    timer_started = False # New Flag


    while running:
        
        # Decrement cooldown
        if menu_click_cooldown > 0:
            menu_click_cooldown -= 1
            
        dx = 0
        if main_menu:
             levels_page = 0 # Reset page when returning to main menu
             command = draw_mainmenu(surface, font, network)
             
             if menu_click_cooldown == 0:
                if command == 'q':
                    running = False
                if command == 2: # Credits (not implemented?)
                    pass
                if command == 2: # Credits (not implemented?)
                    pass
                if command == 3: # Levels
                    # Pass max_level logic here?
                    # For now just open menu.
                    main_menu = False
                    levels_menu = True
                    levels_page = 0
                    menu_click_cooldown = 15 # Wait 15 frames
                if command == 4: # Start
                    main_menu = False
                    # Start Game (Level 1 / idx 0)
                    current_level_idx = 0
                    levels_menu = False 
                    # Reset game?
                    player.reset(health_bar)
                    # Trigger load
                    loading_menu = True
                    loading_timer = 0
                    menu_click_cooldown = 15
                if command == 6: # Leaderboard
                    main_menu = False
                    leaderboard_menu = True
                    menu_click_cooldown = 15
                if command == 7: # Login
                    main_menu = False
                    login_menu = True
                    menu_click_cooldown = 15
                if command == 5: # Settings
                     main_menu = False
                     settings_menu = True
                     menu_click_cooldown = 15
                     
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                    if event.key == pg.K_m:
                        mute_button.toggle()
             pg.display.flip()
             # Still tick clock to keep menu framing consistent, but we don't need dt for menu logic yet
             clock.tick(60)
             continue
             
        elif login_menu:
             events = pg.event.get()
             handle_login_input(events) # Pass events to input boxes
             
             command = draw_login_menu(surface, font, network)
             
             if menu_click_cooldown == 0:
                 if command == 2: # Back
                     login_menu = False
                     main_menu = True
                     menu_click_cooldown = 15
             
             for event in events:
                 if event.type == pg.QUIT: running = False
            
             pg.display.flip()
             clock.tick(60)
             continue



        elif feedback_menu:
             events = pg.event.get()
             handle_feedback_input(events)
             command = draw_feedback_menu(surface, font, network)
             if menu_click_cooldown == 0:
                 if command == 2: # Back
                      feedback_menu = False
                      settings_menu = True
                      menu_click_cooldown = 15
             
             for event in events:
                 if event.type == pg.QUIT: running = False
            
             pg.display.flip()
             clock.tick(60)
             continue

        elif leaderboard_menu:
             command = draw_leaderboard_menu(surface, font, network)
             
             if menu_click_cooldown == 0:
                 if command == 2: # Back
                     leaderboard_menu = False
                     main_menu = True
                     menu_click_cooldown = 15
             
             for event in pg.event.get():
                 if event.type == pg.QUIT: running = False
            
             pg.display.flip()
             clock.tick(60)
             continue
        elif level_complete_menu:
             cmd = draw_level_complete_menu(surface, font, current_level_idx, level_elapsed_time, deaths_this_level, new_highscore, user_best_score)
            
             # 3=Menu, 4=Next, 5=Replay
             if cmd == 3: # Main Menu
                 level_complete_menu = False
                 main_menu = True
                 player.reset(health_bar)
                 current_level_idx = 0 
                
             elif cmd == 4: # Next Level
                 level_complete_menu = False
                 current_level_idx += 1
                 if current_level_idx >= len(level_module.LEVELS):
                     current_level_idx = 0
                     main_menu = True
                 else:
                     loading_menu = True
                     loading_timer = 0
                    
             elif cmd == 5: # Replay
                 level_complete_menu = False
                 player.reset(health_bar)
                 player.level_complete = False  # CRITICAL: Reset completion flag!
                 # Reset Timer
                 timer_started = False
                 level_elapsed_time = 0
                 death_counter.previous_level_deaths_snapshot = death_counter.count
             
             # EVENT HANDLING (was missing!)
             for event in pg.event.get():
                 if event.type == pg.QUIT:
                     running = False
                 if event.type == pg.KEYDOWN:
                     if event.key == pg.K_f:
                         pg.display.toggle_fullscreen()
                     if event.key == pg.K_m:
                         mute_button.toggle()
             
             pg.display.flip()
             clock.tick(60)
             continue

        elif loading_menu:
            # ... loading logic ... (abbreviated for context match)
             loading_timer += 1
             
             # Perform heavy loading on the first few frames to ensure UI has rendered at least once
             if loading_timer == 5: # Small delay to let "Loading..." appear
                 # Re-init level
                 lvl = Level(current_level_idx)
                 # Re-init camera with new dimensions
                 camera = Camera(level_module.LEVEL_WIDTH, level_module.LEVEL_HEIGHT)
                 
                 # Reload background to match new level size
                 bg = game_background('background_img.jpg', width=level_module.LEVEL_WIDTH, height=level_module.LEVEL_HEIGHT)
                 
                 # Re-init enemies for the new level
                 enemies = [Enemy(pos[0], pos[1]) for pos in lvl.enemy_spawns]
                 
             progress = loading_timer / LOADING_DURATION
             # Use lvl.name if available, otherwise fallback
             lvl_name = getattr(lvl, 'name', f"Level {current_level_idx + 1}")
             draw_loading_screen(surface, font, progress, lvl_name, is_name=True)
             

             
             if loading_timer >= LOADING_DURATION:
                # Reset level-specific deaths for new level
                death_counter.reset_level_counter()
                
                loading_menu = False
                  # Game starts now - Initialize Player here to cover the load time
                 # Ensure lvl/camera are ready (they should be from timer==5)
                player = Player(lvl, camera)
                # Reset Timer on Load Complete
                timer_started = False
                level_elapsed_time = 0
             # Handle events for loading screen (quit)
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                    if event.key == pg.K_m:
                        mute_button.toggle()
             
             pg.display.flip()
             clock.tick(60)
             continue

        elif levels_menu:
            command = draw_levels_menu(surface, font, levels_page, max_level_reached)
            if menu_click_cooldown == 0:
                if command == 2: # Back
                    levels_menu = False
                    main_menu = True
                    menu_click_cooldown = 15
                if command == 8: # Prev Page
                    if levels_page > 0: levels_page -= 1
                    menu_click_cooldown = 15
                if command == 9: # Next Page
                    levels_page += 1
                    menu_click_cooldown = 15
                if command >= 10: # Level Selection
                    lvl_idx = command - 10
                    # No Lock Check as requested
                    current_level_idx = lvl_idx
                    levels_menu = False
                    player.reset(health_bar)
                    loading_menu = True
                    loading_timer = 0
                    menu_click_cooldown = 15
            
            for event in pg.event.get():
                if event.type == pg.QUIT: running = False
            
            pg.display.flip()
            clock.tick(60)
            continue

            
        elif settings_menu:
            command = draw_settings_menu(surface, font, mute_button)
            
            # Handle Mute Button Event explicitly here since it's clickable in this menu
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                mute_button.handle_event(event) # Keep existing logic
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                    # Mute button toggles via handle_event, but hotkey is good too
                    if event.key == pg.K_m:
                        mute_button.toggle()

            if menu_click_cooldown == 0:
                if command == 2: # Back
                    settings_menu = False
                    main_menu = True
                    menu_click_cooldown = 15
            
            pg.display.flip()
            clock.tick(60)
            continue 

        elif pause_menu:
             command = draw_pause_menu(surface, font, mute_button)
             
             if menu_click_cooldown == 0:
                 if command == 1: # Resume
                     pause_menu = False
                     menu_click_cooldown = 15
                 if command == 2: # Quit
                     running = False
                 if command == 3: # Main Menu
                     pause_menu = False
                     main_menu = True
                     menu_click_cooldown = 15
                 if command == 4: # Level Select
                     pause_menu = False
                     levels_menu = True
                     menu_click_cooldown = 15 # IMPORTANT: Prevent click-through
                 if command == 5: # Restart
                     player.reset(health_bar)
                     # Full State Reset
                     timer_started = False
                     level_elapsed_time = 0
                     death_counter.reset_level_counter() # Reset "Deaths this Level" to 0
                     
                     pause_menu = False
                     menu_click_cooldown = 15
             
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                    if event.key == pg.K_m:
                        mute_button.toggle()
             
             pg.display.flip()
             clock.tick(60)
             continue

        else:
            # Main Gameplay Loop
            
            # Timer Start Logic
            if not timer_started:
                # Check for input
                keys = pg.key.get_pressed()
                mouse = pg.mouse.get_pressed()
                input_detected = False
                
                # Check Movement Keys
                if keys[pg.K_LEFT] or keys[pg.K_a] or keys[pg.K_RIGHT] or keys[pg.K_d]:
                    input_detected = True
                # Check Jump/Action Keys
                if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE] or keys[pg.K_z]:
                     input_detected = True
                # Check Grapple/Tongue Keys
                if keys[pg.K_e] or keys[pg.K_g] or keys[pg.K_q]: # Q is technically left in some layouts but listed in logic
                     input_detected = True
                # Check Mouse
                if mouse[0] or mouse[2]: # Left or Right Click
                     input_detected = True
                     
                if input_detected:
                    timer_started = True
                    level_start_time = time.time()
            
            # Update timer continuously if started
            if timer_started:
                 level_elapsed_time = time.time() - level_start_time
            else:
                 level_elapsed_time = 0.0
            
            # Handling events
            
            # Enemy spawning from level (static) - No longer random spawning
            # if enemy_spawn_timer checks removed

            for enemy in enemies:
                enemy.update()

                if player.rect.colliderect(enemy.rect):
                    if not enemy.has_hit_player:
                        if not player.invulnerable:
                            health_bar.hp -= enemy.damage
                            if hasattr(player, 'sounds') and 'damage' in player.sounds:
                                player.sounds['damage'].play()
                            enemy.has_hit_player = True
                            if enemy.hit_cooldown == 0:
                                player.velocity_y -= 30
                                player.momentum_x -= 30
                                enemy.hit_cooldown = 120

                else:
                    # reset zodra ze niet meer botsen
                    enemy.has_hit_player = False

            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                
                # Handle mute button click
                mute_button.handle_event(event)
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                        player.shoot_tongue()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Grapple key pressed
                    target_tile = player.find_nearest_grapple_tile()
                    if target_tile:
                        player.try_grapple(target_tile)

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause_menu = not pause_menu
                    if event.key == pg.K_h:
                        show_hitboxes = not show_hitboxes
                    
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                        
                    if event.key == pg.K_m:
                        mute_button.toggle()
                        
                    if event.key == pg.K_p:
                        print(f"Player Pos: {player.rect.topleft}, Level: {current_level_idx}")
                        player.print_current_loc()
                    
                    if event.key in (pg.K_UP, pg.K_w, pg.K_SPACE, pg.K_z):
                        player.request_jump()
                    
                    if event.key == pg.K_e:
                        player.shoot_tongue()
                    
                    if event.key == pg.K_g:  # Grapple key pressed
                        target_tile = player.find_nearest_grapple_tile()
                        if target_tile:
                            player.try_grapple(target_tile)

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_g:  # Grapple key released
                        player.grappling = False
                        player.grapple_target = None

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    player.grappling = False
                    player.grapple_target = None
                    

                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    world_pos = player.camera.to_world(event.pos)

                    # # Find the tile under the mouse
                    # for tile in lvl.tiles: # Use lvl here
                    #     if tile.rect.collidepoint(world_pos):
                    #         if tile.grappleable:
                    #             player.try_grapple(tile)
                    #         else:
                    #             break





                    # Held keys per frame
            keys = pg.key.get_pressed()
            player.update_input_Player(keys)

            # Horizontal input and facing
            if keys[pg.K_LEFT] or keys[pg.K_a] or keys[pg.K_q]:
                dx = -5
                player.facing_dir = -1    # <-- keep Player's facing up to date
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                dx = 5
                player.facing_dir = 1     # <-- keep Player's facing up to date
            else:
                dx = 0
            


            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            # Pass dummy rect for enemy collision (handled in loop above)
            player.update_physics(dx, keys, dt_factor, pg.Rect(0,0,0,0), health_bar)
                        # Check for level completion
            if player.level_complete:
                # Capture Time
                level_elapsed_time = time.time() - level_start_time
                # Submit Score
                # Assuming deaths is tracked in death_counter.count?
                # Actually death_counter tracks TOTAL deaths, or per level?
                # It has `reset_level_counter`.
                # We need deaths for THIS level attempt? Or cumulative?
                # User said "leaderboard of deaths and time per level".
                # Usually means "Failed attempts before success"?
                # Let's use death_counter.count - death_counter.previous_level_deaths_snapshot
                
                deaths_this_level = death_counter.count - death_counter.previous_level_deaths_snapshot
                
                deaths_this_level = death_counter.count - death_counter.previous_level_deaths_snapshot
                
                # Determine Player Name
                # If logged in, use part of email. If anonymous toggle is ON, use "Anonymous".
                # Wait, logic check: "Show Name: ON" means show it. OFF means Anonymous.
                
                # We need to access the toggle from menus.py. Imported `show_username`.
                # BUT `show_username` is a global in menus.py. Does `from menus import show_username` update?
                # No, standard python import copies the value. We need to access `menus.show_username`.
                # Let's adjust import to `import menus` or access via module if possible?
                # Actually, better: `import menus` is already done partially? No `from menus import ...`.
                # Let's import menus module fully to access dynamic global?
                # Or better, just fix the import above to `import menus` and change calls. 
                # OR let's look at how I imported it. `from menus import ...`.
                # If I change `from menus import ...` to include `show_username` it might be stale.
                # BETTER: Add a helper `menus.get_username_toggle()`?
                # Or just `import menus` on top and use `menus.show_username`.
                
                # Let's assume I fix the import in the first chunk to `import menus`.
                # Actually I'll just do `import menus` nicely.
                
                player_name = "Player"
                if network.user:
                     email = network.user.get('email', '')
                     if email:
                         player_name = email.split('@')[0] # Use part before @
                
                # Check Toggle (Accessing via re-import inside function or verify import)
                # I will use a fresh import inside the loop or change top level.
                # Let's change top level to `import menus` as well?
                # Or just access it via the property on the module if I imported module.
                # "from menus import ..." doesn't give module access.
                # I will change the logic below to use `menus.show_username` after adding `import menus`.
                
                # Check Toggle (Accessing via proper module import)
                if not menus.show_username:
                    player_name = "Anonymous"
                    
                print(f"Level Complete! Time: {level_elapsed_time:.2f}s, Deaths: {deaths_this_level}, Name: {player_name}")
                
                # ASYNC SUBMISSION
                def submit_task():
                    network.submit_score(current_level_idx + 1, level_elapsed_time, deaths_this_level, player_name=player_name)
                    # Update Cloud Progress
                    # Unlock next level logic:
                    # current_level_idx is 0-based. 
                    # If we beat lvl 0, we played lvl 1. Next is lvl 2.
                    # Max level reached = 2.
                    # We also update local max_level_reached to show star immediately!
                    network.update_user_progress(current_level_idx + 2, deaths_to_add=deaths_this_level)
                    network.update_user_progress(current_level_idx + 2, deaths_to_add=deaths_this_level)
                    print("[Async] Submission Complete")
                    
                    # TRIGGER TOTAL SCORE CALCULATION
                    # Pass the total number of levels to check.
                    # We are in a thread, so we can call another sync/async network function.
                    network.calculate_and_submit_total(len(level_module.LEVELS))

                threading.Thread(target=submit_task, daemon=True).start()
                
                # Update Local Progress for Stars
                # If we beat level 1 (idx 0), max_level becomes 2.
                if (current_level_idx + 2) > max_level_reached:
                    max_level_reached = current_level_idx + 2
                
                if (current_level_idx + 2) > max_level_reached:
                     max_level_reached = current_level_idx + 2
                
                # Check Highscore & Fetch Personal Best
                # Update LOCAL score (always, for offline tracking - NEVER sent to server)
                update_local_best(current_level_idx + 1, level_elapsed_time, deaths_this_level)
                
                # Fetch user's ONLINE best score for this level for display
                user_best_score = network.get_my_score(current_level_idx + 1)
                
                # Fallback to local best if no online score (offline or not logged in)
                if not user_best_score:
                    local_best = get_local_best(current_level_idx + 1)
                    if local_best:
                        user_best_score = local_best  # Use local best for display
                
                new_highscore = False 
                
                # Trigger Level Complete Menu INSTEAD of immediate next level
                level_complete_menu = True
                loading_menu = False
                
                # current_level_idx is NOT incremented yet.
                # It will be incremented when "Next Level" is clicked.



            if health_bar.hp <= 0:
                death_counter.count += 1
                player.reset(health_bar)
                # Restart timer on death (Speedrun Rules: Timer resets to 0 for new run)
                timer_started = False
                level_elapsed_time = 0
                pass

            # Update Camera
            player.camera.update(player)

           
            # Draw background first (apply camera offset to bg?)
            # For parallax or simple static BG?
            # If BG is LEVEL_WIDTH/HEIGHT, we should scroll it.
            # Background is scaled to LEVEL size.
            surface.fill((0,0,0)) # Clear
            # Create a background rect and shift it
            bg_rect = bg.get_rect()
            surface.blit(bg, player.camera.apply_rect(bg_rect))
            
            
            # Render Map
            player.render_map(surface, show_hitboxes)
            
            


            # Draw Spikes (already handled in render_map)
            # player.level.render_spikes(surface, player.camera) # If this exists? No, it's inside render_map  # Render tiles first
            # Render alle enemies
            for enemy in enemies:
                enemy.render(surface, camera)
                if show_hitboxes:
                    pg.draw.rect(surface, (255, 0, 0), camera.apply_rect(enemy.rect), 1)
            
            if player.hanging==True:

                if player.facing_dir == 1 :
                    player.render_chameleon_ceiling(surface, keys)

                elif player.facing_dir == -1:
                    player.render_chameleon_ceiling_left(surface, keys)

            elif player.on_wall == True:

                if player.wall_side > 0:
                    
                    if player.wall_facing_down:
                        player.render_chameleon_right_wall_down(surface, keys)
                    else:
                        player.render_chameleon_right_wall(surface, keys)
                
                else:
                    # Wall is to the LEFT.
                    if player.wall_facing_down:
                        player.render_chameleon_left_wall_down(surface, keys)
                    else:
                        player.render_chameleon_left_wall(surface, keys)
 
            else:
                if not player.hanging and player.facing_dir == 1 :
                    player.render_chameleon(surface, keys)
            

                elif not player.hanging and player.facing_dir == -1 :
                    player.render_chameleon_left(surface, keys)
            
            if show_hitboxes:
                pg.draw.rect(surface, (255, 0, 0), camera.apply_rect(player.rect), 1)
            
            if player.grappling and player.grapple_target:
                player_screen_pos = player.camera.apply_rect(player.rect).center
                target_screen_pos = player.camera.to_screen(player.grapple_target)
                pg.draw.line(surface, (240, 29, 29), player_screen_pos, target_screen_pos, 5)
            
            #show tongue
            player.update_tongue()
            player.render_tongue(surface)
            tongue_hitbox= player.get_tongue_hitbox()

            if lvl.has_enemy:
                if tongue_hitbox:
                    for enemy in enemies:
                        if tongue_hitbox.colliderect(enemy.rect):
                                
                                enemy.kill_enemy()
                                health_bar.hp += 10
        
            #healthbar creation
            health_bar.draw(surface)
            death_counter.draw(surface, current_level_idx + 1)
            # mute_button.draw(surface) # REMOVED from HUD
            # Draw hints
            if current_level_idx == 0:
                for hint in hints:
                    hint.draw(surface, camera)
            
            # Draw Timer (HUD)
            # Use module level variable accessed via imported name?
            # Or assume we imported 'show_timer' from menus.
            if menus.show_timer:
                 # elapsed is calculated every frame
                 # level_elapsed_time is updated at top of loop.
                 # Draw it Top Left
                 t_str = f"Time: {level_elapsed_time:.1f}s"
                 # Draw with shadow?
                 tsurf = font.render(t_str, True, "white")
                 tsurf_sh = font.render(t_str, True, "black")
                 # Position: topright aligned, y=45 (beneath Total Deaths at y=15)
                 t_rect = tsurf.get_rect(topright=(1260, 45))
                 t_rect_sh = tsurf_sh.get_rect(topright=(1262, 47)) # Shadow offset
                 surface.blit(tsurf_sh, t_rect_sh)
                 surface.blit(tsurf, t_rect)
                
            
            # Delta time
            dt_ms = clock.tick(60)
            if dt_ms > 100: dt_ms = 100 # Cap dt to prevent physics explosions/teleporting
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

if __name__ == "__main__":
    main()
    pg.quit()
