import socket
import sys
import os
import select
import re
import time
import threading
from threading import Thread
import _thread


        
#path = ("./")
# fileList = []
#_lsremote = ("ls-remote")
#files = [f for f in os.listdir('.') if os.path.isfile(f)]
 
HOST = 'localhost'   # Hostname
PORT = 48997 # port
PORT2 = 48996 # port2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Sockets created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    socketRender.bind((HOST, PORT2))
except (socket.error):
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print ('Socket(s) bind complete')
 
#Start listening on socket
s.listen(1)
socketRender.listen(1)
print ('SocketRender is now listening')
print ('Socket now listening')
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    #conn.send('Connected, type !help for command list:\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        # data will be split with a space.
        _data = data.decode().split(" ", 1)

        #----ls-remote----#
        if(_data[0] == 'ls-remote'):
            # refresh file list
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            print('User: '+addr[0]+':'+str(addr[1])+' requested ls-remote')
            remoteList = 'remote files:'
            for f in files:
                fileSize = os.path.getsize(f)
                remoteList += ("| "+f+"-> %d bytes" % fileSize)
            conn.sendall(remoteList.encode())



        #----PLAY----#
        elif(_data[0] == 'play'):
            _found = False # flag in case file is not found
            print('User: '+addr[0]+':'+str(addr[1])+' requested a Play for: %s' % _data[1])
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                #--- file requested found ---#
                if(f == _data[1]):
                    _found = True
                    print('File found. Sending file content to Renderer.')
                    # send 'found' flag to Everybody
                    reply = str(_found)
                    conn.sendall(reply.encode())

                    # get file size and send it to Renderer
                    with open(f) as file:
                        lines = file.readlines()
                        response = ""
                       # if (response != '' )
                        for x in range(0, 3):
                            response += lines[x]
                        connect.sendto(response.encode(), (HOST, 48998))

                #if(lines == EOF)
                        #print('File has ended')
                        #message = ('File has ended')
                        #s.sendto(message.encode(),(serverName,48998))
                        # file.close()
            
            #--- file requested not found ---#
            if(_found == False):
                print('File requested not available in dir.')
                reply = str(_found)
                conn.sendall(reply.encode())

            #reply = 'OK...' + data
            #conn.sendall(reply)
            #break
        else:
            print(data)
            reply = ('OK...' + data.decode())
            conn.sendall(reply.encode())

        if not data: 
            break
        # conn.sendall(reply)
     
    #came out of loop
    print ('User: '+addr[0]+':'+str(addr[1])+' disconnected')
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    connect, address = socketRender.accept()
    print('Connected with ' + address[0] + ':' + str(address[1]))
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    _thread.start_new_thread(clientthread,(conn,))
    #_thread.start_new_thread(renderthread, (connect,))
 
s.close()
