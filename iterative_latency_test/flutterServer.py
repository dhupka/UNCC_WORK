import socket
import time
import asyncio
import sys
import csv
import random


#Creating the constants that we are using 
message = "Strong storm coming, pack up and leave, 5 minutes"
HOST = '192.168.0.167' # IP address of server
PORT = 8000
PORT2 = 9000

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
    return message
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

def sendRisk(connection , msg):
    msgUTF = str(msg).encode()
    connection.sendall(msgUTF)
    
    
    
async def send_msg1(connection , msg):
        msg_utf = msg.encode()
        connection.sendall(msg_utf)

async def main():
    print("Starting the server")
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("socket started1")

    socket1 = await startingSocketServer(HOST,PORT,s1)

    connection1 , address1 = await acceptingServerSocket(socket1)
    print(address1)
    iteration = 0	
    
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("socket started1")

    socket2 = await startingSocketServer(HOST,PORT2,s2)
    print("socket waiting")

    connection2 , address2 = await acceptingServerSocket(socket2)
    print(address2)

    while True:
        # print("Before first message.")
        time.sleep(1)
        time0 = time.time()
        risk = round(random.random()*10,2)
        sendRisk(connection1 , risk)
        sendRisk(connection2 , risk)

        print(risk)
        # msg = await recievingDataServer(connection2 , 100)
        time1 = time.time()
        print((time1-time0) * 1000 /2)

    s1.shutdown(socket.SHUT_RDWR)
    s1.close()
    s2.shutdown(socket.SHUT_RDWR)
    s2.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

