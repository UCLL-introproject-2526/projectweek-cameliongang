# File: level.py
import pygame


class Tile(pygame.sprite.Sprite):
    def _init_(self, pos, groups):
        super()._init_(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(topleft=pos)

class Level:
    def _init_(self):
        self.visible_sprites = pygame.sprite.Group()
        self.setup_level()

    def setup_level(self):
        map_data = [
            "XXXXXXXXXXXXXXXXXXXX",
            "X                  X",
            "X        P         X",
            "X      XXXXX       X",
            "XXXXXXXXXXXXXXXXXXXX"
        ]
        for row_index, row in enumerate(map_data):
            for col_index, cell in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if cell == 'X':
                    Tile((x,y), [self.visible_sprites])
                if cell == 'P':
                    self.player = Player((x,y))
                    self.visible_sprites.add(self.player)

    def update(self, dt):
        self.visible_sprites.update(dt)

    def render(self, surface):
        surface.fill((30, 30, 30))
        self.visible_sprites.draw(surface)