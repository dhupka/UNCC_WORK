import socket
import time
import asyncio
import sys
import csv
import constants


  static message = ""
  


function communication 
if(!message.equals(""))
await sendData()
message = await recieveData()
    sendData()





async def gettingClientConnection(host,port,socket):
	socket.connect((host, port))


async def startingSocketServer(host,port,socket):
    socket.bind((host,port))
    socket.listen()
	# conn , addr = socket.accept()
	# return conn , addr
    return socket

async def acceptingServerSocket(socket):
    conn , address = socket.accept()
    return conn , address


async def recievingDataServer(connection , size):
    # while True:
    data = connection.recv(size)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
        # if not data:
        #     break
    connection.sendall(data)
    print("Size of Message: {0}".format(sys.getsizeof(message)))
    print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO

async def recievingDataServerFirstTime(connection):
    # while True:
    data = connection.recv(1024)
    message = data.decode('utf-8' , 'replace')
    sizeOfMessage = sys.getsizeof(message)
        # if not data:
        #     break
    connection.sendall(data)
    print("Size of Message: {0}".format(sys.getsizeof(message)))
    print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO
    return sizeOfMessage
	#return message

async def send_msg(connection):
	msg = "Your wristband out of charge, recharge it now"
	msg_utf = msg.encode()
	connection.sendall(msg_utf)

	#print("Size of Message: {0}".format(sys.getsizeof(msg_utf)))

async def gettingDataBack(socket):
	data = socket.recv(1024)
	message = data.decode('utf-8','replace')
	print("Size of Message: {0}".format(sys.getsizeof(message)))
	print("Received Message: ", message[2:]) #Removing tab and ascii character that is added for some reason TODO
	#return message
	


async def main():
    HOST = '192.168.0.167' # IP address of server
    PORT = 9702
    PORT2 = 8886


    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# await gettingClientConnection(HOST, PORT, s)
    socket1 = await startingSocketServer(HOST,PORT,s1)
    #socket2 = await startingSocketServer(HOST,PORT2,s2)

    connection1 , address1 = await acceptingServerSocket(socket1)
    print(address1)
    #connection2 , address2 = await acceptingServerSocket(socket2)
    #print(address2)
	#Starting timer at connection to server
    iteration = 0	
	#Sending message to server
    with open('latency.csv','w') as f1:
        writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
        
        while iteration < 500:
            if iteration == 0:
                await send_msg(connection1)
                #sizeMessage1 = await recievingDataServerFirstTime(connection1)
                #await send_msg(connection2)
                #sizeMessage2 = await recievingDataServerFirstTime(connection2)
                iteration = iteration + 1
            else:
                time0 = time.time()
                await send_msg(connection1)
                time1 = time.time()
                #await recievingDataServer(connection1 , sizeMessage1)		
                time2 = time.time()
                rtt1 = ((time2 - time0) * 1000)/2
                print("Total Latency1: {:.2f} ms".format(rtt1))
                # await send_msg(connection2)
                # time3 = time.time()
                # #await recievingDataServer(connection2, sizeMessage2)		
                # time4 = time.time()
                # rtt2 = ((time4 - time3) * 1000)/2
                # print("Total Latency2: {:.2f} ms".format(rtt2))
                #row = [rtt]
                #writer.writerow(row)
                iteration = iteration + 1
                print(iteration)
        s.shutdown(socket.SHUT_RDWR)
        s1.close()
        #s2.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

