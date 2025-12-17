import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT
from camera import Camera
from menus import draw_menu, draw_death_menu
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
    main_menu = True
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
             if command == 4:
                main_menu = False
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             pg.display.flip()
             # Still tick clock to keep menu framing consistent, but we don't need dt for menu logic yet
             clock.tick(60)
             continue
        elif death_menu:
             command = draw_death_menu(surface, font)
             if command == 1: # Restart
                 player = Player()
                 death_menu = False
                 # Reset background if needed? No, standard reuse.
                 # Re-fetch background cause player changed?
                 # background func uses player camera...
                 # But background itself is just an image. The blit happens in loop.
             if command == 2: # Quit
                 running = False
             
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             # Draw the death menu (it draws overlay + buttons)
             # But we want the game visible behind it?
             # draw_death_menu does overlay.
             # We should probably NOT clear screen if we want overlay over game.
             # But the loop clears screen in 'else' block.
             # To keep game visible, we need to RENDER game then RENDER menu.
             # So 'death_menu' logic should probably be AFTER game render?
             # OR we just accept a black background or whatever was last frame.
             # If we want transparent overlay over the game scene:
             # We need to render the game SCENE, then menu.
             # But we want to STOP physics.
             
             pg.display.flip()
             clock.tick(60)
             continue
        else:
            # Handle events FIRST — buffer jump here
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        player.request_jump()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    player.grapple_target = event.pos
                    
                    print(player.grapple_target)

            # Held keys per frame   
            keys = pg.key.get_pressed()
            player.update_input_Player(keys)

            # Input Handling for horizontal movement and facing
            if keys[pg.K_LEFT]:
                dx = -5
                facing_left = True
                facing_right = False
            elif keys[pg.K_RIGHT]:
                dx = 5
                facing_right = True
                facing_left = False

            player.grappling_hook()

            # Update Physics (now takes keys for wall behavior and jump-cut gating)
            player.update_physics(dx, keys, dt_factor)

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
                    # Wall is to the RIGHT. We want to face RIGHT.
                    player.render_camelion_right_wall(surface)
                
                else:
                    # Wall is to the LEFT. We want to face LEFT.
                    player.render_camelion_left_wall(surface)

            else:
                if not player.hanging and facing_right:
                    player.render_camelion(surface)
            

                elif not player.hanging and facing_left:
                    player.render_camelion_left(surface)
            
            if player.grapple_target:
                pg.draw.line(surface, (200,200,200), player.rect.center, player.grapple_target, 2)
                
                

            #healthbar creation
            health_bar.draw(surface)
            # Delta time
            dt_ms = clock.tick(60)
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

pg.quit()

if __name__ == "__main__":
    main()