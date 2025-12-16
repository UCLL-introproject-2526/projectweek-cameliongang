import pygame, sys
from settings import *
from level import Level, LEVELS
from ui import UI

# Ref: http://projectweek.leone.ucll.be/stories/gui/create-window/index.html#create_main_surface
def create_main_surface():
    """Creates the main display surface."""
    return pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    # Ref: http://projectweek.leone.ucll.be/stories/gui/game-state/index.html
    def __init__(self):
        pygame.display.set_caption("Chameleon Platformer")
        self.ui = UI()
        self.state = 'menu' # menu, level_select, playing, paused
        self.level = None

    def process_input(self):
        # Ref: http://projectweek.leone.ucll.be/reference/game-loop/index.html
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'playing':
                        self.state = 'paused'
                    elif self.state == 'paused':
                        self.state = 'playing'
                        
                if event.key == pygame.K_RETURN:
                    if self.state == 'menu':
                        self.state = 'level_select'
                        
                if self.state == 'level_select':
                    # Dynamic level selection
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        level_index = event.key - pygame.K_1
                        if 0 <= level_index < len(LEVELS):
                            self.ui.show_loading_screen()
                            self.level = Level(level_index)
                            self.state = 'playing'
                    
                    if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                        level_index = event.key - pygame.K_KP1
                        if 0 <= level_index < len(LEVELS):
                            self.ui.show_loading_screen()
                            self.level = Level(level_index)
                            self.state = 'playing'
        return True

    def update(self, elapsed_seconds):
        if self.state == 'playing' and self.level:
            self.level.update(elapsed_seconds)

    def render(self, surface):
        if self.state == 'menu':
            self.ui.show_main_menu()
        
        elif self.state == 'level_select':
            self.ui.show_level_select(LEVELS)
        
        elif self.state == 'playing':
            if self.level:
                self.level.render(surface)
                self.ui.show_hud(self.level.player)
        
        elif self.state == 'paused':
            if self.level:
                self.level.render(surface)
                self.ui.show_hud(self.level.player)
            self.ui.show_pause_menu()

def clear_surface(surface):
    # Ref: http://projectweek.leone.ucll.be/stories/gui/graphics/animation/clearing-buffer/index.html
    surface.fill(BLACK)

def render_frame(surface, state):
    # Ref: http://projectweek.leone.ucll.be/stories/gui/graphics/animation/animation-junction/index.html
    clear_surface(surface)
    state.render(surface)
    pygame.display.update()

def main():
    # Ref: http://projectweek.leone.ucll.be/stories/gui/create-window/index.html#main
    pygame.init()
    surface = create_main_surface()
    game = Game()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Measure time
        # Ref: http://projectweek.leone.ucll.be/stories/gui/graphics/animation/time-based-animation/index.html
        dt = clock.tick(FPS) / 1000.0 # Standardize to seconds
        
        # Process Input
        running = game.process_input()
        
        # Update State
        game.update(dt)
        
        # Render Frame
        render_frame(surface, game)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
