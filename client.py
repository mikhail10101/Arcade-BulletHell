import sys
import pygame
from game import Game
from menu import Menu
from scoreboard import Scoreboard
from waiting import Waiting
from network import Network
from interface import generate_cursor

pygame.init()
pygame.font.init()

LENGTH = 1440
WIDTH = 810

def main():
    window = pygame.display.set_mode((LENGTH, WIDTH))
    pygame.display.set_caption("Arcade")

    run = True
    game = Game()
    menu = Menu()
    scoreboard = Scoreboard()
    waiting = Waiting()
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
    cursor_surf = generate_cursor()
    custom = pygame.cursors.Cursor((10, 10), cursor_surf)
    pygame.mouse.set_cursor(custom)
    #pygame.mouse.set_visible(False)

    while run:
        clock.tick(60)
        inputs["mouse_down"] = False
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
                inputs["mouse_down"] = True
                inputs["click"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                inputs["click"] = False

        inputs["click_pos"] = pygame.mouse.get_pos()

        match mode:
            case 0:
                menu.draw(window, inputs["click_pos"])
                if menu.update(inputs) == "Singleplayer":
                    mode = 1
                    game.rounds.round_end_time = pygame.time.get_ticks() - 10000
                if menu.update(inputs) == "Multiplayer":
                    mode = 2

            case 1:
                game.draw(window, 0)
                game.time_update()
                game.update_inputs(inputs, 0)
                game.client_update()
                game.client_update_shapes()
                game.update_color()
                game.update()
                if game.is_game_over():
                    scoreboard.score = game.score
                    mode = 3
                    game = Game()

            #MULTIPLAYER
            case 2:
                if n == None:
                    n = Network()
                    player = int(n.getP())
                    game = Game()
                    game.player_pers = player
                    print("You are player", player)

                try:
                    info = n.send("get")

                    game.ready = info["ready"]
                    game.player_container = info["player_container"]
                    game.bullet_container = info["bullet_container"]
                    game.rounds.shape_container = info["rounds.shape_container"] 
                    game.rounds.round_number = info["rounds.round_number"]
                    game.rounds.mode = info["rounds.mode"]
                    game.rounds.round_end_time = info["rounds.round_end_time"]
                    game.particles = info["particles"] 
                    game.emps = info["emps"]
                    game.charge_bar = info["charge_bar"]
                    game.screen_shake = info["screen_shake"] 
                    game.score = info["score"] 
                    game.game_color = info["game_color"] 
                    game.time = info["time"]
                    game.update_shape_positions(info["shape_positions"])

                    game.client_update_shapes()

                except:
                    mode = 0
                    n = None
                    game = Game()
                    print("Couldn't get game")
                    continue

                if game.connected():
                    game.client_update()
                    game.update_inputs(inputs, player)
                    game.draw(window, player)
                else:
                    waiting.draw(window)

                if game.is_game_over():
                    scoreboard.score = game.score
                    mode = 3
                    n = None
                    game = Game()
                    continue
                
                if game.connected():
                    n.send(
                        str(player) + ":" +
                        str(inputs["up"]) + ":" +
                        str(inputs["down"]) + ":" +
                        str(inputs["left"]) + ":" +
                        str(inputs["right"]) + ":" +
                        str(inputs["click"]) + ":" +
                        str(inputs["click_pos"][0]) + ":" +
                        str(inputs["click_pos"][1])
                    )
                    # game.ready = info["ready"]
                    # game.player_container = info["player_container"]
                    # game.bullet_container = info["bullet_container"]
                    # game.rounds.shape_container = info["rounds.shape_container"] 
                    # game.rounds.round_number = info["rounds.round_number"]
                    # game.rounds.mode = info["rounds.mode"]
                    # game.rounds.round_end_time = info["rounds.round_end_time"]
                    # game.particles = info["particles"] 
                    # game.emps = info["emps"]
                    # game.charge_bar = info["charge_bar"]
                    # game.screen_shake = info["screen_shake"] 
                    # game.score = info["score"] 
                    # game.game_color = info["game_color"] 
                    # game.time = info["time"]

                    # game.client_update_shapes()

            case 3:
                scoreboard.draw(window, inputs["click_pos"])
                if scoreboard.update(inputs) == "MainMenu":
                    mode = 0

            case _:
                pass
        pygame.display.update()
main()