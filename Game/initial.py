import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT

# Function to create and return the main game surface (window)
def create_main_surface():
    screen_size = pg.display.set_mode((LEVEL_WIDTH, LEVEL_HEIGHT))
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
        self.width = 50  # Approx player width
        self.height = 50  # Approx player height
        self.on_ground = False
        self.on_wall = False

        # Load Level
        self.level = Level()
        self.xcoor, self.ycoor = self.level.player_start_pos
        self.tiles = self.level.tiles

        # Coyote time
        self.coyote_timer = 0
        self.coyote_time = 6

        # Jump buffer (frames to remember jump input)
        self.jump_buffer = 0
        self.jump_buffer_time = 6

        # Gated jump-cut
        self.jump_held = False
        self.started_rise = False

    def update_coyote(self):
        if self.on_ground:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(0, self.coyote_timer - 1)

    # Buffer jump intent instead of jumping immediately
    def request_jump(self):
        self.jump_buffer = self.jump_buffer_time

    # Consume buffered jump after collision resolution
    def try_consume_jump(self):
        if (self.on_ground or self.coyote_timer > 0 or self.on_wall) and self.jump_buffer > 0:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.on_wall = False
            self.coyote_timer = 0
            self.jump_buffer = 0
            self.started_rise = False  # reset gating for a new jump

    # Track held key state per frame
    def update_input_state(self, keys):
        self.jump_held = keys[pg.K_UP]

    def update_physics(self, dx, keys):
        # Reset contact flags for this frame
        self.on_ground = False
        self.on_wall = False

        # Horizontal Movement
        self.xcoor += dx
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Horizontal collision
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if getattr(tile, 'type', 'X') == 'S':
                    self.on_wall = True
                    self.velocity_y = 0  # Stick to wall

                if dx > 0:  # Moving Right
                    self.xcoor = tile.rect.left - self.width
                if dx < 0:  # Moving Left
                    self.xcoor = tile.rect.right

        # Vertical Movement
        if self.on_wall:
            # Simple wall behavior: disable gravity, allow climbing with keys
            if keys[pg.K_UP]:
                self.ycoor -= 5
            elif keys[pg.K_DOWN]:
                self.ycoor += 5
        else:
            # Gravity
            self.velocity_y += self.gravity
            self.ycoor += self.velocity_y

        # Mark when upward motion begins (for jump-cut gating)
        if self.velocity_y < 0:
            self.started_rise = True

        # Jump cut only if rising AND UP released after rise started
        if self.started_rise and not self.jump_held and self.velocity_y < 0:
            self.velocity_y = max(self.velocity_y, self.jump_cut)

        # Recompute rect after vertical move
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Vertical collision
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if getattr(tile, 'type', 'X') == 'S':
                    # Ceiling stick (moving up)
                    if self.velocity_y < 0:
                        self.ycoor = tile.rect.bottom
                        self.velocity_y = 0
                        self.on_wall = True  # reuse to disable gravity
                if self.velocity_y > 0:  # Falling
                    self.ycoor = tile.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping up (standard block)
                    if getattr(tile, 'type', 'X') != 'S':
                        self.ycoor = tile.rect.bottom
                        self.velocity_y = 0

        # Update coyote after collision resolution
        self.update_coyote()

        # Consume buffered jump now that collision is resolved
        self.try_consume_jump()

        # Decay jump buffer
        if self.jump_buffer > 0:
            self.jump_buffer -= 1

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

    def render_camelion_left(self, surface):
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
            bush_img = pg.transform.scale(
                bush_img,
                (int(bush_img.get_width() / 1.5), int(bush_img.get_height() / 1.5))
            )
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

    # music
    try:
        pg.mixer.music.load('.\\resources\\themesong.mp3')
        pg.mixer.music.play(-1)
    except:
        pass
    #######################

    # Load background image
    try:
        background = pg.image.load(".\\resources\\background_img.jpg").convert()
        background = pg.transform.scale(background, (LEVEL_WIDTH, LEVEL_HEIGHT))
    except:
        background = pg.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
        background.fill((100, 100, 255))

    # Main game loop
    facing_left = False
    facing_right = True
    while running:
        dx = 0

        # Handle events FIRST — buffer jump here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    status.request_jump()

        # Held keys per frame
        keys = pg.key.get_pressed()
        status.update_input_state(keys)

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
        status.update_physics(dx, keys)

        # Draw background first
        surface.blit(background, (0, 0))

        # Render
        status.render_map(surface)  # Render tiles first
        status.render_bush(surface)
        if facing_right:
            status.render_camelion(surface)
        else:
            status.render_camelion_left(surface)

        # Delta time
        clock.tick(60)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()