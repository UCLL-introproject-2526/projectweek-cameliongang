import pygame
TILE_SIZE = 64
SPIKE_PADDING = 10 # Controls how much smaller the spike hitbox is (pixels removed from sides)
IMAGE_CACHE = {}

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type='X'):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.type = type
        self.rect = self.image.get_rect(topleft=pos)
        self.grappleable = (type== 'G')
        self.grappleable = (type== 'G')
        self.pos = pos
        
        # Check cache first
        if type in IMAGE_CACHE:
             self.image = IMAGE_CACHE[type]
        else:
            self._load_image_and_cache(type)
        
        self.image = IMAGE_CACHE.get(type, self.image)

        # Apply Hitbox Adjustments based on type
        self._apply_hitbox(type, pos)

    def _apply_hitbox(self, type, pos):
        # Hitbox Adjustments based on type
        # HITBOX ADJUSTMENTS: Reduced width/height to be "less wide" (more forgiving)
        # SPIKE_PADDING is defined at top of file
        
        if type == 'Y':
                # Floor Spikes: 1/4 tile high, full width (minus padding), at bottom
                spike_height = TILE_SIZE // 4
                # Rect: x+padding, y+offset, width-2*padding, height
                self.rect = pygame.Rect(pos[0] + SPIKE_PADDING, pos[1] + (TILE_SIZE - spike_height), TILE_SIZE - (2*SPIKE_PADDING), spike_height)
        elif type == 'C':
                # Ceiling Spikes: 1/4 tile high, full width (minus padding), at top
                spike_height = TILE_SIZE // 4
                self.rect = pygame.Rect(pos[0] + SPIKE_PADDING, pos[1], TILE_SIZE - (2*SPIKE_PADDING), spike_height)
        elif type == 'L':
                # Left Wall Spikes: 1/4 tile wide, full height (minus padding), at left
                spike_width = TILE_SIZE // 4
                self.rect = pygame.Rect(pos[0], pos[1] + SPIKE_PADDING, spike_width, TILE_SIZE - (2*SPIKE_PADDING))
        elif type == 'R':
                # Right Wall Spikes: 1/4 tile wide, full height (minus padding), at right
                spike_width = TILE_SIZE // 4
                # Note: Corrected x position logic to match visual
                self.rect = pygame.Rect(pos[0] + (TILE_SIZE - spike_width), pos[1] + SPIKE_PADDING, spike_width, TILE_SIZE - (2*SPIKE_PADDING))
        elif type == 'F':
                # Full Block Spike: Add padding on all sides
                self.rect = pygame.Rect(pos[0] + SPIKE_PADDING, pos[1] + SPIKE_PADDING, TILE_SIZE - (2*SPIKE_PADDING), TILE_SIZE - (2*SPIKE_PADDING))
        
    def _load_image_and_cache(self, type):
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
            if loaded_img:
                self.image = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
                IMAGE_CACHE[type] = self.image

        except Exception:
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
                 self.rect = pygame.Rect(self.pos[0], self.pos[1], TILE_SIZE, spike_height)
                 
            elif type == 'L':
                 # Left Spike: Yellow left strip
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(0, 0, TILE_SIZE // 4, TILE_SIZE)
                 pygame.draw.rect(self.image, (255, 255, 0), rect_area)
                 
                 # Set Rect for Physics
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(self.pos[0], self.pos[1], spike_width, TILE_SIZE)

            elif type == 'R':
                 # Right Spike: Purple right strip
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                 rect_area = pygame.Rect(TILE_SIZE - (TILE_SIZE // 4), 0, TILE_SIZE // 4, TILE_SIZE)
                 pygame.draw.rect(self.image, (128, 0, 128), rect_area)
                 
                 # Set Rect for Physics
                 spike_width = TILE_SIZE // 4
                 self.rect = pygame.Rect(self.pos[0] + (TILE_SIZE - spike_width), self.pos[1], spike_width, TILE_SIZE)

            else:
                self.image.fill((139, 69, 19)) # Brown
                pygame.draw.rect(self.image, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 2)

# LEVEL_0 = [
#     "                              ",
#     "                              ",
#     "                              ",
#     "                              ",
#     "                              ",
#     "                              ",
#     "                              ",
#     "X              S              ",
#     "X              S         G    ",
#     "X              S              ",
#     "X              S         XXXX ",
#     "X              S         CCCC ",
#     "X          Y   XL  F          ",
#     "XXXXXXX  XXXXXXXXXXXXXXXX     ",
#     "                              ",
#     "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
# ]

LEVEL_1 =  [
    #tutorial-level
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
    "X                 SSSSSS    X ",
    "X                           X",
    "X P        Y   Y   YYYY     X ",
    "XXXXXS   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXS   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXX   XXXXXXXXXXXXXXXXX  X ",
    "XXXXXXXXXXXXGXXXXXXXXXXXXX  X ",
    "X                   G       X ",
    "X                           X ",
    "X                           X ",
    "X XXXXXXXXXFFFFFXXXXXXFFFFXXX ",
    "X XXXXXXXXXXXXXXXXXXXXXXXXXXX ",
    "X                        E  XE",
    "X                         E  X ",
    "X                           XE",
    "XXXXXXXXXXXXXXXXXXXXXXX  XXXX ",
    "XSSSSSSSSSSSSSSSSSXXXXX  XXXX ",
    "X N                XXXX  XXXX ",
    "XXXX               SXXX  XXXX ",
    "X                  SXXX  XXXX ",
    "X      S  XXXXXXX        XXXX ",
    "X      S                 XXXX ",
    "X      S                 XXXX ",
    "X         XXXXXXXX  S    XXXX ",
    "X                   S    XXXX ",
    "X                   S    XXXX ",
    "X                   X    XXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]

LEVEL_2 = [
   
    "                                         SX ",
    "    N               G     G              SX ",
    "   XXX                                   SX ",
    "        XXX                      YY  YY  SX ",
    "             X                   XXXXXX  SX ",
    "YYYYYYYYYYYYYXX    YYYYY  YYYYYYX        SX ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         SX ",
    "X            SSSS SS                     SX ",
    "X       G              S              S   X ",
    "X           S          S    XX  XXXX  S   X ",
    "S           S          S              S   X ",
    "S  XXX      S                             X ",
    "S                    G         YY        YX ",
    "S          XXXXX        S   S XXXX Y  Y XXXE",
    "X  P     X              S   S      XXXX   XE",
    "X XXX    XX   XXXXX   X S                 X ",
    "XDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDX ",
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
    "NNNNNNNNNNX        XNNNNNNNNNN",
    "NNNNNNNNNNX        XNNNNNNNNNN",
    "NNNNNNNNNNX     G  XNNNNNNNNNN",
    "NNNNNNNNNNX  N     SNNNNNNNNNN",
    "NNNNNNNNNNX XXXX   XNNNNNNNNNN",
    "NNNNNNNNNNX        XNNNNNNNNNN",
    "NNNNNNNNNNX        XNNNNNNNNNN",
    "NNNNNNNNNNX        SNNNNNNNNNN",
    "NNNNNNNNNNX P      FNNNNNNNNNN",
    "NNNNNNNNNNXXXXXXXXXXNNNNNNNNNN",
    "NNNNNNNNNNDDDDDDDDDDNNNNNNNNNN",
]


#  "XXXXXXXXXXXXXXGXXXXXXXXXGXXXXGXXXXXXXXXXXXX       ",
#     "X                CXXX                     XE   E  ",
#     "X                 CXX                     X E     ",
#     "X P                CS                     X      E",
#     "XXXX  Y  YYY    YY  S       XXXXXXXXXXX   X       ",
#     "XXXXYYXXXXXXYYYXXX  S       XXXXXGXXXXX   X       ",
#     "XXXXXXXGXXXXXXXX    S       XS            X       ",
#     "S                   S    YYYXS            X       ",
#     "S                   SY  XXXXXS         XXXX       ",
#     "S   XXY             SX     XXS            X       ",
#     "S   CCFY         F  SXXL  YXX             X       ",
#     "S     CFYY      FFFYXXC   XXX  XXX        X       ",
#     "S Y    CXXXXXXXXXXXXXC  YXXXX             X       ",
#     "SYFY                    XXXXX             X    E  ",
#     "SFFF                  YXXXXXX             X   E   ",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       ",
#     "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD       ",
# ]


#LEVEL 4 | advanced grapling
LEVEL_4 =  [
   
    "XXXXXXXXGXXXXGXXXXGXXXXGXXXXGXXXXGXXXXXXXXXX",
    "X                                     G    X",
    "X P                                        X",
    "X                                          X",
    "XXXXX       XXXX       XX                  X",
    "X  XXYYYYYYYX  XYYYYYYYXX                  X",
    "X  XXXXXXXXXX  XXXXXXXXXX             XXX  X",
    "X                      XXYYYYYYYYYYYYYX X  X",
    "X                      XXXXXXXXXXXXXXXX X  X",
    "X                      X                X  X",
    "X                      X                X  X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X",
    "X   G       G       G      G      G        X",
    "X                                          X",
    "X                                          X",
    "X N                                        X",
    "XXXXX                                   XXXX",
    "XXXXXDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDXXXX",
]





LEVEL_5 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSXXXXXX",
    "XX                             E E EE XEEXXX",
    "XX           YYYYYYYYYYYYYYY    E  E EXEXEXX",
    "XXXXXXXXX    XXXXXXXXXXXXXXXXXXXXX    XXXXXX",
    "XX      S    XXXXXXXXXXXG             XXXXXX",
    "XS   G  S    XXXXXXG                XXXXXXXX",
    "XS      X  P XXG               XXXXXXXX   XX",
    "XS      XXXXXXX       x xxxxx XX          XX",
    "XS      SSSSSSS        YYYYYYXX           XX",
    "XS                   YYXXXXXXX    XXXXX   XX",
    "XS  YYY  YYYYY  YYYYYXXXXXG      XXC      XX",
    "XS  XXXXXXXXXXXXXXXXXXXX        XXG      YXX",
    "XS  XXXXXXXX      G   G     XXXXXC      YXXX",
    "XS  CCCCCCCC             YYXXC        YYXXXX",
    "XS            X          XXXC     XXXXXXXXGX",
    "XX   Y  Y  Y XX         XXXX   XXXX    G   X",
    "XXXXXXXXXXXXXXX        XXXXXY            N X",
    "XXXXXXXXXXXXXXX        XXXXXXY             X",
    "XXXXXXXXXXXXXXX        XXXXXXXXXXXXX       X",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]


LEVEL_6  = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X     XXXXXXXXXXXXXXXXXX     X",
    "X     XXXXXYYXXXYYYYYYYX     X",
    "X                            X",
    "XXXX                    G    X",
    "XXXS       YY                X",
    "XXXS  XXXXXXXXXXYYYYYYYXXXX  X",
    "XXXX  SXXXXXXXXXXXXXXXXXXXX  X",
    "XXXX  SXXXYYGYYYYYYYYGYYYYY  X",
    "XXXS  XXXX                   X",
    "XXXS  XXXX                   X",
    "XXXX  SXXX   YYYYYY  YYYYY   X",
    "XXXX  SXXX XXXXXXXXXXXXXXXXXXX",
    "XP    XXXX                  NX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]


LEVEL_7 = [
    "XXXXXX               XX                X",
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
    "X       X   X   X          X  X        S",
    "X     XXX   X   X          X  X      S X",
    "XG          X   X      XXX X  X      S X",
    "XX          X   X      X X X  X        S",
    "XXX         X   X      X XXX  X        S",
    "X           X   X      X      X      S X",
    "X      G    XXXXX      XXXXXXXX      S X",
    "X                      G     G     G   S",
    "XP                                     X",
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
    "X  X   C    XX     X     X",
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


LEVEL_9 = [
    

    "XXXXXXXXXXXXXXGXXXXXXXXXGXXXXGXXXXGXXXXGXXX       ",
    "X                CXXX                     XE   E  ",
    "X                 CXX                     X E     ",
    "X P                CS                     X      E",
    "XXXX  Y  YYY    YY  S          YYYY       X       ",
    "XXXXYYXXXXXXYYYXXX  S       YXXXXXXXXXX   X       ",
    "XXXXXXXGXXXXXXXXC   S       XXXXXGXXXXX   X       ",
    "S                   S    YYYXXXC          X       ",
    "S                   SY  XXXXXXC           X       ",
    "S   XXY             SX     XXC         XXXX       ",
    "S    CFY         F  SXXL  YXX             X       ",
    "S     CFYY      FFFYXXC   XXX   N         X       ",
    "S Y    CXXXXXXXXXXXXXC  YXXXXYYXXXYYYYYYYYX       ",
    "SYFY                    XXXXXXXXXXXXXXXXXXX    E  ",
    "SFFF                  YXXXXXXXXXXXXXXXXXXXX   E   ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       ",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD       ",
]
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9]

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

    def render(self, surface, camera, show_hitboxes=False):
        for tile in self.tiles:
            # Use original position for rendering images to ensure they are aligned with grid/visuals
            # and not shifted by hitbox padding.
            render_rect = pygame.Rect(tile.pos[0], tile.pos[1], TILE_SIZE, TILE_SIZE)
            shifted_rect = camera.apply_rect(render_rect)
            
            # Previous manual offsets (y-=48, x-=48) are no longer needed because 
            # we are rendering from the top-left of the tile grid cell (pos),
            # and the images are 64x64.
            
            surface.blit(tile.image, shifted_rect)
            
            # DEBUG: Draw Hitboxes
            if show_hitboxes:
                pygame.draw.rect(surface, (255, 0, 0), camera.apply_rect(tile.rect), 1)
    

    def find_pixel_loc(tile_x, tile_y):
        pixel_x = tile_x * TILE_SIZE
        pixel_y = tile_y * TILE_SIZE
        print(f"you want pixel_x: {pixel_x} and pixel_y: {pixel_y}")
    
    find_pixel_loc(2,1)

    


    
