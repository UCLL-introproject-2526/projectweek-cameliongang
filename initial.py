import pygame as pg

def create_main_surface():
    screen_size = pg.display.set_mode((1024, 768))
    return screen_size

def render_frame(surface,x):
    clear_surface(surface)
    pg.draw.circle(surface, (255, 0, 0), (x, 200), 200)
    pg.display.flip()

def clear_surface(surface):
    surface.fill((0, 0, 0))

class state:
    def __init__(self):
        self.xcoor = 0
        self.ycoor = 0

    def xcoor_update(self, x):
        self.xcoor += x
    
    def ycoor_update(self, y):
        self.ycoor += y

    def render(self, surface):
        clear_surface(surface)
        camelion_img = pg.image.load('./resources/camelion.png').convert()
        camelion_img.set_colorkey((0, 0, 0))
        camelion_img = pg.transform.scale(camelion_img,
                                (camelion_img.get_width() / 2,
                                 camelion_img.get_height() / 2))
        surface.blit(camelion_img, (self.xcoor, self.ycoor))

class keyboard:
    def __init__(self):
        pass


def main():
    #initialization
    pg.init()
    x = 0
    surface = create_main_surface()
    clock = pg.time.Clock()
    status = state()
    running = True
    delta_time = 0.1
    movingxmin = False
    movingxplus = False
    movingymin = False
    movingyplus = False
    while running:

        status.render(surface)
        if movingxmin:
            status.xcoor_update(-1)
        if movingxplus:
            status.xcoor_update(1)
        if movingymin:
            status.ycoor_update(-1)
        if movingyplus:
            status.ycoor_update(1)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    movingxmin = True
                if event.key == pg.K_RIGHT:
                    movingxplus = True

                if event.key == pg.K_UP:
                    movingymin = True
                if event.key == pg.K_DOWN:
                    movingyplus = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    movingxmin = False
                if event.key == pg.K_RIGHT:
                    movingxplus = False

                if event.key == pg.K_UP:
                    movingymin = False
                if event.key == pg.K_DOWN:
                    movingyplus = False

        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

        pg.display.flip()









pg.quit()
if __name__ == "__main__":
    main()