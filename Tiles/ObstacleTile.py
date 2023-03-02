import pygame
from Constants import *
from Functions import *
from Tiles.Tile import Tile


class ObstacleTile(Tile):  # tile who will kill the character if touched
    def __init__(self, img_src, x, y):
        super().__init__(img_src, x, y)

    def isWalkable(self):
        return True

    def isKillable(self):
        return True

    def getType(self):
        return "O"
