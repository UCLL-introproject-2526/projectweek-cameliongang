import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, type='spiky'):
        super().__init__(pos, groups, obstacle_sprites)
        self.enemy_type = type
        self.player = None 
        
        if self.enemy_type == 'slime':
             self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'enemy_slime.png')).convert_alpha()
             self.power_type = 'sticky'
        else:
             self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'enemy.png')).convert_alpha()
             self.power_type = 'fire'

        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # AI State
        self.state = 'patrol' 
        self.direction.x = 1
        self.speed = 2
        
        # Attack Coolers
        self.attack_cooldown = 0
        self.attack_timer = 0 # For active attack frames
        self.is_attacking = False
        self.jump_timer = 0 # For slime jump warmup

    def update(self):
        self.attack_cooldown -= 1
        
        if self.state == 'attack':
            self.attack_state()
        elif self.state == 'chase':
            self.chase_state()
        else:
            self.patrol_state()
            
        # Physics
        self.apply_physics()
        
    def patrol_state(self):
        # Scan for player check
        if self.player and not self.player.is_camouflaged:
            dist = (pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)).length()
            if dist < 300:
                self.state = 'chase'
                return

        # Patrol Movement
        look_ahead_x = self.rect.right + 2 if self.direction.x > 0 else self.rect.left - 2
        look_ahead_rect = pygame.Rect(look_ahead_x, self.rect.bottom + 2, 2, 2)
        
        floor_detected = False
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(look_ahead_rect):
                floor_detected = True
                break
        
        if not floor_detected or self.velocity.x == 0:
            self.direction.x *= -1
            
        self.speed = 2
        self.velocity.x = self.direction.x * self.speed
    
    def chase_state(self):
        if not self.player or self.player.is_camouflaged:
            self.state = 'patrol'
            return
            
        dist_vec = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        dist = dist_vec.length()
        
        if dist > 400: # Lost interest
            self.state = 'patrol'
            return
            
        # Range check for Attack
        attack_range = 60 if self.enemy_type == 'spiky' else 150 # Slime jumps from further
        
        if dist < attack_range and self.attack_cooldown <= 0:
            self.state = 'attack'
            self.attack_timer = 0
            if self.enemy_type == 'slime':
                self.jump_timer = 30 # Warmup frames
            return
            
        # Move towards player
        if dist_vec.x > 0: self.direction.x = 1
        else: self.direction.x = -1
        
        self.speed = 4
        self.velocity.x = self.direction.x * self.speed

    def attack_state(self):
        self.velocity.x = 0 # Stop while attacking (usually)
        self.attack_timer += 1
        
        if self.enemy_type == 'spiky':
            # Slash Attack
            if self.attack_timer == 30: # Hit frame
                # Create hitbox
                hit_rect = pygame.Rect(0, 0, 40, 40)
                if self.direction.x > 0: hit_rect.midleft = self.rect.midright
                else: hit_rect.midright = self.rect.midleft
                
                if self.player.rect.colliderect(hit_rect):
                    self.player.take_damage(1, self.rect.center)
            
            if self.attack_timer > 60: # End attack
                self.state = 'chase'
                self.attack_cooldown = 120
                
        elif self.enemy_type == 'slime':
            # Jump Attack
            if self.jump_timer > 0:
                self.jump_timer -= 1
                # Wiggle/Flash warning?
            else:
                # Launch
                if self.on_ground:
                    # Aim at player
                    dist_x = self.player.rect.centerx - self.rect.centerx
                    jump_dir = 1 if dist_x > 0 else -1
                    
                    self.velocity.y = -15
                    self.velocity.x = jump_dir * 8
                    self.on_ground = False
                
                # While in air, damage on contact
                if not self.on_ground:
                    if self.rect.colliderect(self.player.rect):
                        self.player.take_damage(1, self.rect.center)
                        
                if self.on_ground and self.attack_timer > 30: # Landed
                    self.state = 'chase'
                    self.attack_cooldown = 180

    def apply_physics(self):
        # X
        if self.state == 'attack' and self.enemy_type == 'slime' and self.jump_timer <= 0:
             # Keep momentum in air
             pass
        elif self.state == 'attack' and self.enemy_type == 'spiky':
             self.velocity.x = 0
        else:
             self.velocity.x = self.direction.x * self.speed

        self.rect.x += self.velocity.x
        self.check_horizontal_collision()
        
        # Y
        self.apply_gravity()
        self.rect.y += self.velocity.y
        self.check_vertical_collision()
