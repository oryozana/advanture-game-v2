from Tiles.CollideTile import CollideTile
from Constants import *
from random import randint


def create_shelves(distance, tiles, length, body_color, row, col):
    for shelf in range(MAP_ROWS // distance + length // SCALE - row // distance - 1):
        random = randint(-SHELF_HEIGHT_DIFF, SHELF_HEIGHT_DIFF)
        create_shelf(tiles, length, body_color, row + distance * shelf, col + random)


def create_shelf(tiles, length, body_color, row, col):
    for block in range(length + 1):
        tiles[row + block][col] = CollideTile(ALL_COLORS[body_color], tiles[row + block][col].getX(), tiles[row + block][col].getY())
