import sys
import pygame
from game import Game
from menu import Menu
from scoreboard import Scoreboard
from network import Network
pygame.font.init()

def main():
    run = True
    game = Game()
    menu = Menu()
    scoreboard = Scoreboard()
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

    mode = 0

    n = None
    player = -1

    #cursor
    pygame.mouse.set_cursor(pygame.cursors.diamond)

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

        if mode == 0:
            menu.draw(inputs["click_pos"])
            if menu.update(inputs) == "Singleplayer":
                mode = 1
                game.rounds.round_end_time = pygame.time.get_ticks() - 11000
            if menu.update(inputs) == "Multiplayer":
                mode = 2

        elif mode == 1:
            game.draw(0)
            game.update_inputs(inputs, 0)
            game.update()
            if game.is_game_over():
                scoreboard.score = game.score
                mode = 3
                game.reset()

        #MULTIPLAYER NOT WORKING
        elif mode == 2:
            if n == None:
                n = Network()
                player = int(n.getP())

            # try:
                game = n.send("get")
            # except:
            #     mode = 0
            #     print("Couldn't get game")
            #     continue

            game.draw(player)

            if game.is_game_over():
                mode = 0
            
            if game.connected():
                n.send(
                    str(player) + ":" +
                    str(inputs["up"]) + ":" +
                    str(inputs["down"]) + ":" +
                    str(inputs["left"]) + ":" +
                    str(inputs["right"]) + ":" +
                    str(inputs["right"]) + ":" +
                    str(inputs["click_pos"][0]) + ":" +
                    str(inputs["click_pos"][1])
                )

        elif mode == 3:
            scoreboard.draw(inputs["click_pos"])
            if scoreboard.update(inputs) == "MainMenu":
                mode = 0
main()