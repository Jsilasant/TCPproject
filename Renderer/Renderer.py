from socket import *
import sys
import os

serverName = "localhost"
serverPort = 48998
RenderSocket = socket(AF_INET, SOCK_STREAM)

RenderSocket.connect((serverName, 48996))
print('Renderer has connected!')
while 1:
    print('Im in the while loop')
    lines = RenderSocket.recv(1024)
    lines = lines.decode('utf-8')
    print(lines)
    #if( lines == True):
        #print(lines)

        
    #elif( lines == False):
        #print('Cannot read file! Please request a different one.')
        
