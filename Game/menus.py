import pygame as pg
from standard_use import game_background

class Button:
    def __init__(self, txt , pos):
        self.text = txt
        self.pos = pos
        self.button = pg.rect.Rect((self.pos[0], self.pos[1]), (260,40))

    def draw(self, surface, font):
        pg.draw.rect(surface, 'light gray', self.button, 0, 5)
        pg.draw.rect(surface, 'dark gray', self.button, 5, 5)
        text = font.render(self.text, True, 'black')
        surface.blit(text, (self.pos[0] + 15, self.pos[1] + 7))
    
    def check_clicked(self):
        if self.button.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            return True
        else:
            return False
        

#Maken van het menu
start_button = Button('Start Game', (500, 260))
levels_button = Button('Choose Level', (500, 340))
credits_button = Button('Credits', (500, 420))
exit_button = Button('Quit Game', (500, 500))
def draw_mainmenu(surface, font):
    background = game_background('mmforest.jpg')
    surface.blit(background, (0, 0))
    command = 0
    text = font.render('Camelion Run!', True, 'black')
    surface.blit(text, (500, 200))
    start_button.draw(surface, font)
    levels_button.draw(surface, font)
    credits_button.draw(surface, font)
    exit_button.draw(surface, font)
    if exit_button.check_clicked():
        command = 1
    if credits_button.check_clicked():
        command = 2
    if levels_button.check_clicked():
        command = 3
    if start_button.check_clicked():
        command = 4
    return command


#Maken van het menu levels
start_button = Button('Start Game', (500, 260))
levels_button = Button('Choose Level', (500, 340))
credits_button = Button('Credits', (500, 420))
exit_button = Button('Quit Game', (500, 500))
def draw_levels_menu(surface, font):
    background = game_background('levels_background.png')
    surface.blit(background, (0, 0))
    command = 0
    text = font.render('Camelion Run!', True, 'black')
    surface.blit(text, (500, 200))
    start_button.draw(surface, font)
    levels_button.draw(surface, font)
    credits_button.draw(surface, font)
    exit_button.draw(surface, font)
    if exit_button.check_clicked():
        command = 1
    if credits_button.check_clicked():
        command = 2
    if start_button.check_clicked():
        command = 4
    return command


# Death Menu Content
restart_button = Button('Restart', (375, 600))
quit_death_button = Button('Quit Game', (675, 600))

def draw_death_menu(surface, font):
    background = game_background('gameover_background.jpg')
    surface.blit(background, (0, 0))
    # Semi-transparent overlay
    overlay = pg.Surface(surface.get_size(), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    surface.blit(overlay, (0,0))
    
    command = 0
    
    restart_button.draw(surface, font)
    quit_death_button.draw(surface, font)
    
    if restart_button.check_clicked():
        command = 1 # Restart
    if quit_death_button.check_clicked():
        command = 2 # Quit
        
    return command