import pygame.transform
import Constants
import Furniture
from Tiles.BasicTile import *
from Tiles.BasicTile import BasicTile
from Tiles.CollideTile import *
from Tiles.CollideTile import CollideTile
from Tiles.ObstacleTile import *
from Tiles.OptionTile import *
import Camera
import random  # random.randint(1, 10)


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
            change = True
            if FIRST_RECT_Y_POS <= row * SCALE <= FIRST_RECT_Y_POS + RECT_SIZE:
                if FIRST_RECT_X_POS <= col * SCALE <= FIRST_RECT_X_POS + RECT_SIZE:
                    change = False
                elif FIRST_RECT_X_POS + RECT_SPACE <= col * SCALE <= FIRST_RECT_X_POS + RECT_SIZE + RECT_SPACE:
                    change = False
                elif FIRST_RECT_X_POS + (RECT_SPACE * 2) <= col * SCALE <= FIRST_RECT_X_POS + RECT_SIZE + RECT_SPACE * 2:
                    change = False
                elif FIRST_RECT_X_POS + (RECT_SPACE * 3) <= col * SCALE <= FIRST_RECT_X_POS + RECT_SIZE + RECT_SPACE * 3:
                    change = False

            if random.randint(0, 100) < CHANGE_CHANCE and change:
                color = random_color_generator()
                pygame.draw.rect(screen, color, pygame.Rect(MENU_TILE_SIZE * col, MENU_TILE_SIZE * row, MENU_TILE_SIZE, MENU_TILE_SIZE))
                initiate_menu(screen)


def initiate_menu(screen):
    levels = ["Beginner", "Advanced", "Extreme", "Beta - AI"]
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


# End screen:
def generate_end_screen():
    end_screen = []
    for row in range(END_SCREEN_ROWS):
        new_line = []
        for col in range(END_SCREEN_COLS):
            if col == FLOOR_HEIGHT + 1 or col == CELLING_HEIGHT - 1 or row == 0 or row == END_SCREEN_ROWS - 1:
                new_line.append("X")
            else:
                new_line.append("W")
        end_screen.append(new_line)
    return end_screen


def generate_tiles_end_screen(map):  # create the tiles based of the map
    tiles = []
    for row in range(END_SCREEN_ROWS):
        new_line = []
        for col in range(END_SCREEN_COLS):
            new_line.append(BasicTile(Constants.ALL_COLORS[map[row][col]], row, col))
        tiles.append(new_line)
    return tiles


def draw_end_screen(screen, tiles):  # auto create normal end screen
    for row in range(END_SCREEN_ROWS):
        for col in range(END_SCREEN_COLS):
            tile = tiles[row][col]
            pygame.transform.scale(tile.getImgSrc(), (SCALE, SCALE))
            screen.blit(tile.getImgSrc(), (tile.getX() * Constants.SCALE, tile.getY() * Constants.SCALE))

            # camera_x, camera_y = camera_origin
            # screen.blit(tile.getImgSrc(), (tile.getX() * Constants.SCALE -
            # camera_x, tile.getY() * Constants.SCALE - camera_y))


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
