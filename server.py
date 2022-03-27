import socket, sys, os,random,copy,traceback
from _thread import *
import pickle
from game import Game
import settings
import network

server = network.ip#'10.143.128.116'
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

playerCount = settings.players


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    if gameId in games:
        game = games[gameId]
        game.addPlayer()

    if game.ready:
        game.start()
    
    reply = ""
    endGame = True
    pastSend = None
    while True:
        try:
            data = conn.recv(4096).decode()
            
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    #print(data)
                    if data == "done":
                        print(p, 'is done')
                        if game.checkIfAlive(p):
                            game.playerDone(p)
                        else:
                            print(p,'has been elminated')
                            endGame = False
                            break
                    elif data == "SOLO":
                        game.ready = True
                        game.start()
                    elif data != "get":
                        print('you got data',data)
                        try:
                            game.setState(p, data)
                        except Exception as e:
                            print(str(e))
                    #print(pickle.dumps(game))
                    #conn.sendall(pickle.dumps(game))
                    if data == "get":
                        for i in range(5):
                            try:
                                toSend = game.generateZippedBytes()+b"*"
                                break
                            except Exception as e:
                                print(str(e))
                        if pastSend != toSend:
                            print(toSend)
                            conn.sendall(toSend)
                            pastSend = copy.copy(toSend)
                        else:
                            #conn.sendall(b"SAME")
                            conn.sendall(b"****")
                        """
                        if currentGame.__dict__ != game.__dict__ or :
                            conn.sendall(pickle.dumps(game))
                            currentGame = copy.copy(game)
                        else:
                            conn.sendall(pickle.dumps("SAME"))
                        """
                    else:
                        conn.sendall(pickle.dumps("none"))
                    
            else:
                break
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print('thing')
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            break

    if endGame:
        print("Lost connection", p)
        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass
        idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//(playerCount)
    if idCount % playerCount == 1 or playerCount == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        if playerCount == 1:
            games[gameId].ready = True
    elif idCount % playerCount != 0:
        p = (idCount % playerCount) - 1
    else:
        p = playerCount-1
        games[gameId].ready = True

    print("Assigning to player %s on game %s" % (p, gameId))
    start_new_thread(threaded_client, (conn, p, gameId))
