import pygame
from pygame.display import flip
from time import sleep

# Initialize Pygame
pygame.init()


class State:
    def __init__(self):
        self.x_circle = 0
        self.y_circle = 0

    def update_pos_x(self, x):
        self.x_circle+=x

    def update_pos_y(self, y):
        self.y_circle +=y
        

    def render_frame(self, surface):
        pygame.draw.rect(surface, (0,0,0,),(0,0,1024,768),)
        pygame.draw.circle(surface, (155, 111, 111), (self.x_circle, self.y_circle), 50)
        flip()


class Background:
    def __init__(self):
        self.__image = self.__create_image()

    def __create_image(self):
        # Load the background image
        return pygame.image.load("background.jpg").convert()



# Tuple representing width and height in pixels
def create_main_surface():
    screen_size = (1024, 768)
    # Create window with given size
    return pygame.display.set_mode(screen_size)

def main():
    pos_state=State()
    pos_state.x_circle = 500
    pos_state.y_circle = 500
    
    clock = pygame.time.Clock()
    speed = 200   # pixles per seconde
    
    surface = create_main_surface()
    
    while True:
        dt = clock.tick(60)/1000 #seconds per frame

        pos_state.render_frame(surface)
        #
        

        
        # Basic event handling to keep the window responsive (best practice)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        # Check pressed keys outside the event loop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:          # ⬆️ Up arrow key
            pos_state.update_pos_y(-10)
        if keys[pygame.K_DOWN]:        # ⬇️ Down arrow key
            pos_state.update_pos_y(10)
        if keys[pygame.K_LEFT]:          # ⬆️ Up arrow key
            pos_state.update_pos_x(-10)
        if keys[pygame.K_RIGHT]:        # ⬇️ Down arrow key
            pos_state.update_pos_x(10)
                

if __name__ == "__main__":
    main()