import pygame as pg
import random
import time

leftwalk = 0
rightwalk = 0
# dit is een enemy die enkel lings en rechts stapt
class Enemyclass:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkingspeed = 20
        self.jumpingtime = 2
        self.rect = pg.Rect(x, y, width, height)
        self.spawn = (x , y)
        self.jumpheight = 10
        self.velocity_y = 0
        self.velocity_x = 0
        self.direction = -1

    def update(self, tiles):



        self.on_ground = False
        for 