import pygame

import Agent
from Constants import *
from Functions import *
from Characters.Character import *
from pygame import mixer
from Characters.BasicCharacter import *
from Characters.ReversedCharacter import *
from Furniture import *
from Camera import *
from Map import *
from Player import Player

mixer.init()


def beginner_difficulty():
    create_shelves(DEFAULT_SHELF_DISTANCE, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the easier level"


def advanced_difficulty():
    create_shelves(DEFAULT_SHELF_DISTANCE + 5, map.get_tiles(), DEFAULT_SHELF_LENGTH - 1, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level Seven Closed Eyes.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "This is the advanced level good luck my friend"


def extreme_difficulty():
    create_shelves(DEFAULT_SHELF_DISTANCE + 10, map.get_tiles(), DEFAULT_SHELF_LENGTH - 2, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "It's an Impossible level. Are you insane?!"


def ai_difficulty():
    # run to generate a new ai_map:
    # write_map("ai_map.txt", MAP_ROWS, MAP_COLS, BEGINNER_DIFFICULTY)
    # create_shelves(DEFAULT_SHELF_DISTANCE, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))
    # map.add_furniture("Chandelier")
    # map.add_furniture("Mushroom")
    # save_map("ai_map.txt", generate_map_from_tiles(map.get_tiles()))

    # map.add_skulls_to_tiles()

    mixer.music.load("music\\Geometry Dash - Level 1 -Stereo Madness (All Coins).mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    return "It's my turn, let me show you how things get done :)"


def difficulty_handler():
    text = ""

    if map.get_difficulty() == BEGINNER_DIFFICULTY:
        text = beginner_difficulty()
    elif map.get_difficulty() == ADVANCED_DIFFICULTY:
        text = advanced_difficulty()
    elif map.get_difficulty() == EXTREME_DIFFICULTY:
        text = extreme_difficulty()
    elif map.get_difficulty() == AI_DIFFICULTY:
        text = ai_difficulty()

    add_text(screen, text, TEXT_COLOR, X_TEXT_POS, Y_TEXT_POS)
    return 0, text  # counter = 0


pygame.init()
clock = pygame.time.Clock()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Adventure_game")
pygame.display.flip()

map = Map()
# map.add_furniture("Chandelier")
# map.add_furniture("Mushroom")
# create_shelves(10, map.get_tiles(), DEFAULT_SHELF_LENGTH, "R", DEFAULT_SHELF_HEIGHT, int(MAP_COLS // 2))

map.get_tiles()[5][5].getColor()


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
        clock.tick(MENU_FPS)
        for event in pygame.event.get():  # close pygame
            if event.type == pygame.QUIT:
                clicked = True
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if mouse_in_button(rects[0], mouse_pos):
                    map.update_difficulty(BEGINNER_DIFFICULTY)
                    text = beginner_difficulty()
                    clicked = True
                elif mouse_in_button(rects[1], mouse_pos):
                    map.update_difficulty(ADVANCED_DIFFICULTY)
                    text = advanced_difficulty()
                    clicked = True
                elif mouse_in_button(rects[2], mouse_pos):
                    map.update_difficulty(EXTREME_DIFFICULTY)
                    text = extreme_difficulty()
                    clicked = True
                elif mouse_in_button(rects[3], mouse_pos):
                    map.update_difficulty(AI_DIFFICULTY)
                    text = ai_difficulty()
                    clicked = True

                if clicked:
                    add_text(screen, text, TEXT_COLOR, X_TEXT_POS, Y_TEXT_POS)
                    if not mouse_in_button(rects[3], mouse_pos):
                        map.add_furniture("Chandelier")
                        map.add_furniture("Mushroom")

        if time % CHANGE_RATE == 0:
            update_menu_colors(screen, MENU_COLS, MENU_ROWS)
        time += 1
    return rects, text, run


def create_options():
    mixer.music.load("music\\ELECTROMAN ADVENTURES FULL VERSION GEOMETRY DASH 2.11.mp3")
    mixer.music.set_volume(0)
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


def initiate_game(text: str, active_game: bool):
    player = Player(map, screen)

    text_counter = 0

    while active_game:
        clock.tick(FPS)
        for event in pygame.event.get():  # close pygame
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            _, text, _ = create_menu()

        if keys[pygame.K_o]:
            create_options()

        player.reset_just_changed()

        if keys[pygame.K_r]:
            player.reverse_gravity()

        player.isGonnaBeKilled()

        if player.killed or player.gonna_be_killed:
            counter, text = difficulty_handler()

        player.stay_alive_handler()

        if player.character.getX() == MAP_ROWS - 2:
            map.level_up()

        if player.character.getX() == MAP_END or keys[pygame.K_ESCAPE]:
            player.finished_level_handler()
            text_counter, text = difficulty_handler()

        if not player.changeable:
            player.changeable = player.character.onGround(map.get_tiles())

        if map.get_difficulty() == END_GAME_DIFFICULTY:
            return True

        Camera.update()
        screen.fill((0, 0, 0))  # Clear the screen, add another layout
        Camera.draw(screen, map.get_tiles(), player.character, text, text_counter)
        pygame.display.update()  # update the screen
        text_counter += 1


rects, text, run = create_menu()

finished = initiate_game(text, run)

if finished:
    screen.fill(random_color_generator())  # Clear the screen, add another layout
    add_text(screen, "Well played, you won!", (0, 0, 0), 100, 100)
    pygame.display.update()

while finished:
    for event in pygame.event.get():  # close pygame
        if event.type == pygame.QUIT:
            finished = False

# map.update_difficulty(AI_DIFFICULTY)
# agent = Agent.Agent(map, screen)
# agent.train(1000, "third.h5", "Training...")
# agent.test(5, "third.h5", "Testing...")

pygame.quit()
