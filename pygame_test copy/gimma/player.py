import pygame, math
from settings import *
from entity import Entity
from particles import Particle

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, enemy_sprites, particle_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        self.enemy_sprites = enemy_sprites
        self.particle_sprites = particle_sprites
        self.visible_sprites = groups[0] # Assuming first group is visible/camera group
        
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'player.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # Player specific variables
        self.jump_speed = JUMP_STRENGTH
        self.on_ground = False
        self.power = None # Store current power
        self.jump_count = 0 # Track jumps for double jump
        
        # Tongue / Grapple
        self.grapple_target = None # Vector2 or None
        self.grapple_mode = None # 'swing' or 'pull'
        self.rope_length = 0
        self.grapple_speed = TONGUE_SPEED
        self.pull_speed = PULL_SPEED
        self.clicked = False # Track mouse click state

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Grapple Shoot
        # Left Click (0) -> Swing Mode
        # Right Click (2) -> Pull Mode
        if mouse_buttons[0]:
            if not self.clicked and not self.grapple_target:
                self.shoot_tongue('swing')
            self.clicked = True
        elif mouse_buttons[2]:
            if not self.clicked and not self.grapple_target:
                self.shoot_tongue('pull')
            self.clicked = True
        else:
            self.clicked = False
            # Stop Grapple if Mouse Released (for both modes)
            if self.grapple_target:
                self.grapple_target = None
            
        # Jump / Cancel Grapple
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_z] or keys[pygame.K_UP]
        
        if jump_pressed and self.grapple_target:
            self.grapple_target = None
            # Boost jump when detaching from swing
            if self.grapple_mode == 'swing':
                self.velocity.y = -12 # Initial jump boost off rope
            return

        # Movement Input
        left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]
        right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Standard Movement
        if not self.grapple_target:
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

        # Swinging Movement (Simplified Global Force)
        elif self.grapple_mode == 'swing':
            # Swing Trail
            if abs(self.velocity.x) > 10 or abs(self.velocity.y) > 10:
                if pygame.time.get_ticks() % 5 == 0: # Throttle emission
                    Particle(self.rect.center, [self.visible_sprites], 'dust')
            # Apply horizontal force directly
            # The rope constraint will handle the "swing" arc conversion.
            # This feels more intuitive (Left = Go Left, Right = Go Right).
            force = ACCELERATION * 0.5 # Reduced control in air
            
            if right_pressed:
                self.velocity.x += force
            elif left_pressed:
                self.velocity.x -= force
            
            # Add slight air drag to prevent infinite speed buildup
            self.velocity *= 0.99

        # Cap speed
        max_speed = 8 if not self.grapple_target else 15 # Reduced from 25
        if self.velocity.x > max_speed: self.velocity.x = max_speed
        if self.velocity.x < -max_speed: self.velocity.x = -max_speed


    def shoot_tongue(self, mode):
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
        check_dist = min(dist_to_mouse, TONGUE_LENGTH)
        
        found_hit = False
        
        for i in range(1, int(check_dist), 8):
            check_pos = start_pos + direction * i
            check_rect = pygame.Rect(check_pos.x - 4, check_pos.y - 4, 8, 8)
            
            # Check Enemies (Eat valid, Swing/Pull invalid usually, but let's allow sticking to them for fun?)
            for enemy in self.enemy_sprites:
                if enemy.rect.colliderect(check_rect):
                    self.power = enemy.power_type
                    self.image.fill(enemy.image.get_at((0,0))) 
                    enemy.kill() 
                    found_hit = True
                    break 
            if found_hit: break

            # Check Obstacles
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(check_rect):
                    self.grapple_target = check_pos
                    self.grapple_mode = mode
                    if mode == 'swing':
                         # Set rope length to current distance
                         self.rope_length = (self.grapple_target - pygame.math.Vector2(self.rect.center)).length()
                    found_hit = True
                    break 
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
            # Jump Particles
            Particle(self.rect.midbottom, [self.visible_sprites], 'jump')
            Particle(self.rect.midbottom, [self.visible_sprites], 'jump')
        elif self.power == 'fire' and self.jump_count < 1:
            self.velocity.y = self.jump_speed
            self.jump_count += 1
            # Double Jump Particles
            Particle(self.rect.midbottom, [self.visible_sprites], 'spark')

    def move(self):
        if self.grapple_target:
            if self.grapple_mode == 'pull':
                self.pull_physics()
            elif self.grapple_mode == 'swing':
                self.swing_physics()
        else:
            self.standard_physics()

    def standard_physics(self):
         # Horizontal
        self.rect.x += self.velocity.x
        self.check_horizontal_collision()

        # Vertical
        self.on_ground = False 
        self.apply_gravity()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()
    
    def pull_physics(self):
        # Original Hookshot Logic
        direction = (self.grapple_target - pygame.math.Vector2(self.rect.center))
        dist = direction.length()
        
        if dist < TILE_SIZE: # Arrived
            self.grapple_target = None
            self.velocity.y = -8 
            return
            
        if dist > 0:
            direction = direction.normalize()
        
        pull_force = 1.5
        self.velocity += direction * pull_force
        self.velocity *= 0.95 

        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()

    def swing_physics(self):
        # 1. Apply Gravity (Pendulum needs gravity!)
        self.apply_gravity()
        
        # 2. Rope Constraint (Verlet-ish)
        # Apply constraint BEFORE moving to prevent tunneling, then correct velocity
        current_pos = pygame.math.Vector2(self.rect.center)
        to_anchor = self.grapple_target - current_pos
        dist = to_anchor.length()
        
        if dist > self.rope_length:
            dir_to_anchor = to_anchor.normalize()
            # Pos Correction
            new_pos = self.grapple_target - (dir_to_anchor * self.rope_length)
            self.rect.center = (new_pos.x, new_pos.y)
            
            # Vel Correction (Kill radial velocity moving AWAY)
            radial_vel_mag = self.velocity.dot(dir_to_anchor)
            if radial_vel_mag < 0: # Moving away
                 self.velocity -= dir_to_anchor * radial_vel_mag
                 
            # Damping
            self.velocity *= 0.999 

        # 3. Move & Collide
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
                    if not self.on_ground: # Just landed
                         Particle(self.rect.bottomleft, [self.visible_sprites], 'dust')
                         Particle(self.rect.bottomright, [self.visible_sprites], 'dust')
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
            
            # Draw Chain
            color = (200, 150, 150) # Rope color
            direction = end_pos - start_pos
            length = direction.length()
            if length > 0:
                direction = direction.normalize()
                
                # Draw segments every 10 pixels
                for i in range(0, int(length), 10):
                    pos = start_pos + direction * i
                    pygame.draw.circle(surface, color, (int(pos.x), int(pos.y)), 3)
            
            # Draw Anchor point
            pygame.draw.circle(surface, RED, (int(end_pos.x), int(end_pos.y)), 5)

    def update(self):
        self.input()
        self.move()
