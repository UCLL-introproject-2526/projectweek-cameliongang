import pygame
TILE_SIZE = 64

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type='X'):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.type = type
        self.rect = self.image.get_rect(topleft=pos)
        
        # Try loading sprite based on type
        try:
            if type == 'S':
                loaded_img = pygame.image.load('./resources/slime_block.png').convert_alpha()
            else: # 'X'
                loaded_img = pygame.image.load('./resources/dirt_block.png').convert_alpha()
            
            # Ensure it fits (just in case)
            self.image = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
            
        except Exception:
            # Fallback to color rendering
            # Fallback to color rendering
            if type == 'S':
                self.image.fill((0, 255, 0)) # Green for Sticky
                pygame.draw.rect(self.image, (0, 100, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
            elif type == 'D':
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 self.image.fill((0, 0, 0, 0)) # Invisible
            else:
                self.image.fill((139, 69, 19)) # Brown
                pygame.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)


# HUIDIG LEVEL (COMMENTEER DIT UIT OM HET NIEUWE LEVEL TE SPELEN)
# LEVEL_MAP = [
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "X        SSSS SS          X",
#     "X                  S      X",
#     "X       S          S      X",
#     "X       S          X   S  X",
#     "X       S              S  X",
#     "X        P             X  X",
#     "X      XXXXX        S     X",
#     "X    X              X     X",
#     "X    XX      XX     XXX   X",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "DDDDDDDDDDDDDDDDDDDDDDDDDDD"
# ]

# LEVEL 3: DE TOREN (VERTICALE KLIM)
LEVEL_MAP = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XSSSSSSSSSSSSS SSSSSSSSSSSSX",
    "XS                        SX",
    "XS     P                  SX",
    "XS    XXX                 SX",
    "XS                        SX",
    "XS                        SX",
    "XS                        SX",
    "XS                        SX",
    "XS                        SX",
    "XS                        SX",
    "XS                        SX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDD"
]

# LEVEL 4: ONDERSTEBOVEN (PLAFOND PARCOURS)
# LEVEL_MAP = [
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
#     "XS                                        SX",
#     "XS  P                                     SX",
#     "XS                                        SX",
#     "XSSSSSSS      SSSSSSSS      SSSSSSSS      SX",
#     "X      S      S      S      S      S      SX",
#     "X      S      S      S      S      S      SX",
#     "X      S      S      S      S      S      SX",
#     "X      SSSSSSSS      SSSSSSSS      SSSSSSSSX",
#     "X                                          X",
#     "X                                          X",
#     "X            S            S            S   X",
#     "X            S            S            S   X",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# ]


# NIEUW "EXTRA FUN" LEVEL (UNCOMMENT DIT OM TE SPELEN)
# LEVEL_MAP = [
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
#     "XS                                        SX",
#     "XS                                        SX",
#     "XS   SSSS        SSSSSS     SSSSSS        SX",
#     "XS   S  S        S    S     S    S        SX",
#     "XS   S  S        S    S     S    S        SX",
#     "XS   S  S  P     S    S     S    S        SX",
#     "XS   S  XXXXXXXXXS    xxxxxxx    S        SX",
#     "XS   S           S               S        SX",
#     "XS   S           S               S        SX",
#     "XS   SSSSSSSSSSSSS               SSSSSS   SX",
#     "XS                                        SX",
#     "XS        SSSSSS           SSSSSS         SX",
#     "XS             S           S              SX",
#     "XSSSSSSSS      S           S      SSSSSSSSSX",
#     "X       S      S           S      S        X",
#     "X       S      S           S      S        X",
#     "X       XXXXXXXX           XXXXXXXX        X",
#     "X                                          X",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# ]


LEVEL_WIDTH = len(LEVEL_MAP[0]) * TILE_SIZE
# Exclude the last row (death zone) from the camera height
LEVEL_HEIGHT = (len(LEVEL_MAP) - 1) * TILE_SIZE

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
                if cell == 'D':
                     self.tiles.append(Tile((x, y), 'D'))
                if cell == 'P':
                    self.player_start_pos = (x, y)

    def render(self, surface, camera):
        for tile in self.tiles:
            # Simple Optimization: Only draw if visible (camera interaction)
            # The apply() check effectively does this if we trust Pygame's blit clipping,
            # but we need to shift the rect.
            tile_rect_shifted = camera.apply(tile.rect)
            surface.blit(tile.image, tile_rect_shifted)