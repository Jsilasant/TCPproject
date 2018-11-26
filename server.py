import socket, threading, os
from time import sleep
import time

host, port = '127.0.0.1', 442
   
class transfer():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        self.mysocket.bind((host, port))
        print(' Server is ready ..')
        self.mysocket.listen(3)
        conn, addr = self.mysocket.accept()
        conn.send('This is a test...'.encode())
        
        file_name = 'test.txt'
        size = os.path.getsize(file_name)
        print(' file size : {}'.format(str(size)))
        send_thread = threading.Thread(target = self.send_file, args=(file_name, size, conn, addr, ))
        send_thread.start()

    def send_file(self, file_name, size, conn, addr):
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            conn.send(data)
            while data != bytes(''.encode()):
                #print(data)
                data = file.read(1024)
                conn.send(data)

            print(' File sent successfully.\n')
            
def sleeper():
    while True:
        # Get user input
        num = input('How long to wait: ')
 
        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue
 
        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())


Transfer = transfer()
try:
    sleeper()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()


