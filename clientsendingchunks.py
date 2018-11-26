import socket,sys, threading
import time


host, port = '127.0.0.1', 442

class viewer():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))

    print('Connnected Renderer')
    print(mysocket.recv(16))
    
    def __init__(self):
        data = self.mysocket.recv(64)
        def chunks(lst, n):
            print('Yield successive n-sized chunks from lst')
            for i in xrange(0, len(lst), n):
                yield lst[i:i+n]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, my_port))
ss=StreamSocket(client_socket,Raw)
for chunk in chunks(message, 10):
    print ("sending: " + chunk)
    ss.send(Raw(chunk) )

client_socket.close()
