import pygame
from settings import *
from player import Player
from enemy import Enemy

# Level Layouts
LEVEL_0 = [
            'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'X                                                                                    X',
            'X                   XXXXX                                                            X',
            'X         E                                  S                                       X',
            'X       XXXXX      XX  XX                  XXXXX                                     X',
            'X                XX      XX                                                          X',
            'X      P      XX          XX                                              XXX        X',
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
            'X     XX           XX      X',
            'X    XX           XXX      X',
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
            'X    XX           XXX      X',
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
        self.image = pygame.image.load('assets/tile.png').convert_alpha()
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

    def custom_draw(self, surface, player):
        # Calculate offset
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        # Draw ground/enemies/player with offset
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, offset_pos)

        # Draw tongue
        player.draw_tongue(surface, self.offset)

class Level:
    # Ref: http://projectweek.leone.ucll.be/stories/gui/game-state/index.html
    def __init__(self, level_index=0):
        # self.display_surface = pygame.display.get_surface() # Removed, passed in render
        self.current_level_index = level_index
        
        # Sprite groups
        self.visible_sprites = CameraGroup() # Custom Camera Group
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # Setup level
        self.create_map()

    def create_map(self):
        map_data = LEVELS[self.current_level_index]

        for row_index, row in enumerate(map_data):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if col == 'X':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'P':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.enemy_sprites)
                if col == 'E':
                    Enemy((x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, type='spiky')
                if col == 'S':
                    Enemy((x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, type='slime')

    def update(self, elapsed_seconds):
        # Update Logic
        self.visible_sprites.update()

    def render(self, surface):
        # Update and draw
        surface.fill(BG_COLOR)
        
        # Custom Draw (Camera)
        self.visible_sprites.custom_draw(surface, self.player)
