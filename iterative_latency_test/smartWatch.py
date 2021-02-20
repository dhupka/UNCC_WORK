import socket
import time
import asyncio
import sys
import csv

#Creating the constants that we are using 
message = "Strong storm coming, pack up and leave, 5 minutes"
HOST = '192.168.0.167' # IP address of server
PORT = 9000
PORT2 = 8001

async def gettingClientConnection(host,port,socket):
	socket.connect((host, port))

async def startingSocketServer(host,port,socket):
    socket.bind((host,port))
    socket.listen()
    return socket

async def acceptingServerSocket(socket):
    conn , address = socket.accept()
    return conn , address

async def recievingDataServer(connection , size):
    data = connection.recv(size)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
    # print("Size of Message: {0}".format(sys.getsizeof(message)))
    #print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO

async def recievingDataServerFirstTime(connection):
    data = connection.recv(1024)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
    connection.sendall(data)
    print("Size of Message: {0}".format(sys.getsizeof(message)))
    print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO
    return sizeOfMessage

def send_msg(connection , msg):
    msg_utf = msg.encode()
    connection.sendall(msg_utf)
    
    
async def send_msg1(connection , msg):
        msg_utf = msg.encode()
        connection.sendall(msg_utf)

async def main():
    print("Starting the server")
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("socket started")

    socket1 = await startingSocketServer(HOST,PORT,s1)
    print("socket waiting")

    connection1 , address1 = await acceptingServerSocket(socket1)
    print(address1)
    iteration = 0	

    while iteration < 100:
        # print("Before first message.")
        time0 = time.time()
        send_msg(connection1 , message)
        print("Sent message to connection 1")
        
        await recievingDataServer(connection1 , 100)
        print("Recieved data from connection 1 ")
        time1 = time.time()
        print(iteration)
        print((time1-time0) * 1000 /2)
        iteration = iteration + 1


    s1.shutdown(socket.SHUT_RDWR)
    s1.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

