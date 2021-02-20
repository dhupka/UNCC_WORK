# A way to send (and recieve for now ) AT INTERVAL
# May need to lock data so that one thread cant overwrite data of other thread when in parallel ---
# Ensure we arent losing anything, locking with purpose of protection
#Only using one port and one socket, as threading is purpose of ensuring we can do this all on one

import socket
from _thread import *
import threading
import sys
import csv
import time

#Creating the constants that we are using 
message = "LONG WARNING NUMBER"
HOST = '192.168.0.167' # IP address of server
PORT = 8000
threadCount = 0
#Initialize socket, and option to reuse port
serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

serverSocket.bind((HOST,PORT))

#After connection established, send danger number to client 
def threadedClient(connection):
    #This may need to be an infinite loop to always be sending our messages to various clients
    #or a loop that will send this message after a sleep/wait to client
    #Everytime the message is sent at X interval it needs to be a different warning - for loop, generate random number, ensure it is different
    connection.send(str.encode("Server is working: "))  #Sending danger number 
    i=0
    while i < 1000:
        data = connection.recv(1024)
        message = data.decode('utf-8' , 'replace')
        print("Received Message: ", message[2:])
        print(i)
        i += 1
        connection.sendall(message.encode())
    print('Done with that thread')
    # Recieve back initial danger number the server sent to the client -> possibly do error handling to ensure this message is the same (?)
    # data = connection.recv(1024)
    # message = data.decode('utf-8', 'replace')
    # print ("ACK MESSAGE FROM CLIENT: ", message[2:])
    connection.close()


print('Server started')
print('Socket Listening...')
serverSocket.listen(5) # Queue of connections

#Spins infinitely accepting addresses "concurrently", and will open a new thread per new client connection -> runs threaded client function
while True: 
    client, address = serverSocket.accept()
    print('Connected to: ' + address[0] + ":" + str(address[1]))
    start_new_thread(threadedClient, ((client,)))
    print("Thread Count: " + str(threadCount))
    threadCount += 1
serverSocket.close()
serverSocket.shutdown(socket.SHUT_RDWR)