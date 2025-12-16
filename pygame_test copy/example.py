import pygame as pg

pg.init()

screen = pg.display.set_mode((640, 640))

potato_img = pg.image.load('potato.png').convert()

potato_img = pg.transform.scale(potato_img,
                                (potato_img.get_width() * 2,
                                 potato_img.get_height() * 2))

potato_img.set_colorkey((0, 0, 0))

#voor multiple potatoes maar werkt niet module not calable
#potatoes = pg.surface((64, 64), pg.SRCALPHA)
#potatoes.blit(potato_img, (0, 0))
#potatoes.blit(potato_img, (20, 0))
#potatoes.blit(potato_img, (0, 10))

x = 0
clock = pg.time.Clock()
running = True
moving = False
sound = pg.mixer.Sound('clank.wav')

delta_time = 0.1

font = pg.font.Font(None, size=30)

while running: 
    screen.fill((255, 255, 255))
    #voor fade
    #potato_img.set_alpha(max(0, 255 - x))

    screen.blit(potato_img, (x, 30))

    hitbox = pg.Rect(x, 30, potato_img.get_width(), potato_img.get_height())

    mpos = pg.mouse.get_pos()

    target = pg.Rect(300, 0, 225, 280)
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mpos)
    pg.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)
    if moving:
        x += 50 * delta_time
    
    #text toevoegen via voor ingestelde font hierboven
    text = font.render('Hello Charles/Sander!', True, (0, 0, 0))
    screen.blit(text, (300, 100))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                moving = True
            if event.key == pg.K_f:
                sound.play()
        if event.type == pg.KEYUP:
            if event.key == pg.K_d:
                moving = False

    pg.display.flip()

    dela_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))




pg.quit()




    #music
    sound = pg.mixer.music.load('.\\resources\\themesong.mp3')
    pg.mixer.music.play(-1)
    #######################