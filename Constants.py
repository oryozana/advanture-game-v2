import pygame as pygame
import pygame.image

# Screen:
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# Map:
MAP_ROWS = 200  # normal: 350, after change use write_map("map.txt", MAP_ROWS, MAP_COLS)
MAP_COLS = 25  # normal: 25, after change use write_map("map.txt", MAP_ROWS, MAP_COLS)
CELLING_HEIGHT = 1  # use as col
FLOOR_HEIGHT = MAP_COLS - 2  # use as col

# levels:
Y_TEXT_POS = FLOOR_HEIGHT - 20
X_TEXT_POS = MAP_ROWS

# Inventory:
INVENTORY_AREA = 20
INVENTORY_SCALE = 60
INVENTORY_ITEM_SCALE = 40

# Menu:
MENU_ROWS = 50
MENU_COLS = 25
MENU_TILE_SIZE = 20
FIRST_RECT_X_POS = 80
FIRST_RECT_Y_POS = 200
RECT_COLOR = (255, 255, 255)
RECT_SIZE = 200
RECT_SPACE = 300
RECT_AMOUNT = 3
CHANGE_CHANCE = 15

# Text:
TEXT_COLOR = (0, 0, 0)
TEXT_X_SPACE = 55
TEXT_Y_SPACE = 85
TEXT_SIZE = 25

# Other:
SCALE = 20
SPEED = 1
FPS = 13  # normal: 12

# Character:
JUMP = 5  # normal: 6
GRAVITY = 1
X_POSITION = 1
Y_POSITION = MAP_COLS - 20
CHARACTER_HEIGHT = 20
CHARACTER_WIDTH = 20

# Camera:
CAMERA_X_START = ((SCREEN_WIDTH - 2) // SCALE) // 3
CAMERA_X_END = MAP_ROWS - SCREEN_WIDTH // SCALE

# Shelf:
SHELF_HEIGHT_DIFF = int(JUMP // 2) + 1
SHELF_LENGTH = 15

# Tiles:
ALL_COLORS = {"R": pygame.image.load("Colors\\rust.png"),
              "W": pygame.image.load("Colors\\white.png"),
              "X": pygame.image.load("Colors\\brick_wall.png")}

BASIC_COLORS = {"W": pygame.image.load("Colors\\white.png")}

COLLIDER_COLORS = {"X": pygame.image.load("Colors\\brick_wall.png"),
                   "R": pygame.image.load("Colors\\rust.png")}

OBSTACLE_COLORS = {"S": pygame.image.load("Colors\\spears.png"),
                   "RS": pygame.image.load("Colors\\reversed_spears.png")}
