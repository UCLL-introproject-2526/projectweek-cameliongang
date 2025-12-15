import pygame
from pygame.display import flip

# Initialize Pygame
pygame.init()

# Tuple representing width and height in pixels

def create_main_surface():
    screen_size = (1024, 768)
    # Create window with given size
    return pygame.display.set_mode(screen_size)

def render_frame(surface):
    # Draw a circle
    # Parameters: surface, color, center, radius
    pygame.draw.circle(surface, (255, 0, 0), (200, 200), 50)
    flip()

def main():
    surface = create_main_surface()
    
    while True:
        render_frame(surface)

        # Basic event handling to keep the window responsive (best practice)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

if __name__ == "__main__":
    main()
