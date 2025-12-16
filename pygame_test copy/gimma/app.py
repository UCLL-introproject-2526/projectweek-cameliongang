import pygame, sys
from settings import *
from level import Level, LEVELS
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chameleon Platformer")
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.state = 'menu' # menu, level_select, playing, paused
        self.level = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
                        # pygame.K_1 is 49. So 1 -> 49, 2 -> 50, etc.
                        # We can check if the key is in the range of available levels
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            level_index = event.key - pygame.K_1
                            if 0 <= level_index < len(LEVELS):
                                self.ui.show_loading_screen()
                                self.level = Level(level_index)
                                self.state = 'playing'
                                
                        # Also support numpad
                        if pygame.K_KP1 <= event.key <= pygame.K_KP9:
                             level_index = event.key - pygame.K_KP1
                             if 0 <= level_index < len(LEVELS):
                                self.ui.show_loading_screen()
                                self.level = Level(level_index)
                                self.state = 'playing'

            self.screen.fill('black')
            
            if self.state == 'menu':
                self.ui.show_main_menu()
            
            elif self.state == 'level_select':
                self.ui.show_level_select(LEVELS)
            
            elif self.state == 'playing':
                if self.level:
                    self.level.run()
                    self.ui.show_hud(self.level.player)
            
            elif self.state == 'paused':
                if self.level:
                    self.level.run() 
                    self.ui.show_hud(self.level.player)
                self.ui.show_pause_menu()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
