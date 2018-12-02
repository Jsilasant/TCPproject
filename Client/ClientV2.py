from socket import *
import sys
import os

serverName = "localhost"
serverPort = 48999
clientSocket = socket(AF_INET, SOCK_STREAM)
#clienttoRender = socket(AF_INET, SOCK_STREAM)
# open the TCP connection
clientSocket.connect((serverName, 48997))
#clienttoRender.connect((serverName, 48998))

print("Connected. Type !help for command list:\n")
path = ("./")
files = [f for f in os.listdir('.') if os.path.isfile(f)]

while 1:
  sentence = input('>') # input for windows / raw_input for unix

  # split string to check for meaningful commands
  _check = sentence.split(" ", 1)

  #commands processed locally:
  # user calls !help
  if(sentence=="!help"):
    print ("Available commands:\n"+
           "!help          : list available commands\n"+
           "ls-local       : list local files\n"+
           "ls-remote      : list remote files\n"+
           "play 'filename': play remote file to Renderer\n"+
           "Functions: used for Renderer. \n"+
           "resume         : Resumes Renderer after paused \n" +
           "pause          : Pauses Renderer \n" +
           #"playback       : Makes user replay file \n " +
           "exit           : terminates program")

  # user calls ls-local
  elif(sentence=="ls-local"):
    # refresh file list
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print("local files:")
    for f in files:
      fileSize = os.path.getsize(f)
      print("-> "+f+"\t%d bytes" % fileSize)

  # user calls exit
  elif(sentence=="exit"):
    break

  # user calls ls-remote
  elif(sentence=="ls-remote"):
    clientSocket.sendto(sentence.encode(),(serverName, serverPort))
    modifiedSentence = clientSocket.recv(1024)
    modifiedSentence = modifiedSentence.decode('utf-8')
    print(modifiedSentence)
  #user commands after user plays file
  elif(sentence=="resume"):
    clientSocket.sendto(sentence.encode(),(serverName, serverPort))
  elif (sentence == "pause"):
    clientSocket.sendto(sentence.encode(), (serverName, serverPort))
  elif (sentence == "playback"):
    print('Playing back, ask the server to play the file again.')
    clientSocket.sendto(sentence.encode(), (serverName, serverPort))
  #commands processed remotely:
  elif(len(_check)==2):
    if(_check[0].lower()=="play"):
            #----PLAY----#
      # for PLAY we send the string and wait for server's response
      if(_check[0]=='play'):
        clientSocket.sendto(sentence.encode(),(serverName, 48997))
        modifiedSentence = clientSocket.recv(1024)
        modifiedSentence = modifiedSentence.decode('utf-8')
        print(modifiedSentence)
       
        # check server's response
        #modifiedSentence == 'True'
        if(modifiedSentence == 'True'): # file found
          print('OK. Sending to Renderer!')

        elif(modifiedSentence == 'False'): # file not found
          print(modifiedSentence)
          print('File requested not available in remote dir.')

      #clientSocket.sendto(sentence.encode(),(serverName, serverPort))
      #modifiedSentence = clientSocket.recv(1024)
      #print(modifiedSentence)
    else:
      # multiple invalid strings
      print("[invalid command]")
  else:
    # single invalid string
    print("[invalid command]")

# close the TCP connection
clientSocket.close()
