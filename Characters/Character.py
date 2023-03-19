import pygame
from Constants import *
from Functions import *


class Character:
    def __init__(self, img_src, x, y):
        self.img_src = img_src
        self.x = x
        self.y = y
        self.actualX = x
        self.camera_pos = 0

    def movement(self, map, camera_end, jumping, jump_counter, falling):
        pass

    def jump(self, map, jumping, jump_counter):
        pass

    def onGround(self, tiles):
        pass

    def type(self):
        pass

    def reset(self):
        self.x = X_POSITION
        self.actualX = X_POSITION
        self.y = Y_POSITION

    # def isGonnaStuck(self, tiles):
    #     pass

    def getImageSrc(self):
        return self.img_src

    def getX(self):
        return self.actualX

    def getY(self):
        return self.y
