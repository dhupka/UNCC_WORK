import socket
import time
import asyncio
import sys
import csv

#Creating the constants that we are using 
message = "Your wristband out of charge, recharge it now"
HOST = '192.168.0.167' # IP address of server
PORT = 9700
PORT2 = 8886

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
    # while True:
    data = connection.recv(size)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
    return time.time()
    # print("Size of Message: {0}".format(sys.getsizeof(message)))
    # print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO

async def recievingDataServerFirstTime(connection):
    data = connection.recv(1024)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
    connection.sendall(data)
    print("Size of Message: {0}".format(sys.getsizeof(message)))
    print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO
    return sizeOfMessage

async def send_msg(connection , msg):
    msg_utf = msg.encode()
    connection.sendall(msg_utf)
    return time.time()

async def main():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
    socket1 = await startingSocketServer(HOST,PORT,s1)
    socket2 = await startingSocketServer(HOST,PORT2,s2)

    connection1 , address1 = await acceptingServerSocket(socket1)
    print(address1)
    connection2 , address2 = await acceptingServerSocket(socket2)
    print(address2)

    iteration = 0	
    with open('latency.csv','w') as f1:
        writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
        while iteration < 500:
            if iteration == 0:
                await send_msg(connection1 , message)
                print('Message Sent socket 1 first time')
                sizeMessage1 = await recievingDataServerFirstTime(connection1)
                print('Message received socket 1 first time')
                await send_msg(connection2 , message)
                print('Message Sent socket 2 first time')
                sizeMessage2 = await recievingDataServerFirstTime(connection2)
                print('Message received socket 2 time ')
                iteration = iteration + 1
            else:
                #  = time.time()
                time0 = await send_msg(connection1 , message)
                #print('Message Sent sock 1 ')
                time1 = await recievingDataServer(connection1 , sizeMessage1)
                #print('Message receive sock 1 ')		
                rtt1 = ((time1 - time0) * 1000)/2
                print("Total Latency1: {:.2f} ms".format(rtt1))
                time2 = await send_msg(connection2 , message)
                #print('message sent sock 2 ')
                time3 = await recievingDataServer(connection2, sizeMessage2)
                #print('message receieve sock 2')		
                rtt2 = ((time3 - time2) * 1000)/2
                print("Total Latency2: {:.2f} ms".format(rtt2))
                #row = [rtt]
                #writer.writerow(row)
                iteration = iteration + 1
                print(iteration)

        s1.shutdown(socket.SHUT_RDWR)
        s1.close()
        s2.shutdown(socket.SHUT_RDWR)
        s2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

