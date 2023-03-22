import random

import pygame as pygame
import pygame.image

# Screen:
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# Map:
MAP_ROWS = 300  # normal: 350, after change use write_map("map.txt", MAP_ROWS, MAP_COLS)
MAP_COLS = 25  # normal: 25, after change use write_map("map.txt", MAP_ROWS, MAP_COLS)
CELLING_HEIGHT = 1  # use as col
FLOOR_HEIGHT = MAP_COLS - 2  # use as col
MIDDLE_HEIGHT = (CELLING_HEIGHT + FLOOR_HEIGHT) // 2  # Use as col
MAP_END = MAP_ROWS - 2

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
FIRST_RECT_X_POS = 60
FIRST_RECT_Y_POS = 220
RECT_COLOR = (255, 255, 255)
RECT_SIZE = 200
RECT_SPACE = 220
RECT_AMOUNT = 4
CHANGE_CHANCE = 20
CHANGE_RATE = 25
MENU_FPS = 22

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

# Difficulties:
BEGINNER_DIFFICULTY = 1
ADVANCED_DIFFICULTY = 2
EXTREME_DIFFICULTY = 3
END_GAME_DIFFICULTY = 4
AI_DIFFICULTY = 5

# Camera:
CAMERA_X_START = ((SCREEN_WIDTH - 2) // SCALE) // 3
CAMERA_X_END = MAP_ROWS - SCREEN_WIDTH // SCALE

# Furniture:
START_POINT = 15
END_POINT = MAP_ROWS - START_POINT
MIN_FURNITURE_AMOUNT = 3

# Shelf:
SHELF_HEIGHT_DIFF = int(JUMP // 2) + 1
DEFAULT_SHELF_HEIGHT = 15
SUPPORT_SHELF_LENGTH = 11
DEFAULT_SHELF_LENGTH = 4
DEFAULT_SHELF_DISTANCE = 10

# Chandelier:
CHANDELIER_AMOUNT = random.randint(MIN_FURNITURE_AMOUNT, 5)
CHANDELIER_SPACE = MAP_ROWS // CHANDELIER_AMOUNT + random.randint(-10, 10)
CHANDELIER_START_POINT = random.randint(START_POINT, MAP_ROWS + (MAP_ROWS - END_POINT) - (CHANDELIER_SPACE * (CHANDELIER_AMOUNT - 1)))

# Mushroom:
MUSHROOM_AMOUNT = random.randint(MIN_FURNITURE_AMOUNT, 6)
MUSHROOM_SPACE = MAP_ROWS // MUSHROOM_AMOUNT + random.randint(-10, 10)
MUSHROOM_START_POINT = random.randint(START_POINT, MAP_ROWS + (MAP_ROWS - END_POINT) - (MUSHROOM_SPACE * (MUSHROOM_AMOUNT - 1)))

# Traps:
DEFAULT_TRAP_SPAWN_RATE = 4

# Tiles:
ALL_COLORS = {"R": pygame.image.load("Colors\\rust.png"),
              "W": pygame.image.load("Colors\\white.png"),
              "X": pygame.image.load("Colors\\brick_wall.png"),
              "G": pygame.image.load("Colors\\gold.png"),
              "SI": pygame.image.load("Colors\\silver.png"),
              "SK": pygame.image.load("Colors\\skull.png"),
              "HM": pygame.image.load("Colors\\mushroom_hand.png"),
              "CM": pygame.image.load("Colors\\mushroom_cap_color.png"),
              "SM": pygame.image.load("Colors\\mushroom_secondary_color.png"),
              "EM": pygame.image.load("Colors\\mushroom_eye.png")}

BASIC_COLORS = {"W": pygame.image.load("Colors\\white.png"),
                "G": pygame.image.load("Colors\\gold.png"),
                "SI": pygame.image.load("Colors\\silver.png"),
                "SK": pygame.image.load("Colors\\skull.png"),
                "HM": pygame.image.load("Colors\\mushroom_hand.png"),
                "CM": pygame.image.load("Colors\\mushroom_cap_color.png"),
                "SM": pygame.image.load("Colors\\mushroom_secondary_color.png"),
                "EM": pygame.image.load("Colors\\mushroom_eye.png")}

COLLIDER_COLORS = {"X": pygame.image.load("Colors\\brick_wall.png"),
                   "R": pygame.image.load("Colors\\rust.png")}

OBSTACLE_COLORS = {"S": pygame.image.load("Colors\\spears.png"),
                   "RS": pygame.image.load("Colors\\reversed_spears.png")}
