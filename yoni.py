import pygame

def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)

def render_frame(surface,x):
    clear_surface(surface)
    pygame.draw.circle(surface, (255, 0, 0), (x, 200), 200)
    pygame.display.flip()

def clear_surface(surface):
    surface.fill((0, 0, 0))

class state:
    def __init__(self):
        self.xcoor = 0

    def xcoor_update(self, x):
        self.xcoor += x
    
    def render(self, surface):
        clear_surface(surface)
        pygame.draw.circle(surface, (255, 0, 0), (self.xcoor, 200), 200)
        pygame.display.flip()


def main():
    #initialization
    pygame.init()
    x = 0
    surface = create_main_surface()
    clock = pygame.time.Clock()
    status = state()
    while True:
        status.render(surface)
        status.xcoor_update(2)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        









if __name__ == "__main__":
    main()