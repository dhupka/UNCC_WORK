# A way to send (and recieve for now ) AT INTERVAL
# May need to lock data so that one thread cant overwrite data of other thread when in parallel ---
# Ensure we arent losing anything, locking with purpose of protection
#Only using one port and one socket, as threading is purpose of ensuring we can do this all on one

#For PSR if possible get latency testing of this multithreaded implementation (single socket, single port, mutli thread) 
#compare with latencies of two port, two socket, single thread iterative latency testing

#Sending/Receiving are individual threads, not just for the client.

import socket
from _thread import *
import threading
import sys
import csv
import time

#Creating the constants that we are using 
HOST = '192.168.0.167' # IP address of server
PORT = 9000
threadCount = 0
#Initialize socket, and option to reuse port
serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

serverSocket.bind((HOST,PORT))


def threadedSend(connection):
    ## While true ( or sleep time)
    connection.send(str.encode("Server is working: "))
    i=0
    while i < 1000:
        message = "LONG WARNING NUMBER"
        print(i)
        i += 1
        connection.sendall(str.encode(message))
    print("Send thread is finished.")


def threadedReceive(connection):
    i=0
    print ("starting asojdbf")
    while i < 1000:
        data = connection.recv(1024)
        message = data.decode('utf-8' , 'replace')
        print("Received Message: ", message[2:])
        print(i)
        i += 1
    print("Receive thread is finished.")
    
print('Server started')
print('Socket Listening...')
serverSocket.listen(5) # Queue of connections


while True: 
    print (threading.active_count())
    client, address = serverSocket.accept()
    print('Connected to: ' + address[0] + ":" + str(address[1]))
    start_new_thread(threadedSend, ((client,)))
    start_new_thread(threadedReceive, ((client,)))
    #print("Thread Count: " + str(threadCount))
    threadCount += 1
    
serverSocket.close()
serverSocket.shutdown(socket.SHUT_RDWR)