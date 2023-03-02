import pygame.transform
import Constants
from Tiles.BasicTile import *
from Tiles.CollideTile import *
from Tiles.CollideTile import CollideTile
from Tiles.ObstacleTile import *
from Tiles.OptionTile import *
import Camera
import random  # random.randint(1, 10)


# Map:
def write_map(map_name, rows, cols):  # create a basic editable text file with a basic map
    f = open(map_name, "w")
    for row in range(rows):
        for col in range(cols):
            if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                f.write("X ")
            elif col == FLOOR_HEIGHT and random.randint(0, 5) == 0:
                f.write("S ")
            elif col == CELLING_HEIGHT and random.randint(0, 5) == 0:
                f.write("RS ")
            else:
                f.write("W ")
        f.write("\n")
    f.close()  # write_map("map.txt", MAP_ROWS, MAP_COLS)


def read_map():  # read the .txt map and return it
    world = []
    f = open("map.txt", "r")
    for line in f:
        line = line.replace("\n", "")
        world.append(line.split(" "))
    f.close()
    return world


def draw_map(tiles, screen, camera_origin):  # make the tiles list (based map) apper on the screen
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            tile = tiles[row][col]
            pygame.transform.scale(tile.getImgSrc(), (SCALE, SCALE))
            camera_x, camera_y = camera_origin
            screen.blit(tile.getImgSrc(), (tile.getX() * Constants.SCALE - camera_x, tile.getY() * Constants.SCALE - camera_y))


# Tiles:
def generate_tiles(map):  # create the tiles based of the map
    tiles = []
    for row in range(Constants.MAP_ROWS):
        new_line = []
        for col in range(Constants.MAP_COLS):
            for color in Constants.BASIC_COLORS:
                if map[row][col] == color:
                    new_line.append(BasicTile(Constants.BASIC_COLORS[color], row, col))

            for color in Constants.COLLIDER_COLORS:
                if map[row][col] == color:
                    new_line.append(CollideTile(Constants.COLLIDER_COLORS[color], row, col))

            for color in Constants.OBSTACLE_COLORS:
                if map[row][col] == color:
                    new_line.append(ObstacleTile(Constants.OBSTACLE_COLORS[color], row, col))
        tiles.append(new_line)
    return tiles


# Menu:
def generate_menu(screen, rows, cols):  # auto create normal menu
    for row in range(rows):
        for col in range(cols):
            color = random_color_generator()
            pygame.draw.rect(screen, color, pygame.Rect(MENU_TILE_SIZE * col, MENU_TILE_SIZE * row, MENU_TILE_SIZE, MENU_TILE_SIZE))
            pygame.display.flip()


def update_menu_colors(screen, rows, cols):  # auto create normal menu
    for row in range(rows):
        for col in range(cols):
            if random.randint(0, 100) < CHANGE_CHANCE:
                color = random_color_generator()
                pygame.draw.rect(screen, color, pygame.Rect(MENU_TILE_SIZE * col, MENU_TILE_SIZE * row, MENU_TILE_SIZE, MENU_TILE_SIZE))
                pygame.display.flip()
                initiate_menu(screen)


def initiate_menu(screen):
    levels = ["Beginner", "Advanced", "Extreme"]
    rects = []
    for rect in range(RECT_AMOUNT):
        pygame.draw.rect(screen, RECT_COLOR, pygame.Rect(FIRST_RECT_X_POS + RECT_SPACE * rect, FIRST_RECT_Y_POS, RECT_SIZE, RECT_SIZE))
        rects.append(OptionTile(ALL_COLORS["W"], levels[rect], FIRST_RECT_X_POS + RECT_SPACE * rect, FIRST_RECT_Y_POS))
        add_text(screen, levels[rect], TEXT_COLOR, FIRST_RECT_X_POS + RECT_SPACE * rect + TEXT_X_SPACE, FIRST_RECT_Y_POS + TEXT_Y_SPACE)
        pygame.display.flip()
    return rects


def draw_menu(tiles, screen):  # make the tiles list (based map) apper on the screen
    for row in range(MENU_ROWS):
        for col in range(MENU_COLS):
            tile = tiles[row][col]
            pygame.transform.scale(tile.getImgSrc(), (SCALE, SCALE))
            screen.blit(tile.getImgSrc(), (tile.getX() * Constants.SCALE, tile.getY() * Constants.SCALE))


# Game progress:
def next_level(difficulty):
    difficulty += 1
    return difficulty


# Other:
def add_text(screen, text, color, x_pos, y_pos):
    font_name = "Arial"
    font = pygame.font.SysFont(font_name, TEXT_SIZE)
    screen.blit(font.render(text, True, color), (x_pos, y_pos))


def mouse_in_button(rect, mouse_pos):
    if rect.getX() + RECT_SIZE > mouse_pos[0] > rect.getX() and rect.getY() < mouse_pos[1] < rect.getY() + RECT_SIZE:
        return True


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def isWalkable(tiles, row, col):  # is possible to move through the tile
    if 0 < row < MAP_ROWS and 0 < col < MAP_COLS:
        return tiles[row][col].isWalkable()
    return False


def isKilled(tiles, row, col):  # is touch this tile will kill you
    return tiles[row][col].isKillable()


def kill_character(character):
    character.reset()
    Camera.Camera.reset()
