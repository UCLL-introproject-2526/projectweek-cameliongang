import pygame, sys

def create_main_surface():
    return pygame.display.set_mode((1280, 720))

class Game:
    def __init__(self):
        pygame.init()
        self.surface = create_main_surface()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chameleon Platformer")

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        pass # Logic goes here later

    def render(self, surface):
        surface.fill((30, 30, 30))
        pygame.display.update()

    def run(self):
        while True:
            # Get milliseconds since last frame, convert to seconds
            dt = self.clock.tick(60) / 1000.0 
            
            self.process_input()
            self.update(dt)
            self.render(self.surface)

if __name__ == '__main__':
    game = Game()
    game.run()