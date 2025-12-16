# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
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
