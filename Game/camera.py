import pygame as pg

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        # Track float position for smoothing
        self.scroll = pg.math.Vector2(0, 0)
        self.smoothing_speed = 0.05 # 5% movement per frame

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        # Target position (center player on screen)
        target_x = -target.rect.centerx + int(1280 / 2)
        target_y = -target.rect.centery + int(720 / 2)
        
        # Smoothly interpolate current scroll towards target
        self.scroll.x += (target_x - self.scroll.x) * self.smoothing_speed
        self.scroll.y += (target_y - self.scroll.y) * self.smoothing_speed
        
        # Clamp to map size
        x = min(0, self.scroll.x)  # left
        y = min(0, self.scroll.y)  # top
        x = max(-(self.width - 1280), x)  # right
        y = max(-(self.height - 720), y)  # bottom
        
        # Update rect with integer values
        self.camera = pg.Rect(int(x), int(y), self.width, self.height)
