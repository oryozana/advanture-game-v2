from Constants import *
import Functions


class Camera:
    x = 0
    y = 0

    def update():
        pass

    def __draw_map(screen, tiles):
        Functions.draw_map(tiles, screen, (Camera.x, Camera.y))

    def __draw_player(screen, character):
        screen.blit(character.getImageSrc(), (character.getX() * SCALE - Camera.x, character.getY() * SCALE - Camera.y))

    def draw(screen, tiles, character, text, counter):
        Camera.x = character.getX() * SCALE - SCREEN_WIDTH / 2  # Camera.x is already scaled so you don`t need to scale it later on
        Camera.__draw_map(screen, tiles)
        Camera.__view_text(screen, text, counter)
        Camera.__draw_player(screen, character)

    def reset():
        x = 0
        y = 0

    def __view_text(screen, text, counter):
        if counter < 100:
            Functions.add_text(screen, text, (0, 0, 0), 100, 75)
