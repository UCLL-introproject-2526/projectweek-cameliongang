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

            elif type == 'N':
                loaded_img=pygame.image.load('./resources/end_gate.png').convert_alpha()

            elif type == 'F':
                loaded_img = pygame.image.load('./resources/spikes_full.png').convert_alpha()
            elif type == 'C':
                loaded_img = pygame.image.load('./resources/spikes_ceiling.png').convert_alpha()
            elif type == 'L':
                loaded_img = pygame.image.load('./resources/spikes_left.png').convert_alpha()
            elif type == 'R':
                loaded_img = pygame.image.load('./resources/spikes_right.png').convert_alpha()

            else: # 'X'
                loaded_img = pygame.image.load('./resources/dirt_block.png').convert_alpha()
            
            # Ensure it fits (just in case)
            # Ensure it fits (just in case)
            if loaded_img:
                self.image = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
            
            # Hitbox Adjustments based on type
            if type == 'Y':
                 # Floor Spikes: 1/4 tile high, full width, at bottom
                 spike_height = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1] + (TILE_SIZE - spike_height), TILE_SIZE, spike_height)
            elif type == 'C':
                 # Ceiling Spikes: 1/4 tile high, full width, at top
                 spike_height = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, spike_height)
            elif type == 'L':
                 # Left Wall Spikes: 1/4 tile wide, full height, at left
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1], spike_width, TILE_SIZE)
            elif type == 'R':
                 # Right Wall Spikes: 1/4 tile wide, full height, at right
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0] + (TILE_SIZE - spike_width), pos[1], spike_width, TILE_SIZE)
            elif type == 'F':
                 # Full Block Spike: Full hitbox (already default), no change needed to rect logic
                 pass
            
        except Exception:
            # Fallback to color rendering
            if type == 'S':
                self.image.fill((0, 255, 0)) # Green for Sticky
                pygame.draw.rect(self.image, (0, 100, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)
            elif type == 'D':
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 self.image.fill((0, 0, 0, 0)) 
            elif type == 'N':
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 self.image.fill((52, 193, 235)) 
            elif type == 'Y':
                 # Floor Spike Visual (Red bottom strip)
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(0, TILE_SIZE - (TILE_SIZE // 4), TILE_SIZE, TILE_SIZE // 4)
                 pygame.draw.rect(self.image, (255, 0, 0), rect_area)
                 # Rect logic handled above
            elif type == 'F':
                 # Full Spike: Red full block
                 self.image.fill((255, 50, 50)) 
                 pygame.draw.rect(self.image, (150, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 3)
            elif type == 'C':
                 # Ceiling Spike: Orange top strip
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE // 4)
                 pygame.draw.rect(self.image, (255, 165, 0), rect_area)
                 
                 # Set Rect for Physics
                 spike_height = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, spike_height)
                 
            elif type == 'L':
                 # Left Spike: Yellow left strip
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(0, 0, TILE_SIZE // 4, TILE_SIZE)
                 pygame.draw.rect(self.image, (255, 255, 0), rect_area)
                 
                 # Set Rect for Physics
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0], pos[1], spike_width, TILE_SIZE)

            elif type == 'R':
                 # Right Spike: Purple right strip
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(TILE_SIZE - (TILE_SIZE // 4), 0, TILE_SIZE // 4, TILE_SIZE)
                 pygame.draw.rect(self.image, (128, 0, 128), rect_area)
                 
                 # Set Rect for Physics
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(pos[0] + (TILE_SIZE - spike_width), pos[1], spike_width, TILE_SIZE)

            else:
                self.image.fill((139, 69, 19)) # Brown
                pygame.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)

LEVEL_1 = [

    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
    "X                 SSSSSS    X ",
    "X                           XE",
    "X P        Y   Y   YYYY     X ",
    "XXXXXS   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXS   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXX   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX  X ",
    "X     G       G     G       X ",
    "X                           X ",
    "X                           X ",
    "X XXXXFFFFFXXXFFFFXXXXFFFFXXX ",
    "X XXXXXXXXXXXXXXXXXXXXXXXXXXX ",
    "X                      E    XE",
    "X                        E  X ",
    "X                     E     XE",
    "XXXXXXXXXXXXXXXXXXXXXXX  XXXX ",
    "XSSSSSSSSSFF          X  XXXX ",
    "X          F          X  XXXX ",
    "X N        SFFFFFFFFFFX  XXXX ",
    "XXXX       S  FSSSSSF X  XXXX ",
    "X          S             XXXX ",
    "X                        XXXX ",
    "X         XXXXXX    S    XXXX ",
    "X                   S    XXXX ",
    "X                   S    XXXX ",
    "X                   X    XXXX ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",


]

LEVEL_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X        SSSS SS          X",
    "X                  S      X",
    "X       S          S      X",
    "X       S          X   S  X",
    "X       S              S  E",
    "X        P             X  E",
    "X      XXXXX        S     X",
    "X    X              XN    X",
    "X    XX      XX     XXX   X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDD"
]



# LEVEL_2 = [
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
#     "XS                                        SX",
#     "XS           G     YYY                    SX",
#     "XS   SSSS        SSSSSS     SSSSSS        SX",
#     "XS   S  S        S    S     S    S        SX",
#     "XS   S  S        S    S     S    S        SX",
#     "XS   S  S  P     S    S     S    S        SX",
#     "XS   S  XXXXXXXXXS    xxxxxxx    S        SX",
#     "XS   S           S     Y         S        SX",
#     "XS   S           S               S        SX",
#     "XS   SSSSSSSSSSSSS               SSSSSS   SX",
#     "XS                                        SX",
#     "XS        SSSXSS           SSSSSS         SX",
#     "XS            NS           S              SX",
#     "XSSSSSSSS      S           S      SSSSSSSSSX",
#     "X       S      S           S      S        X",
#     "X       S      S           S      S        X",
#     "X       XXXXXXXX           XXXXXXXX        X",
#     "X                                          X",
#     "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
# ]


LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
    "XS                                        SX",
    "XS  P                                     SX",
    "XS                                        SX",
    "XSSSSSSS      SSSSSSSS      SSSSSSSS      SX",
    "X     GS      S      S      S      S      SX",
    "N      S      S      S      S      S      SX",
    "X     XS      S      S      S      S      SX",
    "G      SSSSSSSS      SSSSSSSS      SSS  SSSX",
    "X                                          X",
    "X       G          G          G            X",
    "X            S            S            S   X",
    "X            S            S            S   X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]
#LEVEL 4 | advanced grapling
LEVEL_4 = [

    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X           G          G         G         X",
    "X P                                    G   X",
    "X                                          X",
    "XXXXXXS     XXXXXS     XXXXXX              X",
    "X     S     X    S     X    X              X",
    "X     S     X    S     X    X         XXX  X",
    "X     S     X    S     X    XYYYYYYYYYX X  X",
    "X     S     X    S     X    XXXXXXXXXXX X  X",
    "X     S     X    S     X                X  X",
    "X     S     X    S     X                X  X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X",
    "X   G       G       G      G      G        X",
    "X                                          X",
    "X                                          X",
    "X N                                        X",
    "XXXXX    XX     XXX      XX     XXX     XXXX",
    "XXXXXDDDDXXDDDDDXXXDDDDDDXXDDDDDXXXDDDDDXXXX",
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
    "XSSSSSSSS      S           S      SSSSSSSSGX",
    "X       S      S           S      S    G   X",
    "X       S      S           S             N X",
    "X       XXXXXXXX           XXXXXXXX        X",
    "X                                          X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
]


LEVEL_6  = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X     XXXXXXXXXXXXXXXXXX     X",
    "X     XXXXXYYXXXYYYYYYYX     X",
    "X                            X",
    "XXXX                    G    X",
    "XXXX       YY                X",
    "XXXS  XXXXXXXXXXYYYYYYYXXXX  X",
    "XXXX  SXXXXXXXXXXXXXXXXXXXX  X",
    "XXXX  SXXXYYGYYYYYYYYGYYYYY  X",
    "XXXS  XXXX                   X",
    "XXXS  XXXX                   X",
    "XXXX  XXXX   YYYYYY  YYYYY   X",
    "XXXX  SXXX XXXXXXXXXXXXXXXXXXX",
    "XP    XXXX                  NX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]


LEVEL_7 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X    X  G            X                 X",
    "X  N X        G      X  X      X       X",
    "X SXGX                X  X             X",
    "X           XX         X  XY     XS    X",
    "G                 G     X  X      S    X",
    "XXXX                     X  XY    S    X",
    "X                GG  SSS  X  XY   S    X",
    "X      XXX               X    XY  S    X",
    "XYYYYXYYYYYYYYYYYYYYYYYY   XYYYX  S    X",
    "XXXXXGXXXXXXXXXXXXXXXXXXXXXXXXXXXXS    X",
    "X                                 S    X",
    "X                      YYYYYYYY        X",
    "X     XX XXXXXXXXXXX   XXXXXXXX    SSS S",
    "X        X         X   X      X        S",
    "X        X         X   X      X      S X",
    "X   XXS  XXXX   XXXX   XXXXX  X      S X",
    "X     S     X   X          X  X        S",
    "X     G S   X   X          X  X        S",
    "X       S   X   X          X  X        S",
    "X     XXX   X   X          X  X      S X",
    "XG          X   X      XXX X  X      S X",
    "XX          X   X      X X X  X        S",
    "XXX         X   X      X XXX  X        S",
    "X           X   X      X      X      S X",
    "X      G    XXXXX      XXXXXXXX      S X",
    "X                      G     G     G   S",
    "XP                                     S",
    "XXXX             YYYYYYYXYYYYYXYYYYYXXXX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]

LEVEL_8 =  [
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "X           XX           X",
    "S XXXXXXXXXXXX           X",
    "X X         XX           X",
    "X X   P   G XXX          X",
    "S X   S     YY X         X",
    "X  F FS Y       X        X",
    "   F FS S   Y    X       X",
    "X    YS S   XY    X      X",
    "XXXXXXS S   XX     X     X",
    "X     S     SX     X     X",
    "X     S S   SX     X     X",
    "X     XXXXX SX     X     X",
    "X           SX     X     X",
    "X           SXY    X     X",
    "S      G    SX     X     X",
    "X       Y   SX     X     X",
    "X YXXY  Y   SX     X     X",
    "S           XXYY   X     X",
    "S      XXXX XX     X     X",
    "S           XX     X     X",
    "S           XX     X     X",
    "S           XX     X     X",
    "X           XX     X     X",
    "XX          XX     X     X",
    "X X    YGY  XX     X     X",
    "X  X   Y    XX     X     X",
    "X   X       XX     X     X",
    "X    XXX    SX     X     X",
    "X           XX     X     X",
    "X      YYYY SX     X     X",
    "X           XX     X     X",
    "X           SX     X     X",
    "X   G   G   XX     X     X",
    "X           SX     X     X",
    "S           SX     X     X",
    "X           SX     X     X",
    "S           SX     X     X",
    "X           XN     X     X",
    "S           SX     X     X",
    "X           SX     X     X",
    "S G         XX     X     X",
    "X           XX     X     X",
    "S           XX     X     X",
    "X     P     XX     X     X",
    "X    XXX    XX     X     X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDD",
]
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8]

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
        self.has_enemy=False
        self.setup_level()

    def setup_level(self):
        self.tiles = []
        self.enemy_spawns = []
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
                if cell == 'N':
                    self.tiles.append(Tile((x,y),'N'))
                # New Spikes
                if cell == 'F':
                    self.tiles.append(Tile((x,y), 'F'))
                if cell == 'C':
                    self.tiles.append(Tile((x,y), 'C'))
                if cell == 'L':
                    self.tiles.append(Tile((x,y), 'L'))
                if cell == 'R':
                    self.tiles.append(Tile((x,y), 'R'))
                # Enemy Spawns
                if cell == 'E':
                    self.enemy_spawns.append((x, y))
                    self.has_enemy = True
                    print("true enemey")

    def render(self, surface, camera, show_hitboxes=False):
        for tile in self.tiles:
            shifted_rect = camera.apply_rect(tile.rect)
            if tile.type == 'Y':
                 # Visual fix: The hitbox is bottom 1/4 (16px), but image is full 64px.
                 # Shift rendering UP by 48px to align visual bottom with hitbox bottom.
                 shifted_rect.y -= 48 
            if tile.type == 'R':
                 # Visual fix: Hitbox is right 1/4 (shifted +48), but image is full 64px.
                 # Shift rendering LEFT by 48px to align visual right with hitbox right.
                 shifted_rect.x -= 48
            surface.blit(tile.image, shifted_rect)
            
            # DEBUG: Draw Hitboxes
            if show_hitboxes:
                pygame.draw.rect(surface, (255, 0, 0), camera.apply_rect(tile.rect), 1)