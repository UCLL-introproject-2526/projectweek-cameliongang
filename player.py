import pygame, math
from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, enemy_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        self.enemy_sprites = enemy_sprites
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # Player specific variables
        self.jump_speed = JUMP_STRENGTH
        self.on_ground = False
        self.power = None # Store current power
        self.jump_count = 0 # Track jumps for double jump
        
        # Tongue / Grapple
        self.grapple_target = None # Vector2 or None
        self.grapple_speed = TONGUE_SPEED
        self.pull_speed = PULL_SPEED
        self.clicked = False # Track mouse click state

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Grapple Shoot (Left Click) - Only on initial press
        if mouse_buttons[0]:
            if not self.clicked and not self.grapple_target:
                self.shoot_tongue()
            self.clicked = True
        else:
            self.clicked = False
            # Stop Grapple if Mouse Released
            if self.grapple_target:
                self.grapple_target = None
            
        # Jump / Cancel Grapple
        # Supports WASD (W), Arrows (Space/Up), and AZERTY (Z)
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_z] or keys[pygame.K_UP]
        
        if jump_pressed and self.grapple_target:
            self.grapple_target = None
            # Do NOT call self.jump() here to avoid infinite climbing.
            # Just detach and let gravity take over, or user can jump again if they have jumps left.
            return

        # Regular Movement Input
        if not self.grapple_target:
            # Horizontal Movement
            # A/Left or Q/Left
            left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]
            right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            
            if right_pressed:
                self.velocity.x += ACCELERATION
            elif left_pressed:
                self.velocity.x -= ACCELERATION
            else:
                # Friction
                if self.velocity.x > 0:
                    self.velocity.x -= FRICTION
                    if self.velocity.x < 0: self.velocity.x = 0
                elif self.velocity.x < 0:
                    self.velocity.x += FRICTION
                    if self.velocity.x > 0: self.velocity.x = 0
            
            # Jumping
            if jump_pressed:
                if self.on_ground:
                    self.jump()
                elif self.power == 'fire' and self.jump_count < 1: # Allow 1 extra jump
                    self.jump()
        else:
            # Grappling Input (maybe Swing later, for now just Pull)
            pass

        # Cap speed
        max_speed = 8
        if self.velocity.x > max_speed: self.velocity.x = max_speed
        if self.velocity.x < -max_speed: self.velocity.x = -max_speed


    def shoot_tongue(self):
        m_pos = pygame.mouse.get_pos()
        
        # Calculate cursor world position
        half_w = pygame.display.get_surface().get_width() // 2
        half_h = pygame.display.get_surface().get_height() // 2
        offset = pygame.math.Vector2(self.rect.centerx - half_w, self.rect.centery - half_h)
        mouse_world_pos = pygame.math.Vector2(m_pos) + offset
        
        start_pos = pygame.math.Vector2(self.rect.center)
        direction = mouse_world_pos - start_pos
        dist_to_mouse = direction.length()
        
        if dist_to_mouse == 0: return # Avoid divide by zero
        
        direction = direction.normalize()
        
        # Limit ray to Tongue Length OR Mouse Distance (whichever is shorter? or just Tongue Length?)
        # User said "click past a wall".
        # If I click past a wall, dist_to_mouse > dist_to_wall.
        # Raycast will hit wall.
        # If I click in air (short of wall), dist_to_mouse < dist_to_wall.
        # I should limit the ray to dist_to_mouse to satisfy "in air does nothing".
        # If I let it go further, I might hit a wall BEHIND my cursor, which violates "exactly where i click".
        # So: Limit to dist_to_mouse.
        
        check_dist = min(dist_to_mouse, TONGUE_LENGTH)
        
        found_hit = False
        
        for i in range(1, int(check_dist), 8): # Precision step
            check_pos = start_pos + direction * i
            check_rect = pygame.Rect(check_pos.x - 4, check_pos.y - 4, 8, 8)
            
            # Check Enemies first
            for enemy in self.enemy_sprites:
                if enemy.rect.colliderect(check_rect):
                    # EAT ENEMY
                    self.power = enemy.power_type
                    self.image.fill(enemy.image.get_at((0,0))) 
                    enemy.kill() 
                    found_hit = True
                    break # Stop ray
            if found_hit: break

            # Check Obstacles
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(check_rect):
                    self.grapple_target = check_pos
                    found_hit = True
                    break # Stop ray
            if found_hit: break

    def jump(self):
        # Wall Jump (Sticky Power)
        if self.power == 'sticky' and not self.on_ground:
            # Check walls
            right_check = pygame.Rect(self.rect.right, self.rect.y, 2, self.rect.height)
            left_check = pygame.Rect(self.rect.left - 2, self.rect.y, 2, self.rect.height)
            
            wall_right = False
            wall_left = False
            
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(right_check): wall_right = True
                if sprite.rect.colliderect(left_check): wall_left = True
            
            # Input check
            keys = pygame.key.get_pressed()
            left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]
            right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            if wall_right:
                if left_pressed: # Jump Away
                    self.velocity.y = -16
                    self.velocity.x = -12
                elif right_pressed: # Climb Up (Vex style wall scale)
                    self.velocity.y = -14
                    self.velocity.x = 2 # Keep sticking
                return
            
            if wall_left:
                if right_pressed: # Jump Away
                    self.velocity.y = -16
                    self.velocity.x = 12
                elif left_pressed: # Climb Up
                    self.velocity.y = -14
                    self.velocity.x = -2 # Keep sticking
                return

        # Normal & Double Jump
        if self.on_ground:
            self.velocity.y = self.jump_speed
            self.jump_count = 0 # Reset
        elif self.power == 'fire' and self.jump_count < 1:
            self.velocity.y = self.jump_speed
            self.jump_count += 1

    def move(self):
        if self.grapple_target:
            self.grapple_move()
        else:
            # Horizontal
            self.rect.x += self.velocity.x
            self.check_horizontal_collision()

            # Vertical
            self.on_ground = False # Assume air until collision proves otherwise
            self.apply_gravity()
            self.rect.y += self.velocity.y
            self.check_vertical_collision()
    
    def grapple_move(self):
        # Move towards target
        direction = (self.grapple_target - pygame.math.Vector2(self.rect.center))
        dist = direction.length()
        
        if dist < TILE_SIZE: # Arrived
            self.grapple_target = None
            # Momentum preservation: Keep velocity but cap it slightly to prevent crazy flings?
            # self.velocity = self.velocity * 0.8 
            self.velocity.y = -8 # Pop up a bit
            return
            
        if dist > 0:
            direction = direction.normalize()
        
        # Physics: Add force towards target (Swing/Pull)
        pull_force = 1.5
        self.velocity += direction * pull_force
        
        # Air drag/Damping while grappling
        self.velocity *= 0.95 

        # Apply movement
        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        
        self.rect.y += self.velocity.y
        self.check_vertical_collision()

    def apply_gravity(self):
        self.velocity.y += GRAVITY
        if self.velocity.y > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY
        
        # Wall Slide (Vex Style)
        if self.power == 'sticky' and self.velocity.y > 0: # Only if falling
            # Check for walls using a slightly wider rect
            right_check = pygame.Rect(self.rect.right, self.rect.y, 2, self.rect.height)
            left_check = pygame.Rect(self.rect.left - 2, self.rect.y, 2, self.rect.height)
            
            touching_wall = False
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(right_check) or sprite.rect.colliderect(left_check):
                    touching_wall = True
                    break
            
            if touching_wall:
                self.velocity.y = min(self.velocity.y, 4) # Cap fall speed (Slide)

    def check_vertical_collision(self):
        # Override to set on_ground
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.y > 0: # Falling
                    self.rect.bottom = sprite.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                    self.jump_count = 0 # Reset jump count
                elif self.velocity.y < 0: # Jumping into ceiling
                    self.rect.top = sprite.rect.bottom
                    self.velocity.y = 0
    
    def draw_tongue(self, surface, offset):
        # Draw tongue if grappling
        if self.grapple_target:
            start_pos = self.rect.center - offset
            end_pos = self.grapple_target - offset
            pygame.draw.line(surface, TONGUE_COLOR, start_pos, end_pos, 4)

    def update(self):
        self.input()
        self.move()
