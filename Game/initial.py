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
    # Initialize enemies from level
    enemies = [Enemy(pos[0], pos[1]) for pos in lvl.enemy_spawns]
    
    # Debug
    show_hitboxes = False

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
    shoot=False
    

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
                 enemies = [Enemy(pos[0], pos[1]) for pos in lvl.enemy_spawns]
             
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
                 player.reset(health_bar)
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
            
            # Enemy spawning from level (static) - No longer random spawning
            # if enemy_spawn_timer checks removed

            for enemy in enemies:
                enemy.update()

                if player.rect.colliderect(enemy.rect):
                    if not enemy.has_hit_player:
                        health_bar.hp -= enemy.damage
                        enemy.has_hit_player = True
                else:
                    # reset zodra ze niet meer botsen
                    enemy.has_hit_player = False

            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause_menu = not pause_menu
                    if event.key == pg.K_h:
                        show_hitboxes = not show_hitboxes
                    
                    if event.key in (pg.K_UP, pg.K_w):
                        player.request_jump()
                    
                    if event.key == pg.K_e:
                        player.shoot_tongue()

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
            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            # Pass dummy rect for enemy collision (handled in loop above)
            player.update_physics(dx, keys, dt_factor, pg.Rect(0,0,0,0), health_bar)
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



            if health_bar.hp <= 0:
                death_counter.count += 1
                player.reset(health_bar)

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
                    player.render_chameleon_ceiling(surface)

                elif player.facing_dir == -1:
                    player.render_chameleon_ceiling_left(surface)

            elif player.on_wall == True:

                if player.wall_side > 0:
                    
                    if player.wall_facing_down:
                        player.render_chameleon_right_wall_down(surface)
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
            death_counter.draw(surface)
            # Delta time
            dt_ms = clock.tick(60)
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

pg.quit()

if __name__== "__main__":
    main()
