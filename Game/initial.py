import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT
from camera import Camera
from menus import draw_menu
from player import Player
from standard_use import play_music, game_background, HealthBar

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Function to create and return the main game surface (window)
def create_main_surface():
    screen_size = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Camelion Run!')
    return screen_size

def render_bush(self, surface):
    try:
        bush_img = pg.image.load('./resources/bush.png').convert()
        bush_img.set_colorkey((0, 0, 0))
        bush_img = pg.transform.scale(
            bush_img,
            (int(bush_img.get_width() / 1.5), int(bush_img.get_height() / 1.5))
        )
        # Hardcoded bush pos for now: (800, 450)
        bush_rect = bush_img.get_rect(topleft=(800,450))
        surface.blit(bush_img, self.camera.apply_rect(bush_rect))
    except:
        bush_rect = pg.Rect(800, 450, 50, 50)
        pg.draw.rect(surface, (0, 255, 0), self.camera.apply_rect(bush_rect))

    

# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    player = Player()
    running = True
    main_menu = True
    font = pg.font.Font('.\\resources\\ARIAL.TTF', 24)
    health_bar = HealthBar(20, 20, 300, 40, 100)

    #music playing
    play_music()

    # Main game loop
    facing_left = False
    facing_right = True
    
    # Delta time initialization
    dt_factor = 1.0

    # Load background image
    try:
        background = pg.image.load(".\\resources\\background_img.jpg").convert()
        background = pg.transform.scale(background, (LEVEL_WIDTH, LEVEL_HEIGHT))
    except:
        background = pg.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        background.fill((100, 100, 255))

    while running:
        dx = 0
        if main_menu:
             buttons = draw_menu(surface, font)
             if buttons == 1:
                running = False
             if buttons == 4:
                main_menu = False
             for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
             pg.display.flip()
             # Still tick clock to keep menu framing consistent, but we don't need dt for menu logic yet
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
                    Player.grapple_target = event.pos
                    #Player.grappling_hook()

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
                
                
                

            #healthbar creation
            health_bar.draw(surface)
            # Delta time
            dt_ms = clock.tick(60)
            dt_factor = (dt_ms / 1000.0) * 60
            pg.display.flip()

pg.quit()

if __name__ == "__main__":
    main()