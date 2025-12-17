import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT, TILE_SIZE
from camera import Camera
import math
from standard_use import HealthBar

# Class to manage the game Player, including position and rendering
class Player:
    def __init__(self, level, camera):
        self.velocity_y = 0
        self.gravity = 0.675
        self.jump_strength = -15
        self.jump_cut = -4
        self.width = 50  # Approx player width
        self.height = 23  # Approx player height (reduced for hitbox)
        self.visual_height = 60 # Full visual height including tail
        self.on_ground = False
        self.on_wall = False
        self.wall_side = 0 # 1 for right, -1 for left
        self.wall_side = 0 # 1 for right, -1 for left
        self.hanging = False # New Player for ceiling stick
        self.is_dead = False # Death state
        self.wall_facing_down = False # Facing state for wall
        self.grapple_target=None
        self.grapple_speed=12
        self.grappling=False
        self.facing_dir = 1  # 1 = right, -1 = left
        self.max_grapple_dist = 500
        self.level_complete = False


        # Momentum
        self.momentum_x = 0

        # Load Level
        self.level = level
        self.xcoor, self.ycoor = self.level.player_start_pos
        self.tiles = self.level.tiles

        #find location of player
        # Camera
        self.camera = camera
        self.rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Coyote time
        self.coyote_timer = 0
        self.coyote_time = 6

        # Jump buffer (frames to remember jump input)
        self.jump_buffer = 0
        self.jump_buffer_time = 6

        # Gated jump-cut
        self.jump_held = False
        self.started_rise = False
        
        # Pre-load Sprites
        self.sprites = {}
        self.load_sprites()

    def reset(self):
        self.xcoor, self.ycoor = self.level.player_start_pos
        self.velocity_y = 0
        self.momentum_x = 0
        self.on_ground = False
        self.on_wall = False
        self.wall_side = 0
        self.hanging = False
        self.is_dead = False
        self.grappling = False
        self.grapple_target = None
        self.rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)
        # Reset health if needed, e.g. HealthBar.hp = 100 but HealthBar is global/static in standard_use usage
        HealthBar.hp = 100

    def load_sprites(self):

        try:
            self.sprites['right'] = pg.image.load('./resources/chameleon.png').convert_alpha()
            self.sprites['left'] = pg.image.load('./resources/chameleon_left.png').convert_alpha()
            self.sprites['ceiling'] = pg.image.load('./resources/chameleon_ceiling.png').convert_alpha()
            self.sprites['ceiling_left'] = pg.image.load('./resources/chameleon_ceiling_left.png').convert_alpha()
            self.sprites['left_wall'] = pg.image.load('./resources/chameleon_left_wall.png').convert_alpha()
            self.sprites['right_wall'] = pg.image.load('./resources/chameleon_right_wall.png').convert_alpha()
            self.sprites['right_wall_down'] = pg.image.load('./resources/cameleon_rightwall_down.png').convert_alpha()
            self.sprites['left_wall_down'] = pg.image.load('./resources/cammelion_leftwall_down.png').convert_alpha()
        except Exception as e:
            print(f"Error loading sprites: {e}")
            # Sprites will be missing, render methods should handle key errors or check existence
        
        # Load bush (static for now, but good to cache if used often)
        try:
             self.bush_img = pg.image.load('./resources/bush.png').convert()
             self.bush_img.set_colorkey((0, 0, 0))
        except:
             self.bush_img = None


    # Coyote reduction
    def update_coyote(self, dt):
        if self.on_ground or self.hanging or self.on_wall:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(0, self.coyote_timer - 1 * dt)

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

    # Track held key Player per frame
    def update_input_Player(self, keys):
    # Jump held: either UP arrow or W key
        self.jump_held = keys[pg.K_UP] or keys[pg.K_w]

    # You can also add other continuous input checks here later
    # (for example crouch, dash, etc.)
    
    def find_nearest_grapple_tile(self):
        nearest_tile = None
        nearest_dist = float("inf")

        for tile in self.tiles:
            if not getattr(tile, "grappleable", False):
                continue

            # Vector to tile
            dx = tile.rect.centerx - self.rect.centerx
            dy = tile.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)

            # Distance gate
            if dist > self.max_grapple_dist:
                continue

            # Facing cone check (wide ~120°)
            fx, fy = (self.facing_dir, 0)  # facing vector
            if dist > 0:
                nx, ny = dx / dist, dy / dist
                dot = fx * nx + fy * ny
                if dot < -0.5:  # outside cone
                    continue

            # Line-of-sight check
            if not self.can_grapple_to(tile):
                continue

            # If we reach here, tile is valid → compare distance
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_tile = tile

        return nearest_tile
    def grappling_hook(self, dt):
        if self.grappling and self.grapple_target:
            dx = self.grapple_target[0] - self.rect.centerx
            dy = self.grapple_target[1] - self.rect.centery
            dist = math.hypot(dx, dy)

            step = self.grapple_speed * dt
            if dist > step:
                # Move toward target
                vx = dx / dist * step
                vy = dy / dist * step
                self.rect.centerx += vx
                self.rect.centery += vy

                # Store momentum so it persists when released
                self.momentum_x = vx
                self.velocity_y = vy
            else:
                # Snap to target
                self.rect.center = self.grapple_target
                self.grappling = False
                self.grapple_target = None
    def can_grapple_to(self, target_tile):
    # Vector from player to tile
        x1, y1 = self.rect.center
        x2, y2 = target_tile.rect.center

        # Step along the line in small increments
        steps = int(math.hypot(x2 - x1, y2 - y1) / TILE_SIZE)
        for i in range(steps + 1):
            if steps != 0:
                t = i / steps
                check_x = x1 + (x2 - x1) * t
                check_y = y1 + (y2 - y1) * t
            

                # Build a point rect to test collisions
                point_rect = pg.Rect(check_x, check_y, 2, 2)

                for tile in self.tiles:
                    if tile.type == 'X' or tile.type == 'S':  # solid types
                        if tile.rect.colliderect(point_rect):
                            return False  # blocked by a wall

        return True  # clear line of sight
    
    def grapple_to(self, pos):
    # Set target and start grappling
        self.grapple_target = pos
        self.grappling = True

    def try_grapple(self, target_tile):
        dx = target_tile.rect.centerx - self.rect.centerx
        dy = target_tile.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > self.max_grapple_dist:
            print("Too far to grapple!")
            return

        # Facing check using dot product
        facing_vector = (self.facing_dir, 0)  # (1,0) for right, (-1,0) for left
        to_tile_vector = (dx, dy)

        dot = facing_vector[0] * to_tile_vector[0] + facing_vector[1] * to_tile_vector[1]
        if dot <= 0:
            print("Tile is behind you!")
            return

        if not self.can_grapple_to(target_tile):
            print("Blocked by wall!")
            return

        self.grapple_to(target_tile.rect.center)

    def update_physics(self, dx, keys, dt, rect):
        #grapling call
        
        if self.grappling and self.grapple_target:
            self.grappling_hook(dt)
            # IMPORTANT: Still check for death even while grappling
            player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)
            for tile in self.tiles:
                if tile.rect.colliderect(player_rect):
                    t_type = getattr(tile, 'type', 'X')
                    if t_type == 'D' or t_type == 'Y':
                        self.is_dead = True
            
        else:
    # normal gravity, collisions, etc.
        # Validate existing wall stick (Persistent Player)
            if self.on_wall:
                # Check for pull-off (Moving away from wall)
                # Only pull off if we ARE NOT trying to jump (buffered jump preserves wall Player for the kick)
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
        # Scale input movement by dt, but momentum is velocity, so apply it over time? 
        # Actually dx is displacement per frame (speed * 1 frame). 
        # So total_dx should be (dx + momentum) * dt.
        # Ensure momentum decay handles dt correctly.
        
        # We need to treat dx as velocity here if we are scaling by dt.
        # Currently dx is 5 pixels/frame. 
        
        total_dx = (dx + self.momentum_x) * dt
        
        # Decay momentum (air resistance / friction)
        # 0.9 per frame -> 0.9 ^ dt
        self.momentum_x *= 0.9 ** dt
        
        if abs(self.momentum_x) < 0.5:
             self.momentum_x = 0

        # Horizontal Movement
        self.xcoor += total_dx
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Horizontal collision
        
        
        if self.rect.colliderect(rect):
            HealthBar.hp -= 1
            print('1 dammage')
        
        
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                t_type = getattr(tile, 'type', 'X')
                if t_type in ['D', 'Y', 'F', 'C', 'L', 'R']:
                    self.is_dead = True
                
            
                if t_type == 'N':
                    self.level_complete = True                                        
                    
                    
                if t_type == 'S':
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
            if keys[pg.K_UP] or keys[pg.K_w]:
                dy = -5 * dt
                self.wall_facing_down = False
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                dy = 5 * dt
                self.wall_facing_down = True
        elif self.hanging:
            # Ceiling Stick
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.hanging = False # Drop
                dy = 5 * dt
            # UP does nothing while hanging? Or maybe clamber?
        else:
            # Gravity
            self.velocity_y += self.gravity * dt
            dy = self.velocity_y * dt

            # Mark when upward motion begins (for jump-cut gating)
            if self.velocity_y < 0:
                self.started_rise = True
    
            # Jump cut
            if self.started_rise and not self.jump_held and self.velocity_y < 0:
                self.velocity_y = max(self.velocity_y, self.jump_cut)
                # Recalculate dy with new velocity? Or just let it take effect next frame?
                # Better to use updated velocity for consistency, but physics engines vary.
                # Let's simple apply it.
                dy = self.velocity_y * dt

        # Apply Vertical Move
        self.ycoor += dy
        player_rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Vertical collision
        for tile in self.tiles:
            if tile.rect.colliderect(player_rect):
                t_type = getattr(tile, 'type', 'X')
                if t_type in ['D', 'Y', 'F', 'C', 'L', 'R']:
                    self.is_dead = True
                if t_type == 'N':
                    self.level_complete = True                                        
                if dy < 0: # Moving Up
                     if t_type == 'S':
                         # Ceiling stick
                         self.ycoor = tile.rect.bottom
                         self.velocity_y = 0
                         self.hanging = True
                     else:
                         self.ycoor = tile.rect.bottom
                         self.velocity_y = 0
                if t_type == 'N':
                    self.level_complete = True  
                elif dy > 0: # Falling / Moving Down
                    self.ycoor = tile.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.momentum_x = 0 # Friction on ground? Maybe not instantly, but let's reset for control consistency
        
        # Update rect for camera use
        self.rect = pg.Rect(self.xcoor, self.ycoor, self.width, self.height)

        # Update coyote after collision resolution
        self.update_coyote(dt)

        # Consume buffered jump now that collision is resolved
        self.try_consume_jump(keys)

        # Decay jump buffer
        if self.jump_buffer > 0:
            self.jump_buffer -= 1 * dt

        

    def render_map(self, surface, show_hitboxes=False):
        self.level.render(surface, self.camera, show_hitboxes)

    def render_chameleon(self, surface):
        

            if 'right' in self.sprites:
                chameleon_img = self.sprites['right']
                rect = chameleon_img.get_rect()
                rect.centerx = self.rect.centerx
                rect.top = self.rect.top
                shifted_rect = self.camera.apply_rect(rect)
                surface.blit(chameleon_img, shifted_rect)
            else:
                shifted_rect = self.camera.apply_rect(self.rect)
                pg.draw.rect(surface, (255, 0, 0), shifted_rect)

    def render_chameleon_left(self, surface):
        

            if 'left' in self.sprites:
                chameleon_img = self.sprites['left']
                rect = chameleon_img.get_rect()
                rect.centerx = self.rect.centerx
                rect.top = self.rect.top
                shifted_rect = self.camera.apply_rect(rect)
                surface.blit(chameleon_img, shifted_rect)
            else:
                shifted_rect = self.camera.apply_rect(self.rect)
                pg.draw.rect(surface, (255, 0, 0), shifted_rect)

    def render_chameleon_ceiling_left(self, surface):
        if 'ceiling_left' in self.sprites:
            chameleon_img = self.sprites['ceiling_left']
            rect = chameleon_img.get_rect()
            rect.centerx = self.rect.centerx
            rect.top = self.rect.top
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (255, 0, 0), shifted_rect)

    def render_chameleon_ceiling(self, surface):
        if 'ceiling' in self.sprites:
            chameleon_img = self.sprites['ceiling']
            rect = chameleon_img.get_rect()
            rect.centerx = self.rect.centerx
            rect.top = self.rect.top
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (255, 0, 0), shifted_rect)
        
    def render_chameleon_left_wall(self, surface):
        if 'left_wall' in self.sprites:
            chameleon_img = self.sprites['left_wall']
            rect = chameleon_img.get_rect()
            rect.left = self.rect.left
            rect.bottom = self.rect.bottom
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (255, 0, 0), shifted_rect)

    def render_chameleon_right_wall(self, surface):
        if 'right_wall' in self.sprites:
            chameleon_img = self.sprites['right_wall']
            rect = chameleon_img.get_rect()
            rect.right = self.rect.right
            rect.bottom = self.rect.bottom
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (0, 0, 255), shifted_rect)

    def render_chameleon_right_wall_down(self, surface):
        if 'right_wall_down' in self.sprites:
            chameleon_img = self.sprites['right_wall_down']
            rect = chameleon_img.get_rect()
            rect.right = self.rect.right
            rect.bottom = self.rect.bottom
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (0, 0, 255), shifted_rect)

    def render_chameleon_left_wall_down(self, surface):
        if 'left_wall_down' in self.sprites:
            chameleon_img = self.sprites['left_wall_down']
            rect = chameleon_img.get_rect()
            rect.left = self.rect.left
            rect.bottom = self.rect.bottom
            shifted_rect = self.camera.apply_rect(rect)
            surface.blit(chameleon_img, shifted_rect)
        else:
            shifted_rect = self.camera.apply_rect(self.rect)
            pg.draw.rect(surface, (255, 0, 0), shifted_rect)