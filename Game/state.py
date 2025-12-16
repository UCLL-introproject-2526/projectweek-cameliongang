import pygame as pg
class state:
    def __init__(self):
        self.xcoor = 0
        self.ycoor = 0

    def xcoor_update(self, x):
        self.xcoor += x
    
    def ycoor_update(self, y):
        self.ycoor += y

    def render_camelion(self, surface):
        camelion_img = pg.image.load('./resources/camelion.png').convert()
        camelion_img.set_colorkey((0, 0, 0))
        camelion_img = pg.transform.scale(camelion_img,
                                (camelion_img.get_width() / 2,
                                 camelion_img.get_height() / 2))
        surface.blit(camelion_img, (self.xcoor, self.ycoor))

    def render_bush(self, surface):
        bush_img = pg.image.load('./resources/bush.png').convert()
        bush_img.set_colorkey((0, 0, 0))
        bush_img = pg.transform.scale(bush_img,
                                (bush_img.get_width() / 1.5,
                                 bush_img.get_height() / 1.5))
        surface.blit(bush_img, (800, 450))
