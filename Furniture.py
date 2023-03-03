from Tiles.CollideTile import CollideTile
from Constants import *
from random import randint


def create_chandeliers(amount, space, tiles, body_color, light_color, row, col):
    for chandelier in range(amount):
        location = row + chandelier * space
        if 3 < location < MAP_ROWS - 3:
            create_chandelier(tiles, body_color, light_color, location, col)


def create_chandelier(tiles, body_color, light_color, row, col):
    tiles[row][col].setImgSrc(BASIC_COLORS[body_color])
    tiles[row][col + 1].setImgSrc(BASIC_COLORS[body_color])
    tiles[row][col + 2].setImgSrc(BASIC_COLORS[body_color])

    tiles[row][col + 3].setImgSrc(BASIC_COLORS[body_color])
    tiles[row + 1][col + 3].setImgSrc(BASIC_COLORS[body_color])
    tiles[row - 1][col + 3].setImgSrc(BASIC_COLORS[body_color])
    tiles[row + 2][col + 3].setImgSrc(BASIC_COLORS[body_color])
    tiles[row - 2][col + 3].setImgSrc(BASIC_COLORS[body_color])

    tiles[row][col + 4].setImgSrc(BASIC_COLORS[body_color])
    tiles[row + 2][col + 4].setImgSrc(BASIC_COLORS[body_color])
    tiles[row - 2][col + 4].setImgSrc(BASIC_COLORS[body_color])

    tiles[row][col + 5].setImgSrc(BASIC_COLORS[light_color])
    tiles[row + 2][col + 5].setImgSrc(BASIC_COLORS[light_color])
    tiles[row - 2][col + 5].setImgSrc(BASIC_COLORS[light_color])


def create_low_chandelier(tiles, body_color, light_color, row, col):
    tiles[row][col].setImgSrc(BASIC_COLORS[body_color])

    tiles[row][col + 1].setImgSrc(BASIC_COLORS[body_color])
    tiles[row + 1][col + 1].setImgSrc(BASIC_COLORS[body_color])
    tiles[row - 1][col + 1].setImgSrc(BASIC_COLORS[body_color])

    tiles[row][col + 2].setImgSrc(BASIC_COLORS[body_color])
    tiles[row + 1][col + 2].setImgSrc(BASIC_COLORS[light_color])
    tiles[row - 1][col + 2].setImgSrc(BASIC_COLORS[light_color])

    tiles[row][col + 3].setImgSrc(BASIC_COLORS[light_color])


def create_desk(tiles, height, width, body_color, row, col):
    for floor in range(height):
        tiles[row][col - floor] = CollideTile(ALL_COLORS[body_color], tiles[row][col - floor].getX(), tiles[row][col - floor].getY())
        tiles[row + width][col - floor] = CollideTile(ALL_COLORS[body_color], tiles[row + width][col - floor].getX(), tiles[row + width][col - floor].getY())

    for block in range(width + 1):
        tiles[row + block][col - height] = CollideTile(ALL_COLORS[body_color], tiles[row + block][col - height].getX(), tiles[row + block][col - height].getY())


def create_border(tiles, height, width, body_color, row, col):
    for i in range(height):
        for j in range(width):
            tiles[row + i][col - j] = CollideTile(COLLIDER_COLORS[body_color], tiles[row + i][col - j].getX(), tiles[row + i][col - j].getY())


def create_shelves(distance, tiles, length, body_color, row, col):
    for shelf in range(MAP_ROWS // distance + length // SCALE - row // distance - 1):
        random = randint(-SHELF_HEIGHT_DIFF, SHELF_HEIGHT_DIFF)
        create_shelf(tiles, length, body_color, row + distance * shelf, col + random)


def create_shelf(tiles, length, body_color, row, col):
    for block in range(length + 1):
        tiles[row + block][col] = CollideTile(ALL_COLORS[body_color], tiles[row + block][col].getX(), tiles[row + block][col].getY())
