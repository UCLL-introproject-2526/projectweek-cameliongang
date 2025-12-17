import pygame as pg
import random
from player import Player
from camera import Camera
import level as level_module
from level import Level # Keep Level class import for convenience
from menus import draw_mainmenu, draw_levels_menu, draw_pause_menu, draw_loading_screen
from standard_use import SCREEN_WIDTH, SCREEN_HEIGHT, HealthBar, DeathCounter, game_background, play_music, create_main_surface
from enemy import Enemy
from level import LEVEL_WIDTH, LEVEL_HEIGHT

# create_main_surface imported from standard_use

# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    
    current_level_idx = 0
    lvl = Level(current_level_idx)
    camera = Camera(level_module.LEVEL_WIDTH, level_module.LEVEL_HEIGHT)
    player = Player(lvl, camera) # Player now takes level and camera
    # Initialize enemy at a safe spot, e.g., 800, 400 or somewhere valid
    enemies = []
    enemycount = 3 
    spawn_interval= 180  # enkel in factoren van 60 veranderen.
    enemy_spawn_timer = 0
    y_enemy = random.randint(1,LEVEL_HEIGHT - 50)
    enemy = Enemy(800, y_enemy) 
    running = True
    running = True
    levels_menu = False
    main_menu = True
    loading_menu = False
    loading_timer = 0
    LOADING_DURATION = 120 # 2 seconds at 60 FPS
    death_menu = False
    pause_menu = False
    font = pg.font.Font('.\\resources\\ARIAL.TTF', 24)
    health_bar = HealthBar(20, 20, 300, 40, 100)
    death_counter = DeathCounter(font)

    #music playing
    play_music()

    #background
    # Draw Game
    bg = game_background('background_img.jpg', width=level_module.LEVEL_WIDTH, height=level_module.LEVEL_HEIGHT)
    surface.blit(bg, (0, 0)) # Parallax/Static?
    facing_left = False
    facing_right = True
    
    # Delta time initialization
    dt_factor = 1.0

    while running:
        dx = 0
        if main_menu:
             command = draw_mainmenu(surface, font)
             if command == 'q':
                 # Quit the game
                 running = False
             if command == 3:
                 levels_menu = True
                 main_menu =False
             if command == 4:
                main_menu = False
                loading_menu = True
                loading_timer = 0
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             pg.display.flip()
             # Still tick clock to keep menu framing consistent, but we don't need dt for menu logic yet
             clock.tick(60)
             continue
        elif loading_menu:
             # Draw Loading Screen
             loading_timer += 1
             
             # Perform heavy loading on the first few frames to ensure UI has rendered at least once
             if loading_timer == 5: # Small delay to let "Loading..." appear
                 # Re-init level
                 lvl = Level(current_level_idx)
                 # Re-init camera with new dimensions
                 camera = Camera(level_module.LEVEL_WIDTH, level_module.LEVEL_HEIGHT)
                 
                 # Reload background to match new level size
                 bg = game_background('background_img.jpg', width=level_module.LEVEL_WIDTH, height=level_module.LEVEL_HEIGHT)
                 
             progress = loading_timer / LOADING_DURATION
             draw_loading_screen(surface, font, progress, current_level_idx)
             
             if loading_timer >= LOADING_DURATION:
                 loading_menu = False
                 # Game starts now - Initialize Player here to cover the load time
                 # Ensure lvl/camera are ready (they should be from timer==5)
                 player = Player(lvl, camera)
                 # Reset enemies bij herstart (nieuw: lege lijst)
                 enemies = []
                 enemy_spawn_timer = 0  # Reset timer
             
             pg.display.flip()
             clock.tick(60)
             # Consume events to prevent queue buildup
             pg.event.pump()
             continue
        elif pause_menu:
             command = draw_pause_menu(surface, font)
             if command == 1: # Resume
                 pause_menu = False
             if command == 2: # Quit
                 running = False
             if command == 3: # Main Menu
                 pause_menu = False
                 main_menu = True
             if command == 4: # Level Select
                 pause_menu = False
                 levels_menu = True
             if command == 5: # Restart
                 player.reset()
                 pause_menu = False
             
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             
             pg.display.flip()
             clock.tick(60)
             continue
        elif levels_menu:
             command = draw_levels_menu(surface, font)
             if command >= 10: # Level selected
                 current_level_idx = command - 10
                 # Start Loading immediately, defer logic to loading_menu loop
                 levels_menu = False
                 loading_menu = True
                 loading_timer = 0
             
             elif command == 2: # Back
                 levels_menu = False
                 main_menu = True
                 
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             
             pg.display.flip()
             clock.tick(60)
             continue
        else:
            # Handling events
            
            
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= spawn_interval and len(enemies) < enemycount:
                
                y_enemy = random.randint(100, 500)
                enemies.append(Enemy(LEVEL_WIDTH, y_enemy))  
                enemy_spawn_timer = 0  
            
            
            for enemy in enemies:
                enemy.update()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause_menu = not pause_menu
                    
                    if event.key in (pg.K_UP, pg.K_w):
                        player.request_jump()

                    elif event.key == pg.K_g:  # Grapple key pressed
                        target_tile = player.find_nearest_grapple_tile()
                        if target_tile:
                            player.try_grapple(target_tile)

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_g:  # Grapple key released
                        player.grappling = False
                        player.grapple_target = None

                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    world_pos = player.camera.to_world(event.pos)

                    # Find the tile under the mouse
                    for tile in lvl.tiles: # Use lvl here
                        if tile.rect.collidepoint(world_pos):
                            if tile.grappleable:
                                player.try_grapple(tile)
                            else:
                                print("Can't grapple this tile!")
                            break


                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    player.grappling = False




                    # Held keys per frame
            keys = pg.key.get_pressed()
            player.update_input_Player(keys)

            # Horizontal input and facing
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                dx = -5
                player.facing_dir = -1    # <-- keep Player's facing up to date
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                dx = 5
                player.facing_dir = 1     # <-- keep Player's facing up to date
            else:
                dx = 0
            


            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            player.update_physics(dx, keys, dt_factor)
                        # Check for level completion
            if player.level_complete:
                current_level_idx += 1
                if current_level_idx >= len(level_module.LEVELS):
                    # All levels completed! Back to main menu or victory screen
                    current_level_idx = 0  # Loop back, or set main_menu = True
                    main_menu = True
                else:
                    # Load next level
                    loading_menu = True
                    loading_timer = 0




            # Check for death
            if player.is_dead:
                death_counter.count += 1
                player.reset()

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
            
            
            # Render
            player.render_map(surface)  # Render tiles first
            # Render alle enemies
            for enemy in enemies:
                enemy.render(surface, camera)
            
            if player.hanging==True:

                if player.facing_dir == 1 :
                    player.render_chameleon_ceiling(surface)

                elif player.facing_dir == -1:
                    player.render_chameleon_ceiling_left(surface)

            elif player.on_wall == True:

                if player.wall_side > 0:
                    # Wall is to the RIGHT.
                    if player.wall_facing_down:
                        player.render_chameleon_right_wall_down(surface)
                    else:
                        player.render_chameleon_right_wall(surface)
                
                else:
                    # Wall is to the LEFT.
                    if player.wall_facing_down:
                        player.render_chameleon_left_wall_down(surface)
                    else:
                        player.render_chameleon_left_wall(surface)

            else:
                if not player.hanging and player.facing_dir == 1 :
                    player.render_chameleon(surface)
            

                elif not player.hanging and player.facing_dir == -1 :
                    player.render_chameleon_left(surface)
            
            if player.grappling and player.grapple_target:
                player_screen_pos = player.camera.apply_rect(player.rect).center
                target_screen_pos = player.camera.to_screen(player.grapple_target)
                pg.draw.line(surface, (240, 29, 29), player_screen_pos, target_screen_pos, 5)
                
                

            #healthbar creation
            health_bar.draw(surface)
            death_counter.draw(surface)
            # Delta time
            dt_ms = clock.tick(60)
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

pg.quit()

if __name__ == "__main__":
    main()