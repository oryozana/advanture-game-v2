import pygame
from Constants import *
from Functions import *
from Tiles.Tile import Tile


class OptionTile(Tile):  # tile who used when the player need to make choices
    def __init__(self, img_src, text, x, y):
        super().__init__(img_src, x, y)
        self.img_src = pygame.transform.scale(self.img_src, (RECT_SIZE, RECT_SIZE))
        self.text = text

    def isWalkable(self):
        return False

    def isKillable(self):
        return False

    def getType(self):
        return "R"

    def getText(self):
        return self.text
