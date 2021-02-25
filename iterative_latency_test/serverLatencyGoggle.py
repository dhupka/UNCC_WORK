import socket
import time
import asyncio
import sys
import csv

#Creating the constants that we are using 
message = "Strong storm coming, pack up and leave, 5 minutes"
HOST = '192.168.0.167' # IP address of server
PORT = 7000 #Goggles
PORT2 = 8000 #Tablet
PORT3 = 9000 #Watch

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
    #sizeOfMessage = sys.getsizeof(message)
    # print("Size of Message: {0}".format(sys.getsizeof(message)))
    #print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO

def send_msg(connection , msg):
    msg_utf = msg.encode()
    connection.sendall(msg_utf)
    

async def main():    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    socket1 = await startingSocketServer(HOST,PORT,s1)
    # socket2 = await startingSocketServer(HOST,PORT2,s2)
    # socket3 = await startingSocketServer(HOST,PORT3,s3)

    connection1 , address1 = await acceptingServerSocket(socket1)
    print(address1)
    # connection2 , address2 = await acceptingServerSocket(socket2)
    # print(address2)
    # connection3 , address3 = await acceptingServerSocket(socket3)
    # print(address3)

    iteration = 0	
    with open('latency-Goggle-65m.csv','w') as f1:
        writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
        while iteration < 1000:

            print("Before first message.")
            time0 = time.time()
            send_msg(connection1 , message)
            print("Sent message to connection 1")

            # send_msg(connection2 , message)
            # print("Sent message to connection 2 ")
            
            # send_msg(connection3 , message)
            # print("Sent message to connection 3 ")

            await recievingDataServer(connection1 , 100)
            print("Recieved data from connection 1 ")
            # await recievingDataServer(connection2, 100)
            # print("Recieved data from connection 2 ")
            # await recievingDataServer(connection3, 100)
            # print("Recieved data from connection 3 ")
            rtt = ((time.time() - time0) * 1000)/2
            print("Total Latency: {:.2f} ms".format(rtt))
            row = [rtt]
            writer.writerow(row)
            iteration = iteration + 1
            print(iteration)

        s1.shutdown(socket.SHUT_RDWR)
        s1.close()
        # s2.shutdown(socket.SHUT_RDWR)
        # s2.close()
        # s3.shutdown(socket.SHUT_RDWR)
        # s3.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

