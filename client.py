import sys
import pygame
from game import Game
from menu import Menu
pygame.font.init()

LENGTH = 1440
WIDTH = 810

def main():
    run = True
    game = Game(LENGTH, WIDTH)
    menu = Menu(LENGTH, WIDTH)
    clock = pygame.time.Clock()
    
    #Inputs to be passed to the game
    inputs = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "click": False,
        "click_pos": [0,0]
    }

    main_menu = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    inputs["up"] = True
                if event.key == pygame.K_s:
                    inputs["down"] = True
                if event.key == pygame.K_a:
                    inputs["left"] = True
                if event.key == pygame.K_d:
                    inputs["right"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    inputs["up"] = False
                if event.key == pygame.K_s:
                    inputs["down"] = False
                if event.key == pygame.K_a:
                    inputs["left"] = False
                if event.key == pygame.K_d:
                    inputs["right"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                inputs["click"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                inputs["click"] = False

        inputs["click_pos"] = pygame.mouse.get_pos()

        if main_menu:
            menu.draw()
            if menu.update(inputs):
                main_menu = False
                game.rounds.round_end_time = pygame.time.get_ticks() - 10000

        else:
            game.draw()
            game.update(inputs)

main()