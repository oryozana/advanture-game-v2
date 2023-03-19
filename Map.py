import Furniture
from Constants import *
from Tiles.BasicTile import *
from Tiles.CollideTile import *
from Tiles.ObstacleTile import *


class Map:
    def __init__(self):
        write_map("map.txt", MAP_ROWS, MAP_COLS, 1)
        self.map = read_map()
        self.tiles = generate_tiles(self.map)
        self.difficulty = 1
        self.beginner_skulls = []
        self.advanced_skulls = []
        self.extreme_skulls = []

        write_map("map.txt", MAP_ROWS, MAP_COLS, BEGINNER_DIFFICULTY)
        self.beginner_map = read_map()
        write_map("map.txt", MAP_ROWS, MAP_COLS, ADVANCED_DIFFICULTY)
        self.advanced_map = read_map()
        write_map("map.txt", MAP_ROWS, MAP_COLS, EXTREME_DIFFICULTY)
        self.extreme_map = read_map()

    def add_furniture(self, furniture_name):
        match furniture_name:
            case "Chandelier":
                Furniture.create_chandeliers(CHANDELIER_AMOUNT, CHANDELIER_SPACE, self.tiles, "SI", "G", CHANDELIER_START_POINT, CELLING_HEIGHT)
            case "Mushroom":
                Furniture.create_mushrooms(MUSHROOM_AMOUNT, MUSHROOM_SPACE, self.tiles, "CM", "SM", MUSHROOM_START_POINT, FLOOR_HEIGHT)

    def add_skulls_to_tiles(self):
        skulls_list = []
        match self.difficulty:
            case Constants.BEGINNER_DIFFICULTY:
                skulls_list = self.beginner_skulls
            case Constants.ADVANCED_DIFFICULTY:
                skulls_list = self.advanced_skulls
            case Constants.EXTREME_DIFFICULTY:
                skulls_list = self.extreme_skulls

        for location in skulls_list:
            self.tiles[location[0]][location[1]].setImgSrc(BASIC_COLORS["SK"])

    def add_skull(self, character_type, location):
        if location[1] != MAP_END:
            skulls_list = []
            match self.difficulty:
                case Constants.BEGINNER_DIFFICULTY:
                    skulls_list = self.beginner_skulls
                case Constants.ADVANCED_DIFFICULTY:
                    skulls_list = self.advanced_skulls
                case Constants.EXTREME_DIFFICULTY:
                    skulls_list = self.extreme_skulls

            match character_type:
                case "B":
                    skulls_list.append((location[0], location[1] + 1))
                case "R":
                    skulls_list.append((location[0], location[1] - 1))

    def update_map(self):
        match self.difficulty:
            case Constants.BEGINNER_DIFFICULTY:
                self.map = self.beginner_map
            case Constants.ADVANCED_DIFFICULTY:
                self.map = self.advanced_map
            case Constants.EXTREME_DIFFICULTY:
                self.map = self.extreme_map
        self.update_tiles()

    def update_tiles(self):
        self.tiles = generate_tiles(self.map)
        self.add_furniture("Chandelier")
        self.add_furniture("Mushroom")

    def update_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.update_map()

    def level_up(self):
        self.difficulty += 1
        self.update_map()

    def get_map(self):
        return self.map

    def get_tiles(self):
        return self.tiles

    def get_difficulty(self):
        return self.difficulty


def write_map(map_name, rows, cols, difficulty):  # create a basic editable text file with a basic map
    f = open(map_name, "w")
    for row in range(rows):
        for col in range(cols):
            if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                f.write("R ")
            elif col == FLOOR_HEIGHT and random.randint(0, DEFAULT_TRAP_SPAWN_RATE - difficulty) == 0:
                f.write("S ")
            elif col == CELLING_HEIGHT and random.randint(0, DEFAULT_TRAP_SPAWN_RATE - difficulty) == 0:
                f.write("RS ")
            elif col == (CELLING_HEIGHT + FLOOR_HEIGHT) // 2 and 0 < row < SUPPORT_SHELF_LENGTH:
                f.write("R ")
            else:
                f.write("W ")
        f.write("\n")
    f.close()  # write_map("map.txt", MAP_ROWS, MAP_COLS, map.get_difficulty())


def read_map():  # read the .txt map and return it
    world = []
    f = open("map.txt", "r")
    for line in f:
        line = line.replace("\n", "")
        world.append(line.split(" ")[:-1])
    f.close()
    return world


def draw_map(tiles, screen, camera_origin):  # make the tiles list (based map) apper on the screen
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            tile = tiles[row][col]
            pygame.transform.scale(tile.getImgSrc(), (SCALE, SCALE))
            camera_x, camera_y = camera_origin
            screen.blit(tile.getImgSrc(),
                        (tile.getX() * Constants.SCALE - camera_x, tile.getY() * Constants.SCALE - camera_y))


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
