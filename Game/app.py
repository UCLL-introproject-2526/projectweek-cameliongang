import pygame
from pygame.display import flip
from time import sleep

pygame.init()

def create_main_surface():
    return pygame.display.set_mode((1280, 720))

def main():
    pygame.init()
    screen = create_main_surface()
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60) / 1000.0 # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()