import pygame
from pygame.display import flip
from time import sleep
import sys

# Initialize Pygame
pygame.init()

class Keys:
    def __init__(self):
        self.speed = 200

        self.move_left = pygame.K_q
        self.move_right = pygame.K_d
        self.move_up = pygame.K_z
        self.move_down = pygame.K_s
 

class State:
    def __init__(self):
        self.x_circle = 500
        self.y_circle = 500

        self.camelion_img = pygame.image.load(
            "./resources/camelion.png"
        ).convert_alpha()

        self.camelion_img = pygame.transform.scale(
            self.camelion_img,
            (
                self.camelion_img.get_width() // 2,
                self.camelion_img.get_height() // 2
            )
        )

    def update_pos_x(self, x):
        self.x_circle += x

    def update_pos_y(self, y):
        self.y_circle += y

    def render(self, surface):
        surface.blit(self.camelion_img, (self.x_circle, self.y_circle))

    def background(self):
        background = pygame.image.load(".\\resources\\background_img.jpg").convert()
        background = pygame.transform.scale(background, (1280, 720))


class Mines:
    def __init__(self):
        self.location=50

    def update_location(self, x):
        self.location+=2

    








# Tuple representing width and height in pixels
def create_main_surface():
    screen_size = (1280, 720)
    # Create window with given size
    return pygame.display.set_mode(screen_size)



def main():
    surface = create_main_surface()
    pos_state = State()
     # Load background image
    background = pygame.image.load(".\\resources\\background_img.jpg").convert()
    background = pygame.transform.scale(background, (1280, 720))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        surface.fill((0, 0, 0))      # clear screen
        pos_state.render(surface)   # draw sprite

      # Draw background first
        surface.blit(background, (0, 0))

        # Draw sprite on top
        pos_state.render(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pos_state.update_pos_y(-10)
        if keys[pygame.K_DOWN]:
            pos_state.update_pos_y(10)
        if keys[pygame.K_LEFT]:
            pos_state.update_pos_x(-10)
        if keys[pygame.K_RIGHT]:
            pos_state.update_pos_x(10)

        pygame.display.flip()


                

if __name__ == "__main__":
    main()