import pygame
from pygame.display import flip
from time import sleep

# Initialize Pygame
pygame.init()


class State:
    def __init__(self):
        self.x_circle = 0

    def update_pos(self, x):
        self.x_circle+=x

    def render_frame(self, surface):
        pygame.draw.rect(surface, (0,0,0,),(0,0,1024,768),)
        pygame.draw.circle(surface, (155, 111, 111), (self.x_circle, 200), 50)
        flip()


# Tuple representing width and height in pixels

def create_main_surface():
    screen_size = (1024, 768)
    # Create window with given size
    return pygame.display.set_mode(screen_size)

def main():
    pos_state=State()
    pos_state.x_circle = 500
    
    clock = pygame.time.Clock()
    speed = 200   # pixles per seconde
    
    surface = create_main_surface()
    
    while True:
        dt = clock.tick(60)/1000 #seconds per frame

        pos_state.render_frame(surface)
        pos_state.update_pos(speed * dt)
        
        # Basic event handling to keep the window responsive (best practice)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

if __name__ == "__main__":
    main()