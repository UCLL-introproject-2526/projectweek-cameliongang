import pygame as pg

def create_main_surface():
    return pg.display.set_mode((1700, 900))

class State:
    def __init__(self):
        self.width = 40
        self.height = 20
        self.xcoor = 200
        self.ycoor = 50
        self.velocity_y = 0
        self.gravity = 0.675
        self.jump_strength = -20
        self.jump_cut = -4
        self.on_ground = False

    def update_gravity(self, keys):
        # Apply gravity
        self.velocity_y += self.gravity
        self.ycoor += self.velocity_y

        # If rising and UP is released, cut the jump short
        if self.velocity_y < 0 and not keys[pg.K_UP]:
            self.velocity_y = max(self.velocity_y, self.jump_cut)

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

    def xcoor_update(self, x):
        self.xcoor += x

    def render_camelion(self, surface):
        img = pg.image.load('./resources/camelion.png').convert()
        img.set_colorkey((0, 0, 0))
        img = pg.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
        surface.blit(img, (self.xcoor, self.ycoor))

    def render_bush(self, surface):
        bush = pg.image.load('./resources/bush.png').convert()
        bush.set_colorkey((0, 0, 0))
        bush = pg.transform.scale(bush, (int(bush.get_width() / 1.5), int(bush.get_height() / 1.5)))
        surface.blit(bush, (800, 450))


def main():
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    status = State()
    running = True
    movingxmin = False
    movingxplus = False
    floor_y = 500

    background = pg.image.load("./resources/background_img.jpg").convert()
    background = pg.transform.scale(background, (1700, 900))

    while running:
        # Floor collision
        if status.ycoor + status.height >= floor_y:
            status.ycoor = floor_y - status.height
            status.velocity_y = 0
            status.on_ground = True
        else:
            status.on_ground = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    movingxmin = True
                if event.key == pg.K_RIGHT:
                    movingxplus = True
                if event.key == pg.K_UP:
                    status.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    movingxmin = False
                if event.key == pg.K_RIGHT:
                    movingxplus = False

        keys = pg.key.get_pressed()

        # Physics
        status.update_gravity(keys)

        # Floor collision
        

        # Movement
        if movingxmin:
            status.xcoor_update(-5)
        if movingxplus:
            status.xcoor_update(5)

        # Draw
        surface.blit(background, (0, 0))
        status.render_camelion(surface)
        status.render_bush(surface)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()