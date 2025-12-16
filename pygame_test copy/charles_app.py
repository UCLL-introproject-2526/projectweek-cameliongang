import pygame as pg

# Function to create and return the main game surface (window)
def create_main_surface():
    screen_size = pg.display.set_mode((1700, 900))
    return screen_size


# Function to clear the surface by filling it with black
def clear_surface(surface):
    surface.fill((0, 0, 0))

# Class to manage the game state, including position and rendering
class state:
    def __init__(self):
        #gravity system
        self.width=40
        self.height=20
        self.xcoor=200
        self.ycoor = 50
        self.velocity_y = 0
        self.gravity = 0.2

    def update_gravity(self):
        self.velocity_y += self.gravity
        self.ycoor += self.velocity_y

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





# Main game loop function
def main():
    # Initialization of Pygame and game variables
    pg.init()
    surface = create_main_surface()
    clock = pg.time.Clock()
    status = state()
    running = True
    delta_time = 0.1
    movingxmin = False
    movingxplus = False
    movingymin = False
    movingyplus = False
    floor_y = 550
    # Load background image
    background = pg.image.load(".\\resources\\background_img.jpg").convert()
    background = pg.transform.scale(background, (1700, 900))
    # Main game loop
    while running:
        # Draw background first
        surface.blit(background, (0, 0))

        #gravity system
        status.update_gravity()

        #floor collision
        if status.ycoor + status.height >= floor_y:
            status.ycoor = floor_y -status.height
            status.velocity_y = 0   # stop falling


        status.render_camelion(surface)
        status.render_bush(surface)
        if movingxmin:
            status.xcoor_update(-5)
        if movingxplus:
            status.xcoor_update(5)
        if movingymin:
            status.ycoor_update(-20)



        # Handle events
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

        # Cap the frame rate and calculate delta time for smooth movement
        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

        # Update the display
        pg.display.flip()

pg.quit()
if __name__ == "__main__":
    main()