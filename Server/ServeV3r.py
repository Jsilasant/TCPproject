import socket
import sys
import os
import select
import re
import time
import threading
from threading import Thread
import _thread
from subprocess import STDOUT, check_output
import multiprocessing


        
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
        rawData = conn.recv(1024)
        # rawData will be split with a space.
        data = rawData.decode().split(" ", 1)
        command = data[0]
        requestedFilename = data[1] if (len(data) > 1) else ""
        found = False

        #----ls-remote----#
        if(command == 'ls-remote'):
            # refresh file list
            files = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
            print('User: '+addr[0]+':'+str(addr[1])+' requested ls-remote')
            remoteList = 'remote files:'
            for currentFile in files:
                fileSize = os.path.getsize(currentFile)
                remoteList += ("| "+currentFile+"> %d bytes" % fileSize)
            conn.sendall(remoteList.encode())



        #----PLAY----#
        elif(command == 'play'):
            found = False # flag in case file is not found
            print('User: '+addr[0]+':'+str(addr[1])+' requested a Play for: %s' % requestedFilename)
            files = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
            for currentFile in files:
                #--- file requested found ---#
                if(currentFile == requestedFilename):
                    found = True
                    print('File found. Sending file content to Renderer.')
                    # send 'found' flag to Everybody
                    playFilereply = str(found)
                    conn.sendall(playFilereply.encode())
                    # --- file requested not found ---#
            if (found == False):
                print('File requested not available in dir.')
                notFoundreply = str(found)
                conn.sendall(notFoundreply.encode())

        if found == True:
            with open(requestedFilename) as file:
                playcommand='play'
                line = file.readline()
                while(command == 'play') & (found == True):
                    if playcommand == 'pause':
                        time.sleep(3)
                    elif playcommand == "resume" or playcommand == 'play':
                        if file.readable():
                            connect.sendto(line.encode(), (HOST, 48998))
                            time.sleep(3)
                            line = file.readline()
                            print("Line sent Successfully!")
                        else:
                            print('File contents sent successfully')
                            command=''
                            break
                    #elif playcommand == "playback":
                           #print('playback is happening')
                           # break
                    ready = select.select([conn], [], [], 2)
                    if ready:
                        conn.settimeout(2)
                        try:
                            rawData = conn.recv(1024)
                        except:
                            continue
                    playcommand = rawData.decode().split(" ", 1)[0]

        if not rawData:
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
