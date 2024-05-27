import socket
from _thread import *
import pickle
from game import Game

server = "192.168.68.127" #change
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")

games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096**3).decode()
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        arr = data.split(":")
                        inputs = {
                            "up": arr[1] == True,
                            "down": arr[2] == True,
                            "left": arr[3] == True,
                            "right": arr[4] == True,
                            "click": arr[5] == True,
                            "click_pos": [int(arr[6]), int(arr[7])],
                        }
                        game.update_inputs(inputs, int(arr[0]))
                    
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
        p = 1

    start_new_thread(threaded_client, (conn,p,gameId))