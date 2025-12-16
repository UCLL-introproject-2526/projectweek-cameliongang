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
        self.wall_side = 0 # 1 for right, -1 for left
        self.hanging = False # New state for ceiling stick

        # Momentum
        self.momentum_x = 0

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
    def try_consume_jump(self, keys):
        if (self.on_ground or self.coyote_timer > 0 or self.on_wall or self.hanging) and self.jump_buffer > 0:
            
            # Wall Jump Logic: Only fire if holding AWAY from wall
            if self.on_wall:
                kick_strength = 10
                did_wall_jump = False
                
                if self.wall_side == 1: # Wall on right
                    if keys[pg.K_LEFT]: # Must hold LEFT to jump off right wall
                        self.momentum_x = -kick_strength
                        did_wall_jump = True
                elif self.wall_side == -1: # Wall on left
                     if keys[pg.K_RIGHT]: # Must hold RIGHT to jump off left wall
                        self.momentum_x = kick_strength
                        did_wall_jump = True
                
                if not did_wall_jump:
                    return # Do not consume jump if direction is wrong (allow climbing/holding)

            # Execute Jump
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.on_wall = False
            self.wall_side = 0
            self.hanging = False
            self.coyote_timer = 0
            self.jump_buffer = 0
            self.started_rise = False  # reset gating for a new jump

    # Track held key state per frame
    def update_input_state(self, keys):
        self.jump_held = keys[pg.K_UP]

    def update_physics(self, dx, keys):
        # Validate existing wall stick (Persistent State)
        if self.on_wall:
            # Check for pull-off (Moving away from wall)
            # Only pull off if we ARE NOT trying to jump (buffered jump preserves wall state for the kick)
            if ((dx < 0 and self.wall_side == 1) or (dx > 0 and self.wall_side == -1)) and self.jump_buffer == 0:
                self.on_wall = False
                self.wall_side = 0
            else:
                # Check for physical connection (Sensor)
                sensor_x = self.xcoor + self.width if self.wall_side == 1 else self.xcoor - 2
                sensor = pg.Rect(sensor_x, self.ycoor + 5, 2, self.height - 10) # slightly smaller to avoid corner issues
                touching = False
                for tile in self.tiles:
                     if getattr(tile, 'type', 'X') == 'S' and tile.rect.colliderect(sensor):
                         touching = True
                         break
                if not touching:
                    self.on_wall = False
                    self.wall_side = 0

        self.on_ground = False
        # Do not rely on side collision to set on_wall every frame if we want persistence,
        # BUT new collisions must set it.

        # Apply Momentum
        total_dx = dx + self.momentum_x
        # Decay momentum (air resistance / friction)
        self.momentum_x *= 0.9
        if abs(self.momentum_x) < 0.5:
             self.momentum_x = 0

        # Horizontal Movement
        self.xcoor += total_dx
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Horizontal collision
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if getattr(tile, 'type', 'X') == 'S':
                    self.on_wall = True
                    self.wall_side = 1 if total_dx > 0 else -1
                    self.velocity_y = 0  # Stick to wall
                    self.hanging = False # Wall/Side overrides hanging?
                    self.momentum_x = 0 # Stop momentum on hit

                if total_dx > 0:  # Moving Right
                    self.xcoor = tile.rect.left - self.width
                    self.momentum_x = 0 # crash stop
                if total_dx < 0:  # Moving Left
                    self.xcoor = tile.rect.right
                    self.momentum_x = 0 # crash stop

        # Vertical Movement Calculation
        dy = 0
        
        # Check if hanging is still valid (must be touching 'S' above)
        if self.hanging:
            # Create a sensor rect slightly above
            sensor = pg.Rect(self.xcoor, self.ycoor - 1, self.width, 1)
            still_touching = False
            for tile in self.tiles:
                if getattr(tile, 'type', 'X') == 'S' and tile.rect.colliderect(sensor):
                    still_touching = True
                    break
            if not still_touching:
                self.hanging = False
        
        if self.on_wall:
            # Wall Climb
            if keys[pg.K_UP]:
                dy = -5
            elif keys[pg.K_DOWN]:
                dy = 5
        elif self.hanging:
            # Ceiling Stick
            if keys[pg.K_DOWN]:
                self.hanging = False # Drop
                dy = 5
            # UP does nothing while hanging? Or maybe clamber?
        else:
            # Gravity
            self.velocity_y += self.gravity
            dy = self.velocity_y

            # Mark when upward motion begins (for jump-cut gating)
            if self.velocity_y < 0:
                self.started_rise = True
    
            # Jump cut
            if self.started_rise and not self.jump_held and self.velocity_y < 0:
                self.velocity_y = max(self.velocity_y, self.jump_cut)
                dy = self.velocity_y

        # Apply Vertical Move
        self.ycoor += dy
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Vertical collision
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                if dy < 0: # Moving Up
                     if getattr(tile, 'type', 'X') == 'S':
                         # Ceiling stick
                         self.ycoor = tile.rect.bottom
                         self.velocity_y = 0
                         self.hanging = True
                     else:
                         self.ycoor = tile.rect.bottom
                         self.velocity_y = 0
                elif dy > 0: # Falling / Moving Down
                    self.ycoor = tile.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.momentum_x = 0 # Friction on ground? Maybe not instantly, but let's reset for control consistency
        
        # Update coyote after collision resolution
        self.update_coyote()

        # Consume buffered jump now that collision is resolved
        self.try_consume_jump(keys)

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