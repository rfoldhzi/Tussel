import socket
import pickle
import methods
from game import Game
prev = None

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '10.143.128.116'
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()
        self.i = 0

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        global prev
        try:
            self.client.send(str.encode(data))
            r = self.client.recv(2048*2)
            #print(r)
            if len(r) != 19 and len(r) != 4 and len(r) != 14:
                print("bytes:",len(r))
            else:
                return "Nothing"
            """
            self.i+=1
            if self.i%10==0:
                print(r)
                print('bytes', len(r)
            """
            #print(r)
            if r[-1] == 42:
                #print("!!!!!!!!!!")
                r = r.decode("utf-8")
                #print("asuhas",type(r))
                #r = methods.unzipper(r)
                #print("45784598756")
                #print(r)
                return r[:-1]
            else:
                #print("@@@@@@@@@@@@")
                print('RRRrrr',r)
                try:
                    while r[-1] != 42:
                        print("Struggles?")
                        r += self.client.recv(4096)
                        print(r)
                except:
                    return "Nothing"
            r = r.decode("utf-8")
            #r = methods.unzipper(r)
            #print(r)
            n =r.find("*")
            return r[:n]
            return r[:-1]
            
            pick = None
            try:
                """
                print(r)
                r.seek(0)#IDKKKKkkk
                print('okay then',r)
                """
                pick = pickle.loads(r)
            except:
                data = [r]
                while True:
                    print('looped')
                    packet = self.client.recv(4096)
                    #print(packet)
                    #if not packet: break
                    data.append(packet)
                    try:
                        print('stuff')
                        f= b"".join(data)#dfjkdfjdfjdf
                        #print('f',f)
                        #f.seek(0)
                        print('f')
                        pick = pickle.loads(f)
                        print('loaded')
                        #print('pick')
                        break
                    except Exception as e:
                        print('Exception has occered')
                        if str(e) == 'Ran out of input':
                            break
                        print('except',type(e),e)
                        print(str(e))
                        continue
                    print('you wernet supposed to do that')
                print('BROKEN OUT OF LOOP')
            if r == b'':
                return Game()
            else:
                prev = r
                #print('1')
                return pick
        except socket.error as e:
            print('erRor',type(e),e)
            if type(e) == ConnectionAbortedError:
                raise Exception("Disconnect")

