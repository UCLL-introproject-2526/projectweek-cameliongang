
import pygame as pg
from level import Level

# Function to create and return the main game surface (window)
def create_main_surface():
    screen_size = pg.display.set_mode((1700, 900))
    return screen_size


# Function to clear the surface by filling it with black
def clear_surface(surface):
    surface.fill((0, 0, 0))

# Class to manage the game state, including position and rendering
class state:
    def __init__(self):
        self.velocity_y = 0
        self.gravity = 0.675
        self.jump_strength = -15
        self.jump_cut = -4
        self.width = 50 # Approx player width
        self.height = 50 # Approx player height
        self.on_ground = False
        self.on_wall = False
        
        # Load Level
        self.level = Level()
        self.xcoor, self.ycoor = self.level.player_start_pos
        self.tiles = self.level.tiles

    def jump(self):
        if self.on_ground or self.on_wall:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.on_wall = False

    def update_physics(self, dx):
        self.on_ground = False
        self.on_wall = False
        
        # Horizontal Movement
        self.xcoor += dx
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        #jump movement

        keys = pg.key.get_pressed()

        if self.velocity_y < 0 and not keys[pg.K_UP]:
            self.velocity_y = max(self.velocity_y, self.jump_cut)
        
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if getattr(tile, 'type', 'X') == 'S':
                    self.on_wall = True
                    self.velocity_y = 0 # Stick to wall
                    
                    # Simple Climb: If invalid move, push out, but allow climbing?
                    # "zijwaarts op kan klimmen" (climb sideways up it?)
                    # For now, let's just stick. Movement up/down needs vertical input.
                
                if dx > 0: # Moving Right
                    self.xcoor = tile.rect.left - self.width
                if dx < 0: # Moving Left
                    self.xcoor = tile.rect.right
        
        # Vertical Movement
        if self.on_wall:
            # If on wall, we can move up/down with keys potentially, or just hold validation
            # For now, let's disable gravity if on wall
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.ycoor -= 5
            elif keys[pg.K_DOWN]:
                self.ycoor += 5
        else:
            self.velocity_y += self.gravity
            self.ycoor += self.velocity_y
            
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)
        
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if getattr(tile, 'type', 'X') == 'S':
                     # Ceiling Stick (moving up)
                     if self.velocity_y < 0:
                         self.ycoor = tile.rect.bottom
                         self.velocity_y = 0
                         self.on_wall = True # Re-use on_wall to disable gravity
                
                if self.velocity_y > 0: # Falling
                    self.ycoor = tile.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0: # Jumping Up (Standard Block)
                    if getattr(tile, 'type', 'X') != 'S':
                        self.ycoor = tile.rect.bottom
                        self.velocity_y = 0

    def render_map(self, surface):
        self.level.render(surface)

    def render_camelion(self, surface):
        
        try:
            camelion_img = pg.image.load('./resources/camelion.png').convert()
            camelion_img.set_colorkey((0, 0, 0))
            # Resize to match collision box roughly
            camelion_img = pg.transform.scale(camelion_img, (self.width, self.height))
            surface.blit(camelion_img, (self.xcoor, self.ycoor))
        except:
             pg.draw.rect(surface, (255, 0, 0), (self.xcoor, self.ycoor, self.width, self.height))

    def render_camelion_left(self,surface):
        try:
            camelion_img = pg.image.load('./resources/camelion_facing_left.png').convert()
            camelion_img.set_colorkey((0, 0, 0))
            # Resize to match collision box roughly
            camelion_img = pg.transform.scale(camelion_img, (self.width, self.height))
            surface.blit(camelion_img, (self.xcoor, self.ycoor))
        except:
             pg.draw.rect(surface, (255, 0, 0), (self.xcoor, self.ycoor, self.width, self.height))
    def render_bush(self, surface):
        try:
            bush_img = pg.image.load('./resources/bush.png').convert()
            bush_img.set_colorkey((0, 0, 0))
            bush_img = pg.transform.scale(bush_img,
                                    (bush_img.get_width() / 1.5,
                                     bush_img.get_height() / 1.5))
            surface.blit(bush_img, (800, 450))
        except:
            pg.draw.rect(surface, (0, 255, 0), (800, 450, 50, 50))

class keyboard:
    def __init__(self):
        pass


# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    status = state()
    running = True
    
    #music
    try:
        sound = pg.mixer.music.load('.\\resources\\themesong.mp3')
        pg.mixer.music.play(-1)
    except:
        pass
    #######################

    # Load background image
    try:
        background = pg.image.load(".\\resources\\background_img.jpg").convert()
        background = pg.transform.scale(background, (1700, 900))
    except:
        background = pg.Surface((1700, 900))
        background.fill((100, 100, 255))

    # Main game loop
    facing_left=False
    facing_right=True
    while running:
        # Draw background first
        surface.blit(background, (0, 0))

        # Input Handling
        dx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            dx = -5
            status.render_camelion_left(surface)
            facing_left = True
            facing_right = False

        if keys[pg.K_RIGHT]:
             dx = 5
             status.render_camelion
             facing_right = True
             facing_left = False
        # Note: Jump input handled in event loop now for cleaner tap response

        # Update Physics
        status.update_physics(dx)

        # Render
        status.render_map(surface) # Render tiles first
        status.render_bush(surface)
        if facing_right==True:
            status.render_camelion(surface)
        else:
            status.render_camelion_left(surface)
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    status.jump()
    

        # Delta time
        clock.tick(60)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()