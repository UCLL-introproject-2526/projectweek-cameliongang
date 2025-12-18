import pygame as pg
from level import Level, LEVEL_WIDTH, LEVEL_HEIGHT


def render_bush(self, surface):
    try:
        bush_img = pg.image.load('./resources/bush.png').convert()
        bush_img.set_colorkey((0, 0, 0))
        bush_img = pg.transform.scale(
            bush_img,
            (int(bush_img.get_width() / 1.5), int(bush_img.get_height() / 1.5))
        )
        # Hardcoded bush pos for now: (800, 450)
        bush_rect = bush_img.get_rect(topleft=(800,450))
        surface.blit(bush_img, self.camera.apply_rect(bush_rect))
    except:
        bush_rect = pg.Rect(800, 450, 50, 50)
        pg.draw.rect(surface, (0, 255, 0), self.camera.apply_rect(bush_rect))