import pygame
TILE_SIZE = 64

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type='X'):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.type = type
        if type == 'S':
            self.image.fill((0, 255, 0)) # Green for Sticky
            pygame.draw.rect(self.image, (0, 100, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        else:
            self.image.fill((139, 69, 19)) # Brown
            pygame.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        self.rect = self.image.get_rect(topleft=pos)

LEVEL_MAP = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X        SSSS SS          X",
    "X                         X",
    "X       S                 X",
    "X       S                 X",
    "X       S                 X",
    "X        P                X",
    "X      XXXXX              X",
    "X    X                    X",
    "X    XX      XX     XXX   X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

LEVEL_WIDTH = len(LEVEL_MAP[0]) * TILE_SIZE
LEVEL_HEIGHT = len(LEVEL_MAP) * TILE_SIZE

class Level:
    def __init__(self):
        self.tiles = []
        self.player_start_pos = (100, 100) # Default
        self.setup_level()

    def setup_level(self):
        self.tiles = []
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    self.tiles.append(Tile((x, y), 'X'))
                if cell == 'S':
                     self.tiles.append(Tile((x, y), 'S'))
                if cell == 'P':
                    self.player_start_pos = (x, y)

    def render(self, surface, camera):
        for tile in self.tiles:
            # Simple Optimization: Only draw if visible (camera interaction)
            # The apply() check effectively does this if we trust Pygame's blit clipping,
            # but we need to shift the rect.
            tile_rect_shifted = camera.apply(tile.rect)
            surface.blit(tile.image, tile_rect_shifted)