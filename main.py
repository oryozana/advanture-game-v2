import pygame
from Constants import *
from Functions import *
from Characters.Character import *
from pygame import mixer
from Characters.BasicCharacter import *
from Characters.ReversedCharacter import *
from Furniture import *
from Camera import *
mixer.init()


def beginner():
    create_shelves(10, tiles, 4, "R", SHELF_LENGTH, int(MAP_COLS // 2))
    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the easier level"


def advanced():
    create_shelves(15, tiles, 4, "R", SHELF_LENGTH, int(MAP_COLS // 2))
    mixer.music.load("music\\Geometry Dash - Polargeist All Coins.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the advanced level good luck my friend"


def extreme_level():
    create_shelves(15, tiles, 3, "R", SHELF_LENGTH, int(MAP_COLS // 2))
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
map = read_map()
tiles = generate_tiles(map)


def create_menu():
    mixer.music.load("music\\ELECTROMAN ADVENTURES FULL VERSION GEOMETRY DASH 2.11.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    run = True
    clicked = False
    generate_menu(screen, MENU_COLS, MENU_ROWS)
    rects = initiate_menu(screen)
    time = 0

    while not clicked:  # Menu screen
        clock.tick(FPS)
        for event in pygame.event.get():  # close pygame
            if event.type == pygame.QUIT:
                clicked = True
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if mouse_in_button(rects[0], mouse_pos):
                    text = beginner()
                    difficulty = 1
                    clicked = True
                elif mouse_in_button(rects[1], mouse_pos):
                    text = advanced()
                    difficulty = 2
                    clicked = True
                elif mouse_in_button(rects[2], mouse_pos):
                    text = extreme_level()
                    difficulty = 3
                    clicked = True
        if time % 25 == 0:
            update_menu_colors(screen, MENU_COLS, MENU_ROWS)
        time += 1
    return rects, text, difficulty, run


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


rects, text, difficulty, run = create_menu()
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

    if changeable and keys[pygame.K_r]:
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

    camera_end, jumping, jump_counter, falling = character.movement(map, tiles, camera_end, jumping, jump_counter, falling)

    if character.getX() == MAP_ROWS - 2:
        difficulty = next_level(difficulty)

    if isKilled(tiles, character.getX(), character.getY()) or character.getX() == MAP_ROWS - 2 or keys[pygame.K_ESCAPE]:
        kill_character(character)
        tiles = generate_tiles(map)
        draw_map(tiles, screen, (Camera.x, Camera.y))
        character_src = pygame.image.load("Characters/Character\\cube.png")
        character_src = pygame.transform.scale(character_src, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        character = BasicCharacter(character_src, character.getX(), character.getY())
        changeable = True
        if difficulty == 1:
            text = beginner()
        elif difficulty == 2:
            text = advanced()
        elif difficulty == 3:
            text = extreme_level()
        counter = 0
        add_text(screen, text, TEXT_COLOR, X_TEXT_POS, Y_TEXT_POS)
    if not changeable:
        changeable = character.onGround(tiles)

    if difficulty == 4:
        finished = True

    Camera.update()
    screen.fill((0, 0, 0))  # Clear the screen, add another layout
    Camera.draw(screen, tiles, character, text, counter)
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
