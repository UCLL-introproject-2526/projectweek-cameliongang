import os

# Base Directory Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

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
GRAVITY = 1.0       
JUMP_STRENGTH = -18 
TERMINAL_VELOCITY = 18 
ACCELERATION = 1.0 
FRICTION = 0.5

# Tongue
TONGUE_SPEED = 25   
TONGUE_LENGTH = 500 
PULL_SPEED = 2.0    
