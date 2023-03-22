import pygame
from Constants import *
from Functions import *


class Tile:  # tile used as a super class, the whole display made from them
    def __init__(self, img_src, x, y):
        self.img_src = img_src
        self.img_src = pygame.transform.scale(self.img_src, (SCALE, SCALE))
        self.x = x
        self.y = y

    def isWalkable(self):
        pass

    def isKillable(self):
        pass

    def getType(self):
        pass

    def getImgSrc(self):
        return self.img_src

    def setImgSrc(self, img_src):
        self.img_src = img_src
        self.img_src = pygame.transform.scale(self.img_src, (SCALE, SCALE))

    def getColor(self):
        for key, value in EVERY_COLOR.items():
            value = pygame.transform.scale(value, (SCALE, SCALE))

            value_array = pygame.surfarray.array2d(value)
            img_array = pygame.surfarray.array2d(self.img_src)
            if (value_array == img_array).all():
                return key

        return "W"



    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y
