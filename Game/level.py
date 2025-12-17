import pygame
TILE_SIZE = 64

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type='X'):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.type = type
        self.rect = self.image.get_rect(topleft=pos)
        self.grappleable = (type== 'G')
        self.pos = pos
        # Try loading sprite based on type
        try:
            if type == 'S':
                loaded_img = pygame.image.load('./resources/slime_block.png').convert_alpha()
            elif type == 'Y':
                loaded_img = pygame.image.load('./resources/spikes.png').convert_alpha()
                # Update collision rect for Y here as well? No, rect is logic, image is visual.
                # But image loading is shared.
            elif type == 'D':
                # Death zone should be invisible or specific?
                # If we want invisible, don't load image.
                raise Exception("Invisible") # Trigger fallback to create empty surface
            elif type == 'G':
                loaded_img = pygame.image.load('./resources\grapple_block.png').convert_alpha()
            else: # 'X'
                loaded_img = pygame.image.load('./resources/dirt_block.png').convert_alpha()
            
            # Ensure it fits (just in case)
            self.image = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
            
            if type == 'Y':
                 # Spikes: 1/4 tile high, full width hitbox
                 spike_height = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1] + (TILE_SIZE - spike_height), TILE_SIZE, spike_height)
            
        except Exception:
            # Fallback to color rendering
            # Fallback to color rendering
            if type == 'S':
                self.image.fill((0, 255, 0)) # Green for Sticky
                pygame.draw.rect(self.image, (0, 100, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
            elif type == 'D':
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 self.image.fill((0, 0, 0, 0)) # Invisible
        
            elif type == 'Y':
                 # Spikes: 1/4 tile high, full width
                 try:
                     self.image = pygame.image.load(r".\resources\spikes.png").convert_alpha()
                     self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                 except:
                     # Fallback if image fails
                     self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                     rect_area = pygame.Rect(0, TILE_SIZE - (TILE_SIZE // 4), TILE_SIZE, TILE_SIZE // 4)
                     pygame.draw.rect(self.image, (255, 0, 0), rect_area) # Red

                 # Update the physics rect to match the visual spike area (bottom 1/4)
                 spike_height = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1] + (TILE_SIZE - spike_height), TILE_SIZE, spike_height)
                 return # Return early because self.rect is already set correctly


            else:
                self.image.fill((139, 69, 19)) # Brown
                pygame.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)

# HUIDIG LEVEL (COMMENTEER DIT UIT OM HET NIEUWE LEVEL TE SPELEN)
LEVEL_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X        SSSS SS          X",
    "X                  S      X",
    "X       S          S      X",
    "X       S          X   S  X",
    "X       S              S  X",
    "X        P             X  X",
    "X      XXXXX        S     X",
    "X    X              X     X",
    "X    XX      XX     XXX   X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDD"
]

# LEVEL 3: DE TOREN (VERTICALE KLIM)
LEVEL_2 = [
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
LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
    "XS                                        SX",
    "XS  P                                     SX",
    "XS                                        SX",
    "XSSSSSSS      SSSSSSSS      SSSSSSSS      SX",
    "X      S      S      S      S      S      SX",
    "X      S      S      S      S      S      SX",
    "X      S      S      S      S      S      SX",
    "X      SSSSSSSS      SSSSSSSS      SSSSSSSSX",
    "X                                          X",
    "X                                          X",
    "X            S            S            S   X",
    "X            S            S            S   X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]


# NIEUW "EXTRA FUN" LEVEL (UNCOMMENT DIT OM TE SPELEN)
LEVEL_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
    "XS                                        SX",
    "XS           G     YYY                    SX",
    "XS   SSSS        SSSSSS     SSSSSS        SX",
    "XS   S  S        S    S     S    S        SX",
    "XS   S  S        S    S     S    S        SX",
    "XS   S  S  P     S    S     S    S        SX",
    "XS   S  XXXXXXXXXS    xxxxxxx    S        SX",
    "XS   S           S     Y         S        SX",
    "XS   S           S               S        SX",
    "XS   SSSSSSSSSSSSS               SSSSSS   SX",
    "XS                                        SX",
    "XS        SSSSSS           SSSSSS         SX",
    "XS             S           S              SX",
    "XSSSSSSSS      S           S      SSSSSSSSSX",
    "X       S      S           S      S        X",
    "X       S      S           S      S        X",
    "X       XXXXXXXX           XXXXXXXX        X",
    "X                                          X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
]

LEVEL_5 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
    "XS                                        SX",
    "XS           GGGGGGGG    YYY              SX",
    "XS   SSSS        SSSSSS     SSSSSS        SX",
    "XS   S  S        S    S     S    S        SX",
    "XS   S  S        S    S     S    S        SX",
    "XS   S  S  P     S    S     S    S        SX",
    "XS   S  XXXXXXXXXS    xxxxxxx    S        SX",
    "XS   S           S     Y         S        SX",
    "XS   S           S               S        SX",
    "XS   SSSSSSSSSSSSS               SSSSSS   SX",
    "XS                                        SX",
    "XS        SSSSSS           SSSSSS         SX",
    "XS             S           S              SX",
    "XSSSSSSSS      S           S      SSSSSSSSSX",
    "X       S      S           S      S        X",
    "X       S      S           S      S        X",
    "X       XXXXXXXX           XXXXXXXX        X",
    "X                                          X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
]

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]

# Default width/height based on first level (or dynamic per level load)
# But StandardUse uses this constant... we might need to update that too if levels vary significantly?
# For now, let's keep them dynamic in the class but these global constants might be tricky.
# We'll rely on the loaded level's dimensions.
LEVEL_WIDTH = len(LEVELS[0][0]) * TILE_SIZE
LEVEL_HEIGHT = (len(LEVELS[0]) - 1) * TILE_SIZE

class Level:
    def __init__(self, level_index=0):
        self.tiles = []
        self.player_start_pos = (100, 100) # Default
        self.current_map = LEVELS[level_index]
        # Update globals/instance vars for this specific level
        global LEVEL_WIDTH, LEVEL_HEIGHT
        LEVEL_WIDTH = len(self.current_map[0]) * TILE_SIZE
        LEVEL_HEIGHT = (len(self.current_map) - 1) * TILE_SIZE
        self.setup_level()

    def setup_level(self):
        self.tiles = []
        for row_index, row in enumerate(self.current_map):
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
                if cell == 'G':
                    self.tiles.append(Tile((x,y), 'G'))
                if cell == 'Y':
                    self.tiles.append(Tile((x,y), 'Y'))

    def render(self, surface, camera):
        for tile in self.tiles:
            shifted_rect = camera.apply_rect(tile.rect)
            if tile.type == 'Y':
                 # Visual fix: The hitbox is bottom 1/4 (16px), but image is full 64px.
                 # Shift rendering UP by 48px to align visual bottom with hitbox bottom.
                 shifted_rect.y -= 48 
            surface.blit(tile.image, shifted_rect)