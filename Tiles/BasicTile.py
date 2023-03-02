import pygame
from Constants import *
from Functions import *
from Tiles.Tile import Tile


class BasicTile(Tile):  # background tile, don't do much but that
    def __init__(self, img_src, x, y):
        super().__init__(img_src, x, y)

    def isWalkable(self):
        return True

    def isKillable(self):
        return False

    def getType(self):
        return "B"
