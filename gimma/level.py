import pygame
from settings import *
from player import Player
from enemy import Enemy
from particles import Particle
from objects import Bush, Mine

# Level Layouts
LEVEL_0 = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                                                                                    X',
            'X                   XXXXX                                                            X',
            'X         E            B                     S                                       X',
            'X       XXXXX      XX  XX   M              XXXXX                                     X',
            'X                   B    XX      XX                                                  X',
            'X      P      XX    B     XX                                              XXX        X',
            'XXXXXXXXXXXXXXX            XXXXXXXXXXXXXX           E                    XX X        X',
            'X                                         X         XXXX                XX  X        X',
            'X   Grapple Training!                     X                            XX   X        X',
            'X                                         X                           XX    X        X',
            'X          XXXX                           X       E                  XX     X        X',
            'X                                         X     XXXXX               XX      X        X',
            'X   X                                     X                        XX       X        X',
            'X   X     X                               X  Big Jump!            XX        X        X',
            'X   X     X     X      X                  XXXXXXXXXXXXXXXXXXXXXXXX          X        X',
            'X                                                                           X        X',
            'X                  E                                                        X        X',
            'X               XXXXXXX                                                     X        X',
            'X                                                                           X        X',
            'X   XXXXXX    XXXXXXXXXXX               XXXXXXX                             X        X',
            'X        X    X         X                                                   X        X',
            'X        X    X    E    X                                                   X        X',
            'X        XXXXXX   XXX   X                                                   X        X',
            'X                       X                                                   X        X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

LEVEL_1 = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                          X',
            'X             E            X',
            'X            XXX           X',
            'X           XX XX          X',
            'X          XX   XX         X',
            'X         XX     S         X',
            'X        XX     XXX        X',
            'X       XX                 X',
            'X      XX           X      X',
            'X     XX    B      XX      X',
            'X    XX     M     XXX      X',
            'X   XX           XXXX      X',
            'X   X           XXXXX      X',
            'X P X          XXXXXX      X',
            'XXXXXXXX      XXXXXXX      X',
            'X            XXXXXXXX      X',
            'X           XXXXXXXXX      X',
            'X          XXXXXXXXXX      X',
            'X         XXXXXXXXXXX      X',
            'X        XXXXXXXXXXXX      X',
            'X       XXXXXXXXXXXXX      X',
            'X      XXXXXXXXXXXXXX      X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

LEVEL_2 = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                          X',
            'X             E            X',
            'X            XXX           X',
            'X           XX XX          X',
            'X          XX   XX         X',
            'X         XX     S         X',
            'X        XX     XXX        X',
            'X       XX                 X',
            'X      XX           X      X',
            'X     XX           XX      X',
            'X    XX    B      XXX      X',
            'X   XX     M     XXXX      X',
            'X   X      M    XXXXX      X',
            'X P X          XXXXXX      X',
            'XXXXXXXX      XXXXXXX      X',
            'X            XXXXXXXX      X',
            'X           XXXXXXXXX      X',
            'X          XXXXXXXXXX      X',
            'X         XXXXXXXXXXX      X',
            'X        XXXXXXXXXXXX      X',
            'X       XXXXXXXXXXXXX      X',
            'X      XXXXXXXXXXXXXX      X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

LEVEL_3 = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X          P               X',
            'X        XXXXX             X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X            E             X',
            'X          XXXXX           X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'X                          X',
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

LEVELS = [LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3]

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'tile.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        # Center camera setup
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        # 1. Camera Logic (Smooth Lerp + Lookahead)
        # Target offset
        target_offset_x = player.rect.centerx - self.half_w
        target_offset_y = player.rect.centery - self.half_h
        
        # Smoothly move current offset to target
        self.offset.x += (target_offset_x - self.offset.x) * 0.1
        self.offset.y += (target_offset_y - self.offset.y) * 0.1
        
        # 2. Background (Parallax Grid)
        self.display_surface.fill(BG_COLOR)
        
        # Grid settings
        grid_size = 64
        grid_color = (40, 40, 40)
        
        # Offset for parallax (moves slower than camera)
        parallax_factor = 0.5
        parallax_offset_x = (self.offset.x * parallax_factor) % grid_size
        parallax_offset_y = (self.offset.y * parallax_factor) % grid_size
        
        cols = WIDTH // grid_size + 2
        rows = HEIGHT // grid_size + 2
        
        # Draw Lines
        for col in range(cols):
            x = col * grid_size - parallax_offset_x
            pygame.draw.line(self.display_surface, grid_color, (x, 0), (x, HEIGHT))
            
        for row in range(rows):
            y = row * grid_size - parallax_offset_y
            pygame.draw.line(self.display_surface, grid_color, (0, y), (WIDTH, y))

        # 3. Draw Sprites (Ground, Enemies, Player)
        # Sort by Y position for slight depth overlap if needed
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # 4. Draw Tongue
        player.draw_tongue(self.display_surface, self.offset)

class Level:
    def __init__(self, level_index=0):
        self.display_surface = pygame.display.get_surface()
        self.current_level_index = level_index
        
        # Sprite groups
        self.visible_sprites = CameraGroup() # Custom Camera Group
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.particle_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        
        # Setup level
        self.create_map()
        
        # Link player to enemies
        for enemy in self.enemy_sprites:
            enemy.player = self.player

    def create_map(self):
        map_data = LEVELS[self.current_level_index]


        for row_index, row in enumerate(map_data):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if col == 'X':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'P':
                    self.player = Player(
                        (x, y), 
                        [self.visible_sprites], 
                        self.obstacle_sprites, 
                        self.enemy_sprites,
                        self.particle_sprites,
                        self.interactable_sprites
                    )
                    
                    self.player.visible_sprites = self.visible_sprites
                    
                if col == 'E':
                    Enemy((x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, type='spiky')
                if col == 'S':
                    Enemy((x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, type='slime')
                if col == 'B':
                    Bush((x, y), [self.visible_sprites, self.interactable_sprites])
                if col == 'M':
                    Mine((x, y), [self.visible_sprites, self.interactable_sprites])

    def run(self):
        # Update and draw
        
        # Update Logic
        self.visible_sprites.update()
        # Particle sprites update logic is handled via visible_sprites update if added there
        
        # Custom Draw (Camera)
        self.visible_sprites.custom_draw(self.player)
