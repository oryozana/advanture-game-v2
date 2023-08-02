import Constants
from Functions import isKilled
from Characters.BasicCharacter import *
from Characters.ReversedCharacter import *
from Camera import *
from Map import *


class Player:
    def __init__(self, map: Map, screen):
        character_src = pygame.image.load("Characters/Character\\cube.png")  # / - Folder, \\ - File
        character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.character = BasicCharacter(character_src, X_POSITION, Y_POSITION)

        self.score = 0

        self.screen = screen
        self.map = map

        self.jumping = False
        self.jump_counter = 0
        self.falling = False
        self.camera_end = CAMERA_X_END
        self.changeable = True

        self.gonna_be_killed = False
        self.killed = False

        self.just_changed = False
        self.just_changed_from = self.character.type()

    def reverse_gravity(self):
        if self.changeable:
            self.just_changed = True
            self.just_changed_from = self.character.type()

            if self.character.type() == "B":
                character_src = pygame.image.load("Characters/Character\\cubeReversed.png")
                character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
                self.character = ReversedCharacter(character_src, self.character.getX(), self.character.getY())
                self.changeable = False

            elif self.character.type() == "R":
                character_src = pygame.image.load("Characters/Character\\cube.png")
                character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
                self.character = BasicCharacter(character_src, self.character.getX(), self.character.getY())
                self.changeable = False

    def reset_just_changed(self):
        self.just_changed = False
        self.just_changed_from = self.character.type()

    def isGonnaBeKilled(self):
        self.killed = isKilled(self.map.get_tiles(), self.character.getX() + 1,
                               self.character.getY()) and not self.jumping
        self.gonna_be_killed = False

        if self.character.type() == "B":
            if isKilled(self.map.get_tiles(), self.character.getX() + 1, self.character.getY() + 1) and self.falling:
                self.gonna_be_killed = True
                self.killed = True

        elif self.character.type() == "R":
            if isKilled(self.map.get_tiles(), self.character.getX() + 1, self.character.getY() - 1) and self.falling:
                self.gonna_be_killed = True
                self.killed = True

        self.death_handler()

    def death_handler(self):
        if self.killed or self.gonna_be_killed:
            killed_location = None

            if self.just_changed:
                character_src = pygame.image.load("Characters/Character\\cube.png")  # / - Folder, \\ - File
                character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
                match self.just_changed_from:
                    case "B":
                        self.character = BasicCharacter(character_src, self.character.getX(), self.character.getY())
                    case "R":
                        self.character = ReversedCharacter(character_src, self.character.getX(), self.character.getY())

            if self.killed and not self.gonna_be_killed:
                if self.character.type() == "B":
                    killed_location = (self.character.getX() + 1, self.character.getY() - 2)
                elif self.character.type() == "R":
                    killed_location = (self.character.getX() + 1, self.character.getY())

            elif self.gonna_be_killed:
                killed_location = (self.character.getX() + 1, self.character.getY() - 1)

            kill_character(self.character)
            self.map.update_tiles()
            draw_map(self.map.get_tiles(), self.screen, (Camera.x, Camera.y))

            character_src = pygame.image.load("Characters/Character\\cube.png")
            character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
            self.character = BasicCharacter(character_src, self.character.getX(), self.character.getY())
            self.changeable = True

            if killed_location is not None:
                self.map.add_skull(self.character.type(), killed_location)

    def stay_alive_handler(self):
        if not self.killed:
            if self.character.onGround(self.map.get_tiles()) and not (self.character.getY() == CELLING_HEIGHT or self.character.getY() == FLOOR_HEIGHT):
                self.score += 25
                print("On shelf")
            if self.character.getY() == CELLING_HEIGHT or self.character.getY() == FLOOR_HEIGHT:
                self.score -= 4
                print("On c or f")

            self.camera_end, self.jumping, self.jump_counter, self.falling = self.character.movement(self.map,
                                                                                                     self.camera_end,
                                                                                                     self.jumping,
                                                                                                     self.jump_counter,
                                                                                                     self.falling)

            self.score += 1
        else:
            self.gonna_be_killed = False
            self.killed = False

    def finished_level_handler(self):
        kill_character(self.character)
        self.map.update_tiles()
        draw_map(self.map.get_tiles(), self.screen, (Camera.x, Camera.y))

        character_src = pygame.image.load("Characters/Character\\cube.png")
        character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.character = BasicCharacter(character_src, self.character.getX(), self.character.getY())
        self.changeable = True
