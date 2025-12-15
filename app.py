import pygame
from pygame.display import flip
from time import sleep

# Initialize Pygame
pygame.init()


class State






# Tuple representing width and height in pixels

def create_main_surface():
    screen_size = (1024, 768)
    # Create window with given size
    return pygame.display.set_mode(screen_size)

def render_frame(surface,x_circle):
    # Draw a circle
    
    
    # Parameters: surface, color, center, radius
    pygame.draw.circle(surface, (155, 111, 111), (x_circle, 200), 50)
    flip()


def clear_surface(surface):
    pygame.draw.rect(surface, (0,0,0,),(0,0,1024,768),)


def main():
    clock = pygame.time.Clock()
    x_circle = 500
    speed = 101   # pixles per seconde
    surface = create_main_surface()
    
    while True:
        dt = clock.tick(60)/1000
        render_frame(surface, x_circle)
        x_circle+=speed * dt
        sleep(0.016)
        clear_surface(surface)
        # Basic event handling to keep the window responsive (best practice)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

if __name__ == "__main__":
    main()