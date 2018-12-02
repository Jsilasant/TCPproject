from socket import *
import sys
import os

serverName = "localhost"
serverPort = 48998
#RenderPort = 48995
RenderSocket = socket(AF_INET, SOCK_STREAM)
#ClientRecv = socket(AF_INET, SOCK_STREAM)
#ClientRecv.bind((serverName, RenderPort))
#ClientRecv.listen(1)

RenderSocket.connect((serverName, 48996))
print('Renderer has connected!')
while 1:
    #input = RenderSocket.recv(1024)
    lines = RenderSocket.recv(1024)
    lines = lines.decode('utf-8')
    print(lines)
   # if (input == 'pause'):
    #    print('im trying to pause')

