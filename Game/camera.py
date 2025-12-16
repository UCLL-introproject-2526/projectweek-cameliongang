import pygame as pg

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(1280 / 2)
        y = -target.rect.centery + int(720 / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - 1280), x)  # right
        y = max(-(self.height - 720), y)  # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
