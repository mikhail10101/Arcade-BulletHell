import socket
from _thread import *
import pickle
from game import Game

import pygame

pygame.init()

clock = pygame.time.Clock()

server = "10.195.221.99" #change
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for connection, Server Started")

games = {}
idCount = 0

def game_update(id):
    while True:
        clock.tick(60)
        games[id].update()

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    setup = False

    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]

                try:
                    if (not setup) and p==0:
                        start_new_thread(game_update, (gameId,))
                        setup = True
                except Exception as error:
                    print(error)

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        arr = data.split(":")
                        inputs = {
                            "up": arr[1] == "True",
                            "down": arr[2] == "True",
                            "left": arr[3] == "True",
                            "right": arr[4] == "True",
                            "click": arr[5] == "True",
                            "click_pos": [int(arr[6]), int(arr[7])],
                        }
                        game.update_inputs(inputs, int(arr[0]))

                    # info = {
                    #     "ready": game.ready,
                    #     "player_container": game.player_container,
                    #     "bullet_container": game.bullet_container,
                    #     "rounds": game.rounds,
                    #     "particles": game.particles,
                    #     "emps": game.emps,
                    #     "charge_bar": game.charge_bar,
                    #     "screen_shake": game.screen_shake,
                    #     "score": game.score,
                    #     "game_color": game.game_color
                    # }
                    conn.sendall(pickle.dumps(game))
            else:
                break

        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass

    #I think this should be removed
    idCount -= 1 
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    idCount += 1
    p = 0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating new game...")
    else:
        games[gameId].ready = True
        games[gameId].rounds.round_end_time = pygame.time.get_ticks() - 10000
        p = 1

    start_new_thread(threaded_client, (conn,p,gameId))