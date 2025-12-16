# Ref: http://projectweek.leone.ucll.be/reference/python/clean-code/index.html#no-magic-constants

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
# Aliases for compatibility
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT

TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (30, 30, 30)
TONGUE_COLOR = (255, 100, 100)

# UI Colors (Ref: Clean Code - No Magic Numbers)
HUD_BG_COLOR = (50, 50, 50)
HUD_BORDER_COLOR = (200, 200, 200)
TEXT_COLOR = WHITE
TITLE_COLOR = (100, 255, 100)
INFO_COLOR = (150, 150, 150)
POWER_TEXT_COLOR_FIRE = (255, 100, 100)
POWER_TEXT_COLOR_STICKY = (100, 255, 100)
POWER_TEXT_COLOR_NONE = (200, 200, 200)
LOADING_TEXT_COLOR = WHITE

# UI Layout
HUD_POS = (10, 10)
HUD_SIZE = (150, 70)
HUD_BORDER_RADIUS = 10
HUD_BORDER_WIDTH = 3

# Physics
GRAVITY = 1.0       # Increased from 0.8 for weight
JUMP_STRENGTH = -18 # Increased from -16 to match gravity
TERMINAL_VELOCITY = 18 # Higher fall speed
FRICTION = 0.6      # Less friction for more slide (was 0.8) -> actually 0.6 makes it SLIPPERY. Higher is more grip. 0.8 is fine. Let's try 0.9 for tighter control.
FRICTION = 0.5      # Wait, velocity *= friction? No, velocity -= friction in my code.
                    # My code: velocity.x -= FRICTION. 
                    # If FRICTION is 0.8, it subtracts 0.8 per frame.
                    # ACCELERATION is 1.2.
                    # Max speed was 8.
                    # Let's make acceleration 1.5 and Friction 0.8.
ACCELERATION = 1.0 # Tighter
FRICTION = 0.5

# Tongue
TONGUE_SPEED = 25   # Faster shot
TONGUE_LENGTH = 500 # Longer range
PULL_SPEED = 2.0    # Faster pull
