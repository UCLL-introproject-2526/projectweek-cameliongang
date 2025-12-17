import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT
from camera import Camera
from menus import draw_mainmenu, draw_death_menu, draw_levels_menu, draw_loading_screen
from player import Player
from standard_use import play_music, game_background, HealthBar, create_main_surface


# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    player = Player()
    running = True
    running = True
    main_menu = True
    loading_menu = False
    loading_timer = 0
    LOADING_DURATION = 120 # 2 seconds at 60 FPS
    death_menu = False
    font = pg.font.Font('.\\resources\\ARIAL.TTF', 24)
    health_bar = HealthBar(20, 20, 300, 40, 100)

    #music playing
    play_music()

    #background
    background = game_background('background_img.jpg')

    # Main game loop
    facing_left = False
    facing_right = True
    
    # Delta time initialization
    dt_factor = 1.0

    while running:
        dx = 0
        if main_menu:
             command = draw_mainmenu(surface, font)
             if command == 1:
                running = False
             if command == 3:
                 pass
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
             # Calculate progress (0.0 to 1.0)
             progress = min(1.0, loading_timer / LOADING_DURATION)
             draw_loading_screen(surface, font, progress)
             
             loading_timer += 1
             if loading_timer >= LOADING_DURATION:
                 loading_menu = False
                 # Game starts now - Initialize Player here to cover the load time
                 player = Player()
             
             pg.display.flip()
             clock.tick(60)
             # Consume events to prevent queue buildup
             pg.event.pump()
             continue
        elif death_menu:
             command = draw_death_menu(surface, font)
             if command == 1: # Restart
                 death_menu = False
                 loading_menu = True
                 loading_timer = 0
                 # Reset background if needed? No, standard reuse.
                 # Re-fetch background cause player changed?
                 # background func uses player camera...
                 # But background itself is just an image. The blit happens in loop.
             if command == 2: # Quit
                 running = False
             
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             
             pg.display.flip()
             clock.tick(60)
             continue
        else:
            # Handle events FIRST — buffer jump here
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        player.request_jump()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    world_pos = player.camera.to_world(event.pos)
                    player.grapple_target = world_pos
                    player.grappling = True


                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    player.grappling = False  # stop pulling, keep momentum



            # Held keys per frame   
            keys = pg.key.get_pressed()
            player.update_input_Player(keys)

            # Input Handling for horizontal movement and facing
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                dx = -5
                facing_left = True
                facing_right = False
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                dx = 5
                facing_right = True
                facing_left = False
            


            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            player.update_physics(dx, keys, dt_factor)

            # Check for death
            if player.is_dead:
                death_menu = True

            # Update Camera
            player.camera.update(player)

           
            # Draw background first (apply camera offset to bg?)
            # For parallax or simple static BG?
            # If BG is LEVEL_WIDTH/HEIGHT, we should scroll it.
            # Background is scaled to LEVEL size.
            surface.fill((0,0,0)) # Clear
            # Create a background rect and shift it
            bg_rect = background.get_rect()
            surface.blit(background, player.camera.apply_rect(bg_rect))

            # Render
            player.render_map(surface)  # Render tiles first
            if player.hanging==True:

                if facing_right:
                    player.render_camelion_ceiling(surface)

                elif facing_left:
                    player.render_camelion_ceiling_left(surface)

            elif player.on_wall == True:

                if player.wall_side > 0:
                    # Wall is to the RIGHT.
                    if player.wall_facing_down:
                        player.render_camelion_right_wall_down(surface)
                    else:
                        player.render_camelion_right_wall(surface)
                
                else:
                    # Wall is to the LEFT.
                    if player.wall_facing_down:
                        player.render_camelion_left_wall_down(surface)
                    else:
                        player.render_camelion_left_wall(surface)

            else:
                if not player.hanging and facing_right:
                    player.render_camelion(surface)
            

                elif not player.hanging and facing_left:
                    player.render_camelion_left(surface)
            
            if player.grappling and player.grapple_target:
                player_screen_pos = player.camera.apply_rect(player.rect).center
                target_screen_pos = player.camera.to_screen(player.grapple_target)
                pg.draw.line(surface, (200,200,200), player_screen_pos, target_screen_pos, 2)
                
                

            #healthbar creation
            health_bar.draw(surface)
            # Delta time
            dt_ms = clock.tick(60)
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

pg.quit()

if __name__ == "__main__":
    main()