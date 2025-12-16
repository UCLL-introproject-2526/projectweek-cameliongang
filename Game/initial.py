
import pygame as pg
from level import LEVEL_MAP

TILE_SIZE = 64

# Function to create and return the main game surface (window)
def create_main_surface():
    screen_size = pg.display.set_mode((1700, 900))
    return screen_size


# Function to clear the surface by filling it with black
def clear_surface(surface):
    surface.fill((0, 0, 0))

class Tile(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((139, 69, 19)) # Brown
        pg.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        self.rect = self.image.get_rect(topleft=pos)

# Class to manage the game state, including position and rendering
class state:
    def __init__(self):
        self.xcoor = 100
        self.ycoor = 100
        self.velocity_y = 0
        self.gravity = 0.675
        self.jump_strength = -15
        self.width = 40 # Approx player width
        self.height = 40 # Approx player height
        
        # Load Level
        self.tiles = []
        self.load_level()

    def jump(self):
        if self.velocity_y == 0:
            self.velocity_y = self.jump_strength

    def load_level(self):
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    self.tiles.append(Tile((x, y)))
                if cell == 'P':
                    self.xcoor = x
                    self.ycoor = y

    def update_physics(self, dx):
        # Horizontal Movement
        self.xcoor += dx
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)
        
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if dx > 0: # Moving Right
                    self.xcoor = tile.rect.left - self.width
                if dx < 0: # Moving Left
                    self.xcoor = tile.rect.right
        
        # Vertical Movement (Gravity)
        self.velocity_y += self.gravity
        self.ycoor += self.velocity_y
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)
        
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if self.velocity_y > 0: # Falling
                    self.ycoor = tile.rect.top - self.height
                    self.velocity_y = 0
                elif self.velocity_y < 0: # Jumping Up
                    self.ycoor = tile.rect.bottom
                    self.velocity_y = 0

    def render_map(self, surface):
        for tile in self.tiles:
            surface.blit(tile.image, tile.rect)

    def render_camelion(self, surface):
        try:
            camelion_img = pg.image.load('./resources/camelion.png').convert()
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
    sound = pg.mixer.music.load('.\\resources\\themesong.mp3')
    pg.mixer.music.play(-1)
    #######################

    # Load background image
    try:
        background = pg.image.load(".\\resources\\background_img.jpg").convert()
        background = pg.transform.scale(background, (1700, 900))
    except:
        background = pg.Surface((1700, 900))
        background.fill((100, 100, 255))

    # Main game loop
    while running:
        # Draw background first
        surface.blit(background, (0, 0))

        # Input Handling
        dx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            dx = -5
        if keys[pg.K_RIGHT]:
             dx = 5
        if keys[pg.K_UP]:
             status.jump()

        # Update Physics
        status.update_physics(dx)

        # Render
        status.render_map(surface) # Render tiles first
        status.render_bush(surface)
        status.render_camelion(surface)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Delta time
        clock.tick(60)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()