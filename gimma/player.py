import pygame, math
from settings import *
from entity import Entity
from particles import Particle

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, enemy_sprites, particle_sprites, interactable_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        self.enemy_sprites = enemy_sprites
        self.particle_sprites = particle_sprites
        self.interactable_sprites = interactable_sprites
        self.visible_sprites = groups[0] 
        
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'player.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # Player specific variables
        self.jump_speed = JUMP_STRENGTH
        self.on_ground = False
        self.power = None 
        self.jump_count = 0 
        self.is_camouflaged = False
        
        # Health
        self.hp = 3
        self.invincible = False
        self.invincible_timer = 0
        
        # Tongue / Grapple
        self.grapple_target = None 
        self.grapple_mode = None 
        self.rope_length = 0
        self.grapple_speed = TONGUE_SPEED
        self.pull_speed = PULL_SPEED
        self.clicked = False 

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Grapple Shoot
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
            if self.grapple_target:
                self.grapple_target = None
            
        # Jump / Cancel Grapple
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_z] or keys[pygame.K_UP]
        
        if jump_pressed and self.grapple_target:
            self.grapple_target = None
            if self.grapple_mode == 'swing':
                self.velocity.y = -12 
            return

        # Movement Input
        left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]
        right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        if not self.grapple_target:
            if right_pressed:
                self.velocity.x += ACCELERATION
            elif left_pressed:
                self.velocity.x -= ACCELERATION
            else:
                if self.velocity.x > 0:
                    self.velocity.x -= FRICTION
                    if self.velocity.x < 0: self.velocity.x = 0
                elif self.velocity.x < 0:
                    self.velocity.x += FRICTION
                    if self.velocity.x > 0: self.velocity.x = 0
            
            if jump_pressed:
                if self.on_ground:
                    self.jump()
                elif self.power == 'fire' and self.jump_count < 1: 
                    self.jump()

        elif self.grapple_mode == 'swing':
            if abs(self.velocity.x) > 10 or abs(self.velocity.y) > 10:
                if pygame.time.get_ticks() % 5 == 0: 
                    Particle(self.rect.center, [self.visible_sprites], 'dust')

            force = ACCELERATION * 0.5 
            
            if right_pressed:
                self.velocity.x += force
            elif left_pressed:
                self.velocity.x -= force
            
            self.velocity *= 0.99 

        max_speed = 8 if not self.grapple_target else 15 
        if self.velocity.x > max_speed: self.velocity.x = max_speed
        if self.velocity.x < -max_speed: self.velocity.x = -max_speed

    def shoot_tongue(self, mode):
        m_pos = pygame.mouse.get_pos()
        half_w = pygame.display.get_surface().get_width() // 2
        half_h = pygame.display.get_surface().get_height() // 2
        offset = pygame.math.Vector2(self.rect.centerx - half_w, self.rect.centery - half_h)
        mouse_world_pos = pygame.math.Vector2(m_pos) + offset
        
        start_pos = pygame.math.Vector2(self.rect.center)
        direction = mouse_world_pos - start_pos
        dist_to_mouse = direction.length()
        
        if dist_to_mouse == 0: return 
        
        direction = direction.normalize()
        check_dist = min(dist_to_mouse, TONGUE_LENGTH)
        
        found_hit = False
        
        for i in range(1, int(check_dist), 8):
            check_pos = start_pos + direction * i
            check_rect = pygame.Rect(check_pos.x - 4, check_pos.y - 4, 8, 8)
            
            for enemy in self.enemy_sprites:
                if enemy.rect.colliderect(check_rect):
                    self.power = enemy.power_type
                    self.image.fill(enemy.image.get_at((0,0))) 
                    enemy.kill() 
                    found_hit = True
                    break 
            if found_hit: break

            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(check_rect):
                    self.grapple_target = check_pos
                    self.grapple_mode = mode
                    if mode == 'swing':
                         self.rope_length = (self.grapple_target - pygame.math.Vector2(self.rect.center)).length()
                    found_hit = True
                    break 
            if found_hit: break

    def jump(self):
        if self.power == 'sticky' and not self.on_ground:
            right_check = pygame.Rect(self.rect.right, self.rect.y, 2, self.rect.height)
            left_check = pygame.Rect(self.rect.left - 2, self.rect.y, 2, self.rect.height)
            
            wall_right = False
            wall_left = False
            
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(right_check): wall_right = True
                if sprite.rect.colliderect(left_check): wall_left = True
            
            keys = pygame.key.get_pressed()
            left_pressed = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]
            right_pressed = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            if wall_right:
                if left_pressed: 
                    self.velocity.y = -16
                    self.velocity.x = -12
                elif right_pressed: 
                    self.velocity.y = -14
                    self.velocity.x = 2 
                return
            
            if wall_left:
                if right_pressed: 
                    self.velocity.y = -16
                    self.velocity.x = 12
                elif left_pressed: 
                    self.velocity.y = -14
                    self.velocity.x = -2 
                return

        if self.on_ground:
            self.velocity.y = self.jump_speed
            self.jump_count = 0 
            Particle(self.rect.midbottom, [self.visible_sprites], 'jump')
            Particle(self.rect.midbottom, [self.visible_sprites], 'jump')
        elif self.power == 'fire' and self.jump_count < 1:
            self.velocity.y = self.jump_speed
            self.jump_count += 1
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
        self.rect.x += self.velocity.x
        self.check_horizontal_collision()

        self.on_ground = False 
        self.apply_gravity()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()
    
    def pull_physics(self):
        direction = (self.grapple_target - pygame.math.Vector2(self.rect.center))
        dist = direction.length()
        
        if dist < TILE_SIZE: 
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
        self.apply_gravity()
        
        current_pos = pygame.math.Vector2(self.rect.center)
        to_anchor = self.grapple_target - current_pos
        dist = to_anchor.length()
        
        if dist > self.rope_length:
            dir_to_anchor = to_anchor.normalize()
            new_pos = self.grapple_target - (dir_to_anchor * self.rope_length)
            self.rect.center = (new_pos.x, new_pos.y)
            
            radial_vel_mag = self.velocity.dot(dir_to_anchor)
            if radial_vel_mag < 0: 
                 self.velocity -= dir_to_anchor * radial_vel_mag
                 
            self.velocity *= 0.999 

        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()

    def apply_gravity(self):
        self.velocity.y += GRAVITY
        if self.velocity.y > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY
        
        if self.power == 'sticky' and self.velocity.y > 0: 
            right_check = pygame.Rect(self.rect.right, self.rect.y, 2, self.rect.height)
            left_check = pygame.Rect(self.rect.left - 2, self.rect.y, 2, self.rect.height)
            
            touching_wall = False
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(right_check) or sprite.rect.colliderect(left_check):
                    touching_wall = True
                    break
            
            if touching_wall:
                self.velocity.y = min(self.velocity.y, 4) 

    def check_vertical_collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.velocity.y > 0: 
                    self.rect.bottom = sprite.rect.top
                    self.velocity.y = 0
                    if not self.on_ground: 
                         Particle(self.rect.bottomleft, [self.visible_sprites], 'dust')
                         Particle(self.rect.bottomright, [self.visible_sprites], 'dust')
                    self.on_ground = True
                    self.jump_count = 0 
                elif self.velocity.y < 0: 
                    self.rect.top = sprite.rect.bottom
                    self.velocity.y = 0
    
    def draw_tongue(self, surface, offset):
        if self.grapple_target:
            start_pos = self.rect.center - offset
            end_pos = self.grapple_target - offset
            
            color = (200, 150, 150) 
            direction = end_pos - start_pos
            length = direction.length()
            if length > 0:
                direction = direction.normalize()
                
                for i in range(0, int(length), 10):
                    pos = start_pos + direction * i
                    pygame.draw.circle(surface, color, (int(pos.x), int(pos.y)), 3)
            
            pygame.draw.circle(surface, RED, (int(end_pos.x), int(end_pos.y)), 5)

    def update(self):
        self.input()
        self.move()
        self.check_interactions()
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image.set_alpha(255)
            else:
                 if self.invincible_timer % 10 < 5:
                     self.image.set_alpha(100)
                 else:
                     self.image.set_alpha(255)

    def take_damage(self, amount, source_pos):
        if not self.invincible:
            self.hp -= amount
            if self.hp <= 0:
                print("Player Died!")
                self.hp = 3
                
            self.invincible = True
            self.invincible_timer = 60
            
            self.knockback(source_pos)
            Particle(self.rect.center, [self.visible_sprites], 'spark') 

    def check_interactions(self):
        keys = pygame.key.get_pressed()
        
        on_bush = False
        hit_objects = pygame.sprite.spritecollide(self, self.interactable_sprites, False)
        
        for obj in hit_objects:
            if getattr(obj, 'type', '') == 'bush':
                if keys[pygame.K_c]:
                    on_bush = True
            
            if getattr(obj, 'type', '') == 'mine':
                center = obj.rect.center
                self.knockback(center)
                for _ in range(10): 
                    Particle(center, [self.visible_sprites], 'spark')
                obj.kill()
        
        if on_bush:
            self.is_camouflaged = True
            self.image.set_alpha(100) 
        else:
            self.is_camouflaged = False
            self.image.set_alpha(255)

    def knockback(self, source_pos):
        direction = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(source_pos)
        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(0, -1) 
            
        self.velocity = direction * 15 
        self.velocity.y = -10 
