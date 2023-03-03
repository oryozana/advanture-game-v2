import pygame
from Constants import *
from Functions import *
from Characters.Character import *
from pygame import mixer
from Characters.BasicCharacter import *
from Characters.ReversedCharacter import *
from Furniture import *
from Camera import *
from Map import *
mixer.init()


def beginner():
    create_shelves(10, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the easier level"


def advanced():
    create_shelves(15, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level Seven Closed Eyes.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the advanced level good luck my friend"


def extreme_level():
    create_shelves(15, map.get_tiles(), DEFAULT_SHELF_LENGTH - 1, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "It's an Impossible level. are you insane?!"


pygame.init()
clock = pygame.time.Clock()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Adventure_game")
pygame.display.flip()

map = Map()
map.add_furniture("Chandelier")
map.add_furniture("Mushroom")
create_shelves(10, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))


def create_menu():
    mixer.music.load("music\\ELECTROMAN ADVENTURES FULL VERSION GEOMETRY DASH 2.11.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()

    run = True
    clicked = False
    generate_menu(screen, MENU_COLS, MENU_ROWS)
    rects = initiate_menu(screen)
    time = 0
    text = ""

    while not clicked:  # Menu screen
        clock.tick(FPS)
        for event in pygame.event.get():  # close pygame
            if event.type == pygame.QUIT:
                clicked = True
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if mouse_in_button(rects[0], mouse_pos):
                    map.update_difficulty(1)
                    text = beginner()
                    clicked = True
                elif mouse_in_button(rects[1], mouse_pos):
                    map.update_difficulty(2)
                    text = advanced()
                    clicked = True
                elif mouse_in_button(rects[2], mouse_pos):
                    map.update_difficulty(3)
                    text = extreme_level()
                    clicked = True

                if clicked:
                    map.add_furniture("Chandelier")
                    map.add_furniture("Mushroom")

        if time % 25 == 0:
            update_menu_colors(screen, MENU_COLS, MENU_ROWS)
        time += 1
    return rects, text, run


def create_options():
    mixer.music.load("music\\ELECTROMAN ADVENTURES FULL VERSION GEOMETRY DASH 2.11.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    clicked = False
    screen.fill((255, 255, 255))

    add_text(screen, "Keys and what they do:", TEXT_COLOR, TEXT_X_SPACE, TEXT_Y_SPACE)
    add_text(screen, "Space key ---> jump", TEXT_COLOR, TEXT_X_SPACE, TEXT_Y_SPACE + TEXT_Y_SPACE)
    add_text(screen, "R key ---> reverse gravity", TEXT_COLOR, TEXT_X_SPACE, TEXT_Y_SPACE + TEXT_Y_SPACE * 2)
    add_text(screen, "Esc key ---> Open difficulty menu", TEXT_COLOR, TEXT_X_SPACE, TEXT_Y_SPACE + TEXT_Y_SPACE * 3)
    add_text(screen, "O key ---> Open options", TEXT_COLOR, TEXT_X_SPACE, TEXT_Y_SPACE + TEXT_Y_SPACE * 4)
    pygame.display.flip()

    while not clicked:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clicked = True


rects, text, run = create_menu()
character_src = pygame.image.load("Characters/Character\\cube.png")  # / - Folder, \\ - File
character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
character = BasicCharacter(character_src, X_POSITION, Y_POSITION)

jumping = False
jump_counter = 0
falling = False
camera_end = CAMERA_X_END
killed = False
changeable = True
finished = False
counter = 0

while run and not finished:
    clock.tick(FPS)
    for event in pygame.event.get():  # close pygame
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        create_menu()

    if keys[pygame.K_o]:
        create_options()

    just_changed = False
    just_changed_from = character.type()

    if changeable and keys[pygame.K_r]:
        just_changed = True
        just_changed_from = character.type()

        if character.type() == "B":
            character_src = pygame.image.load("Characters/Character\\cubeReversed.png")
            character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
            character = ReversedCharacter(character_src, character.getX(), character.getY())
            changeable = False

        elif character.type() == "R":
            character_src = pygame.image.load("Characters/Character\\cube.png")
            character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
            character = BasicCharacter(character_src, character.getX(), character.getY())
            changeable = False

    killed, gonna_be_killed = isGonnaBeKilled(character, jumping, falling, map.get_tiles())

    if killed or gonna_be_killed:
        if just_changed:
            match just_changed_from:
                case "B":
                    character = BasicCharacter(character_src, character.getX(), character.getY())
                case "R":
                    character = ReversedCharacter(character_src, character.getX(), character.getY())

        if killed and not gonna_be_killed:
            if character.type() == "B":
                killed_location = (character.getX() + 1, character.getY() - 2)
            elif character.type() == "R":
                killed_location = (character.getX() + 1, character.getY())

        elif gonna_be_killed:
            killed_location = (character.getX() + 1, character.getY() - 1)

        kill_character(character)
        map.update_tiles()
        draw_map(map.get_tiles(), screen, (Camera.x, Camera.y))
        map.add_furniture("Chandelier")
        map.add_furniture("Mushroom")
        character_src = pygame.image.load("Characters/Character\\cube.png")
        character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        character = BasicCharacter(character_src, character.getX(), character.getY())
        changeable = True

        map.add_skull(character.type(), killed_location)

        if map.get_difficulty() == 1:
            text = beginner()
        elif map.get_difficulty() == 2:
            text = advanced()
        elif map.get_difficulty() == 3:
            text = extreme_level()

        counter = 0
        add_text(screen, text, TEXT_COLOR, X_TEXT_POS, Y_TEXT_POS)

    if not killed:
        camera_end, jumping, jump_counter, falling = character.movement(map, camera_end, jumping, jump_counter, falling)
    else:
        gonna_be_killed = False
        killed = False

    if character.getX() == MAP_ROWS - 2:
        map.level_up()

    if character.getX() == MAP_END or keys[pygame.K_ESCAPE]:
        kill_character(character)
        map.update_tiles()
        draw_map(map.get_tiles(), screen, (Camera.x, Camera.y))
        map.add_furniture("Chandelier")
        map.add_furniture("Mushroom")
        character_src = pygame.image.load("Characters/Character\\cube.png")
        character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        character = BasicCharacter(character_src, character.getX(), character.getY())
        changeable = True

        if map.get_difficulty() == 1:
            text = beginner()
        elif map.get_difficulty() == 2:
            text = advanced()
        elif map.get_difficulty() == 3:
            text = extreme_level()

        counter = 0
        add_text(screen, text, TEXT_COLOR, X_TEXT_POS, Y_TEXT_POS)

    if not changeable:
        changeable = character.onGround(map.get_tiles())

    if map.get_difficulty() == 4:
        finished = True

    Camera.update()
    screen.fill((0, 0, 0))  # Clear the screen, add another layout
    Camera.draw(screen, map.get_tiles(), character, text, counter)
    pygame.display.update()  # update the screen
    counter += 1

screen.fill(random_color_generator())  # Clear the screen, add another layout
add_text(screen, "Well played, you won!", (0, 0, 0), 100, 100)
pygame.display.update()
while finished:
    for event in pygame.event.get():  # close pygame
        if event.type == pygame.QUIT:
            finished = False

pygame.quit()
